"""Import/Export Router — bulk CSV in, CSV out.

Reads run at read-tier; writes (POST imports) require require_write.
All imports log to sale_import_log per CLAUDE.md rule #2.

CSV-only by design. xlsx import is a Phase 2 follow-up — pandas/openpyxl
adds heavy dependencies that don't pay off until volume justifies it.
"""

import csv
import io
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse

import structlog

try:
    from ..database import query, execute
    from ..auth import require_write
except ImportError:
    from database import query, execute
    from auth import require_write

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/io", tags=["Import-Export"])


# ═══════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════

def _log_import(
    source: str,
    file_name: str,
    inserted: int,
    skipped: int,
    errors: int,
    notes: str = "",
) -> str:
    """Append to sale_import_log.

    Schema: id, import_type, source_file, records_total, records_imported,
    records_failed, errors, imported_by, started_at, completed_at.
    """
    log_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    error_summary = notes if notes else f"skipped={skipped}, errors={errors}"
    execute(
        """
        INSERT INTO sale_import_log
            (id, import_type, source_file, records_total, records_imported,
             records_failed, errors, imported_by, started_at, completed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            log_id, source, file_name,
            inserted + skipped + errors,
            inserted, errors, error_summary,
            "API",
            now, now,
        ],
    )
    return log_id


def _read_csv(file: UploadFile) -> list[dict]:
    """Decode UploadFile to list[dict]. UTF-8 BOM tolerated, ; or , autodetected."""
    raw = file.file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Empty file")
    text = raw.decode("utf-8-sig", errors="replace")
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    return [row for row in reader]


# ═══════════════════════════════════════════════════════════════
# Customers — import
# ═══════════════════════════════════════════════════════════════

@router.post("/import/customers", dependencies=[Depends(require_write)])
async def import_customers_csv(
    file: UploadFile = File(...),
    dry_run: bool = Query(False, description="Validate without inserting"),
):
    """Bulk-import customers from CSV.

    Required columns: name. Optional: code, country, region, address,
    website, business_description, status. Rows with a duplicate `code`
    are skipped (not errored). Empty `name` rows are errored.
    """
    rows = _read_csv(file)
    if not rows:
        raise HTTPException(status_code=400, detail="CSV has no data rows")

    inserted = 0
    skipped = 0
    errors = []
    skipped_codes = []
    now = datetime.now().isoformat()

    existing_codes = {
        r["code"]
        for r in query("SELECT code FROM sale_customers WHERE code IS NOT NULL")
        if r.get("code")
    }

    for idx, row in enumerate(rows, start=2):  # +1 header, +1 1-indexed
        name = (row.get("name") or "").strip()
        if not name:
            errors.append({"row": idx, "error": "missing name"})
            continue

        code = (row.get("code") or "").strip() or None
        if code and code in existing_codes:
            skipped += 1
            skipped_codes.append(code)
            continue

        if dry_run:
            inserted += 1
            if code:
                existing_codes.add(code)
            continue

        customer_id = str(uuid.uuid4())
        execute(
            """
            INSERT INTO sale_customers
                (id, code, name, country, region, address, website,
                 business_description, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                customer_id, code, name,
                (row.get("country") or "").strip() or None,
                (row.get("region") or "").strip() or None,
                (row.get("address") or "").strip() or None,
                (row.get("website") or "").strip() or None,
                (row.get("business_description") or "").strip() or None,
                (row.get("status") or "ACTIVE").strip(),
                now, now,
            ],
        )
        inserted += 1
        if code:
            existing_codes.add(code)

    if not dry_run:
        log_id = _log_import(
            source="api_csv",
            file_name=file.filename or "customers.csv",
            inserted=inserted,
            skipped=skipped,
            errors=len(errors),
            notes=f"Errors: {errors[:5]}" if errors else "",
        )
    else:
        log_id = None

    return {
        "dry_run": dry_run,
        "inserted": inserted,
        "skipped_dup_code": skipped,
        "skipped_codes_sample": skipped_codes[:10],
        "errors": errors[:50],
        "error_count": len(errors),
        "import_log_id": log_id,
    }


# ═══════════════════════════════════════════════════════════════
# Contacts — import
# ═══════════════════════════════════════════════════════════════

@router.post("/import/contacts", dependencies=[Depends(require_write)])
async def import_contacts_csv(
    file: UploadFile = File(...),
    dry_run: bool = Query(False),
):
    """Bulk-import customer contacts from CSV.

    Required: name + (customer_id OR customer_code). Optional: email, phone,
    position, linkedin, is_primary. Rows referencing an unknown customer
    are errored.
    """
    rows = _read_csv(file)
    if not rows:
        raise HTTPException(status_code=400, detail="CSV has no data rows")

    customers = query("SELECT id, code FROM sale_customers")
    by_code = {(c.get("code") or ""): c["id"] for c in customers if c.get("code")}
    valid_ids = {c["id"] for c in customers}

    inserted = 0
    errors = []
    now = datetime.now().isoformat()

    for idx, row in enumerate(rows, start=2):
        name = (row.get("name") or "").strip()
        if not name:
            errors.append({"row": idx, "error": "missing name"})
            continue

        cust_id = (row.get("customer_id") or "").strip() or None
        cust_code = (row.get("customer_code") or "").strip() or None
        if cust_id and cust_id not in valid_ids:
            errors.append({"row": idx, "error": f"unknown customer_id: {cust_id}"})
            continue
        if not cust_id and cust_code:
            cust_id = by_code.get(cust_code)
            if not cust_id:
                errors.append({"row": idx, "error": f"unknown customer_code: {cust_code}"})
                continue
        if not cust_id:
            errors.append({"row": idx, "error": "need customer_id or customer_code"})
            continue

        if dry_run:
            inserted += 1
            continue

        contact_id = str(uuid.uuid4())
        is_primary_raw = (row.get("is_primary") or "").strip().lower()
        is_primary = 1 if is_primary_raw in ("1", "true", "yes", "y") else 0

        if is_primary:
            execute(
                "UPDATE sale_customer_contacts SET is_primary = 0 "
                "WHERE customer_id = ?",
                [cust_id],
            )

        execute(
            """
            INSERT INTO sale_customer_contacts
                (id, customer_id, name, email, phone, position, linkedin,
                 is_primary, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                contact_id, cust_id, name,
                (row.get("email") or "").strip() or None,
                (row.get("phone") or "").strip() or None,
                (row.get("position") or "").strip() or None,
                (row.get("linkedin") or "").strip() or None,
                is_primary, now,
            ],
        )
        inserted += 1

    if not dry_run:
        log_id = _log_import(
            source="api_csv",
            file_name=file.filename or "contacts.csv",
            inserted=inserted,
            skipped=0,
            errors=len(errors),
            notes=f"Errors: {errors[:5]}" if errors else "",
        )
    else:
        log_id = None

    return {
        "dry_run": dry_run,
        "inserted": inserted,
        "errors": errors[:50],
        "error_count": len(errors),
        "import_log_id": log_id,
    }


# ═══════════════════════════════════════════════════════════════
# Generic CSV stream helper for exports
# ═══════════════════════════════════════════════════════════════

def _stream_csv(rows: list[dict], columns: list[str], filename: str):
    """Build a StreamingResponse over an in-memory CSV."""
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf, fieldnames=columns,
        extrasaction="ignore", quoting=csv.QUOTE_MINIMAL,
    )
    writer.writeheader()
    for r in rows:
        writer.writerow({k: r.get(k) if r.get(k) is not None else "" for k in columns})
    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ═══════════════════════════════════════════════════════════════
# Exports
# ═══════════════════════════════════════════════════════════════

@router.get("/export/customers")
async def export_customers_csv(
    region: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """Export customers as CSV. Filters mirror /customers list."""
    where = []
    params: list = []
    if region:
        where.append("region = ?"); params.append(region)
    if status:
        where.append("status = ?"); params.append(status)
    where_sql = " AND ".join(where) if where else "1=1"

    rows = query(
        f"SELECT * FROM sale_customers WHERE {where_sql} ORDER BY name ASC",
        params,
    )
    columns = [
        "id", "code", "name", "country", "region", "address", "website",
        "business_description", "status", "created_at", "updated_at",
    ]
    return _stream_csv(rows, columns, "customers.csv")


@router.get("/export/contacts")
async def export_contacts_csv(
    customer_id: Optional[str] = Query(None),
):
    """Export contacts as CSV."""
    where = []
    params: list = []
    if customer_id:
        where.append("ct.customer_id = ?"); params.append(customer_id)
    where_sql = " AND ".join(where) if where else "1=1"
    rows = query(
        f"""
        SELECT ct.id, ct.customer_id, c.code AS customer_code, c.name AS customer_name,
               ct.name, ct.email, ct.phone, ct.position, ct.linkedin,
               ct.is_primary, ct.created_at
        FROM sale_customer_contacts ct
        LEFT JOIN sale_customers c ON c.id = ct.customer_id
        WHERE {where_sql}
        ORDER BY c.name, ct.name
        """,
        params,
    )
    columns = [
        "id", "customer_id", "customer_code", "customer_name",
        "name", "email", "phone", "position", "linkedin",
        "is_primary", "created_at",
    ]
    return _stream_csv(rows, columns, "contacts.csv")


@router.get("/export/opportunities")
async def export_opportunities_csv(
    stage: Optional[str] = Query(None),
    product_group: Optional[str] = Query(None),
    assigned_to: Optional[str] = Query(None),
):
    """Export opportunities (pipeline) as CSV."""
    where = []
    params: list = []
    if stage:
        where.append("stage = ?"); params.append(stage)
    if product_group:
        where.append("product_group = ?"); params.append(product_group)
    if assigned_to:
        where.append("assigned_to = ?"); params.append(assigned_to)
    where_sql = " AND ".join(where) if where else "1=1"

    rows = query(
        f"SELECT * FROM sale_opportunities WHERE {where_sql} "
        f"ORDER BY last_activity_date DESC",
        params,
    )
    columns = [
        "id", "pl_hd", "product_group", "customer_name", "project_name",
        "scope_en", "stage", "win_probability", "weight_ton",
        "contract_value_usd", "gm_percent", "gm_value_usd",
        "estimated_signing", "assigned_to", "stale_flag",
        "last_activity_date", "created_at",
    ]
    return _stream_csv(rows, columns, "opportunities.csv")


@router.get("/export/quotations")
async def export_quotations_csv(
    status: Optional[str] = Query(None),
    market: Optional[str] = Query(None),
    year: Optional[str] = Query(None),
):
    """Export quotation history as CSV."""
    where = []
    params: list = []
    if status:
        where.append("status = ?"); params.append(status)
    if market:
        where.append("market = ?"); params.append(market)
    if year:
        where.append("strftime('%Y', date_offer) = ?"); params.append(year)
    where_sql = " AND ".join(where) if where else "1=1"

    rows = query(
        f"SELECT * FROM sale_quotation_history WHERE {where_sql} "
        f"ORDER BY date_offer DESC, quotation_no DESC",
        params,
    )
    columns = [
        "id", "quotation_no", "customer_code", "customer_name", "country",
        "market", "product_type", "project_name", "weight_ton",
        "price_usd_mt", "value_usd", "value_vnd", "gross_profit_usd",
        "gp_percent", "date_offer", "incharge", "status", "owner",
    ]
    return _stream_csv(rows, columns, "quotations.csv")


@router.get("/import/log")
async def list_import_log(
    import_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Paginated read of sale_import_log — useful to verify CSV imports."""
    where = []
    params: list = []
    if import_type:
        where.append("import_type = ?"); params.append(import_type)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_import_log WHERE {where_sql}",
        params,
    )[0]["cnt"]
    items = query(
        f"SELECT * FROM sale_import_log WHERE {where_sql} "
        f"ORDER BY started_at DESC LIMIT ? OFFSET ?",
        params + [limit, offset],
    )
    return {"total": total, "items": items, "limit": limit, "offset": offset}
