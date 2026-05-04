"""Quotations Router — sale_quotation_history (968) + sale_quotation_revisions (147).

Quotation_history is the historical xlsx import (each row = one quote).
Quotation_revisions belong to a specific opportunity (opp-scoped revisions).
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

import structlog

try:
    from ..database import query, execute
    from ..auth import UserContext, get_current_writer
    from ..models.quotation import QuotationCreate, QuotationUpdate, QuotationRevise
    from ..services.state_machine import (
        validate_quotation_transition,
        get_allowed_quotation_transitions,
        InvalidTransitionError,
    )
    from ..services.audit import log_status_change, log_financial_change
except ImportError:
    from database import query, execute
    from auth import UserContext, get_current_writer
    from models.quotation import QuotationCreate, QuotationUpdate, QuotationRevise
    from services.state_machine import (
        validate_quotation_transition,
        get_allowed_quotation_transitions,
        InvalidTransitionError,
    )
    from services.audit import log_status_change, log_financial_change

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/quotations", tags=["Quotations"])


# ═══════════════════════════════════════════════════════════════
# Pydantic models imported from models/quotation.py (rule #16)
# ═══════════════════════════════════════════════════════════════


# Financial fields whose changes get audit-logged
_AUDITED_QUOTATION_FIELDS = {
    "weight_ton", "price_usd_mt", "value_vnd", "value_usd",
    "gross_profit_usd", "gp_percent",
}


@router.get("")
async def list_quotations(
    customer_id: Optional[str] = Query(None, description="Filter by linked sale_customers.id"),
    customer_code: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    market: Optional[str] = Query(None),
    product_type: Optional[str] = Query(None),
    incharge: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None, description="ISO date — date_offer >= ?"),
    date_to: Optional[str] = Query(None, description="ISO date — date_offer <= ?"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List historical quotations from sale_quotation_history."""
    where = []
    params: list = []
    if customer_id:
        where.append("customer_id = ?")
        params.append(customer_id)
    if customer_code:
        where.append("customer_code = ?")
        params.append(customer_code)
    if status:
        where.append("status = ?")
        params.append(status)
    if market:
        where.append("market = ?")
        params.append(market)
    if product_type:
        where.append("product_type = ?")
        params.append(product_type)
    if incharge:
        where.append("incharge = ?")
        params.append(incharge)
    if date_from:
        where.append("date_offer >= ?")
        params.append(date_from)
    if date_to:
        where.append("date_offer <= ?")
        params.append(date_to)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_quotation_history WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT * FROM sale_quotation_history
        WHERE {where_sql}
        ORDER BY date_offer DESC, quotation_no DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/win-rate")
async def quotation_win_rate(
    market: Optional[str] = Query(None),
    product_type: Optional[str] = Query(None),
    year: Optional[str] = Query(None, description="Filter date_offer YYYY"),
):
    """Win rate (status='WON' vs total) over sale_quotation_history."""
    where = []
    params: list = []
    if market:
        where.append("market = ?")
        params.append(market)
    if product_type:
        where.append("product_type = ?")
        params.append(product_type)
    if year:
        where.append("strftime('%Y', date_offer) = ?")
        params.append(year)
    where_sql = " AND ".join(where) if where else "1=1"

    stats = query(
        f"""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN UPPER(status) = 'WON' THEN 1 ELSE 0 END) AS won,
            SUM(CASE WHEN UPPER(status) = 'LOST' THEN 1 ELSE 0 END) AS lost,
            SUM(CASE WHEN status IS NULL OR status = '' THEN 1 ELSE 0 END) AS unknown,
            COALESCE(SUM(CASE WHEN UPPER(status) = 'WON' THEN value_usd END), 0) AS won_value_usd
        FROM sale_quotation_history
        WHERE {where_sql}
        """,
        params,
        one=True,
    ) or {}

    total = stats.get("total", 0) or 0
    won = stats.get("won", 0) or 0

    return {
        "filter": {"market": market, "product_type": product_type, "year": year},
        "total_quotations": total,
        "won_count": won,
        "lost_count": stats.get("lost", 0),
        "unknown_count": stats.get("unknown", 0),
        "won_value_usd": stats.get("won_value_usd", 0),
        "win_rate_pct": round(won / total * 100, 1) if total > 0 else 0.0,
    }


@router.get("/{quotation_id}")
async def get_quotation(quotation_id: str):
    """Get a single historical quotation."""
    item = query(
        """
        SELECT qh.*, c.name AS linked_customer_name
        FROM sale_quotation_history qh
        LEFT JOIN sale_customers c ON c.id = qh.customer_id
        WHERE qh.id = ?
        """,
        [quotation_id],
        one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return {"quotation": dict(item)}


# ═══════════════════════════════════════════════════════════════
# Revisions — sale_quotation_revisions (opportunity-scoped, 147 rows)
# ═══════════════════════════════════════════════════════════════

@router.get("/revisions/list")
async def list_revisions(
    opportunity_id: Optional[str] = Query(None),
    customer_response: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List quotation revisions across all opportunities."""
    where = []
    params: list = []
    if opportunity_id:
        where.append("qr.opportunity_id = ?")
        params.append(opportunity_id)
    if customer_response:
        where.append("qr.customer_response = ?")
        params.append(customer_response)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_quotation_revisions qr WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT qr.*, o.project_name, o.customer_name
        FROM sale_quotation_revisions qr
        LEFT JOIN sale_opportunities o ON o.id = qr.opportunity_id
        WHERE {where_sql}
        ORDER BY qr.revision_date DESC, qr.revision_number DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/by-opportunity/{opportunity_id}/revisions")
async def list_opportunity_revisions(opportunity_id: str):
    """All revisions for one opportunity (newest first)."""
    items = query(
        """
        SELECT * FROM sale_quotation_revisions
        WHERE opportunity_id = ?
        ORDER BY revision_number DESC
        """,
        [opportunity_id],
    )
    return {"opportunity_id": opportunity_id, "items": items, "count": len(items)}


# ═══════════════════════════════════════════════════════════════
# Writes — POST / PATCH / revise
# ═══════════════════════════════════════════════════════════════

def _next_quotation_no() -> int:
    """Next quotation_no for sale_quotation_history (max + 1)."""
    row = query(
        "SELECT COALESCE(MAX(quotation_no), 0) + 1 AS next_no "
        "FROM sale_quotation_history",
        one=True,
    ) or {}
    return int(row.get("next_no") or 1)


@router.post("")
async def create_quotation(
    payload: QuotationCreate,
    user: UserContext = Depends(get_current_writer),
):
    """Create a new quotation in DRAFT status.

    Either customer_id (canonical) or customer_code/customer_name (legacy)
    must be provided. customer_id is verified against sale_customers when
    supplied.
    """
    if not payload.customer_id and not (payload.customer_code or payload.customer_name):
        raise HTTPException(
            status_code=400,
            detail="Provide customer_id, customer_code, or customer_name",
        )

    customer_name = payload.customer_name
    customer_code = payload.customer_code
    customer_id = payload.customer_id

    if customer_id:
        cust = query(
            "SELECT id, name, code FROM sale_customers WHERE id = ?",
            [customer_id],
            one=True,
        )
        if not cust:
            raise HTTPException(status_code=404, detail="Customer not found")
        customer_name = customer_name or cust.get("name")
        customer_code = customer_code or cust.get("code")

    quotation_id = str(uuid.uuid4())
    quotation_no = _next_quotation_no()
    now = datetime.now().isoformat()
    date_offer = payload.date_offer or now[:10]

    execute(
        """
        INSERT INTO sale_quotation_history
            (id, quotation_no, customer_code, customer_name, country,
             market, product_type, project_name, scope_of_work,
             launch_date, duration_months, weight_ton, price_usd_mt,
             value_vnd, value_usd, gross_profit_usd, gp_percent,
             date_offer, incharge, status, remark, owner,
             customer_id, source, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, 'DRAFT', ?, ?, ?, 'API', ?)
        """,
        [
            quotation_id, quotation_no, customer_code, customer_name,
            payload.country, payload.market, payload.product_type,
            payload.project_name, payload.scope_of_work,
            payload.launch_date, payload.duration_months,
            payload.weight_ton, payload.price_usd_mt,
            payload.value_vnd, payload.value_usd,
            payload.gross_profit_usd, payload.gp_percent,
            date_offer, payload.incharge, payload.remark, payload.owner,
            customer_id, now,
        ],
    )

    logger.info(
        "quotation_created",
        quotation_id=quotation_id,
        quotation_no=quotation_no,
        project_name=payload.project_name,
    )

    return {
        "id": quotation_id,
        "quotation_no": quotation_no,
        "status": "DRAFT",
        "message": f"Quotation created: {payload.project_name} (#{quotation_no})",
    }


@router.patch("/{quotation_id}")
async def update_quotation(
    quotation_id: str,
    payload: QuotationUpdate,
    user: UserContext = Depends(get_current_writer),
):
    """Update a quotation. Status changes are validated via state machine.

    Allowed transitions:
      DRAFT → SENT, NEGOTIATION, CANCELLED
      SENT → NEGOTIATION, WON, LOST, EXPIRED
      NEGOTIATION → WON, LOST, EXPIRED
      LOST → DRAFT (reopen)
      EXPIRED → DRAFT (reopen)
    """
    existing = query(
        "SELECT * FROM sale_quotation_history WHERE id = ?",
        [quotation_id],
        one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Quotation not found")

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    # State machine: validate before writing
    new_status = data.get("status")
    if new_status is not None and new_status != existing.get("status"):
        try:
            validate_quotation_transition(
                existing.get("status") or "DRAFT", new_status,
            )
        except InvalidTransitionError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        log_status_change(
            "quotation", quotation_id,
            existing.get("status") or "", new_status,
            changed_by=user.actor,
        )

    # Audit financial diffs
    financial_diffs = {}
    for field in _AUDITED_QUOTATION_FIELDS:
        if field in data and data[field] != existing.get(field):
            financial_diffs[field] = (existing.get(field), data[field])
    if financial_diffs:
        log_financial_change(
            "quotation", quotation_id, financial_diffs,
            changed_by=user.actor,
        )

    sets = [f"{k} = ?" for k in data.keys()]
    params = list(data.values()) + [quotation_id]
    execute(
        f"UPDATE sale_quotation_history SET {', '.join(sets)} WHERE id = ?",
        params,
    )

    current_status = (data.get("status") or existing.get("status") or "DRAFT").upper()
    return {
        "id": quotation_id,
        "status": "ok",
        "current_status": current_status,
        "allowed_next_statuses": get_allowed_quotation_transitions(current_status),
        "updated_fields": list(data.keys()),
    }


@router.post("/{quotation_id}/revise")
async def revise_quotation(
    quotation_id: str,
    payload: QuotationRevise,
    user: UserContext = Depends(get_current_writer),
):
    """Create a new revision row for a quotation.

    Writes to sale_quotation_revisions (opportunity-scoped). Either the
    parent quotation has an opportunity_id (set on the linked opportunity
    via opp.estimated_signing/quotation_date) OR the caller passes
    opportunity_id in the body.
    """
    quotation = query(
        "SELECT * FROM sale_quotation_history WHERE id = ?",
        [quotation_id],
        one=True,
    )
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    opportunity_id = payload.opportunity_id
    if not opportunity_id:
        # Best-effort match: any opportunity for the same customer with
        # the same project_name. This won't always resolve.
        if quotation.get("customer_id") and quotation.get("project_name"):
            opp = query(
                """
                SELECT id FROM sale_opportunities
                WHERE customer_id = ? AND LOWER(project_name) = LOWER(?)
                LIMIT 1
                """,
                [quotation["customer_id"], quotation["project_name"]],
                one=True,
            )
            if opp:
                opportunity_id = opp["id"]

    if not opportunity_id:
        raise HTTPException(
            status_code=400,
            detail=(
                "opportunity_id required — pass it in the body or link the "
                "quotation's customer+project_name to an existing opportunity"
            ),
        )

    # Next revision number for this opportunity
    last_rev = query(
        "SELECT COALESCE(MAX(revision_number), 0) + 1 AS next_rev "
        "FROM sale_quotation_revisions WHERE opportunity_id = ?",
        [opportunity_id],
        one=True,
    ) or {}
    next_rev = int(last_rev.get("next_rev") or 1)

    revision_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    today = now[:10]

    # Pull values from the body, falling back to the parent quotation
    weight = payload.weight_ton if payload.weight_ton is not None else quotation.get("weight_ton")
    unit_price = payload.unit_price_usd if payload.unit_price_usd is not None else quotation.get("price_usd_mt")
    total_usd = payload.total_value_usd if payload.total_value_usd is not None else quotation.get("value_usd")
    total_vnd = payload.total_value_vnd if payload.total_value_vnd is not None else quotation.get("value_vnd")
    gm_pct = payload.gm_percent if payload.gm_percent is not None else quotation.get("gp_percent")
    gm_val = payload.gm_value if payload.gm_value is not None else quotation.get("gross_profit_usd")

    execute(
        """
        INSERT INTO sale_quotation_revisions
            (id, opportunity_id, revision_number, revision_date,
             revision_reason, quotation_ref,
             weight_ton, unit_price_usd, total_value_usd, total_value_vnd,
             material_cost, labor_cost, overhead_cost, gm_percent, gm_value,
             scope_summary, valid_until, sent_to,
             notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            revision_id, opportunity_id, next_rev, today,
            payload.revision_reason, str(quotation.get("quotation_no") or ""),
            weight, unit_price, total_usd, total_vnd,
            payload.material_cost, payload.labor_cost, payload.overhead_cost,
            gm_pct, gm_val,
            payload.scope_summary, payload.valid_until, payload.sent_to,
            payload.notes, now, now,
        ],
    )

    logger.info(
        "quotation_revision_created",
        quotation_id=quotation_id,
        opportunity_id=opportunity_id,
        revision_id=revision_id,
        revision_number=next_rev,
    )

    return {
        "id": revision_id,
        "quotation_id": quotation_id,
        "opportunity_id": opportunity_id,
        "revision_number": next_rev,
        "status": "ok",
    }
