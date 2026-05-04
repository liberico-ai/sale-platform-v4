"""
Customers Router
Manages customer data, search, and customer details with contacts and opportunities.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

import structlog

try:
    from ..database import query, execute
    from ..auth import UserContext, get_current_writer, get_current_admin
    from ..errors import DuplicateError, EntityNotFoundError
    from ..services.audit import log_status_change, log_change
    from ..models.customer import CustomerCreate, CustomerUpdate
except ImportError:
    from database import query, execute
    from auth import UserContext, get_current_writer, get_current_admin
    from errors import DuplicateError, EntityNotFoundError
    from services.audit import log_status_change, log_change
    from models.customer import CustomerCreate, CustomerUpdate

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("")
async def list_customers(
    region: Optional[str] = Query(None, description="Filter by region"),
    status: Optional[str] = Query(None, description="Filter by status (ACTIVE, INACTIVE, etc.)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    List all customers with optional filtering by region and status.
    Supports pagination with limit and offset.
    
    Args:
        region: Optional region filter
        status: Optional status filter
        limit: Number of results to return (1-200)
        offset: Number of results to skip
        
    Returns:
        dict: Total count, items list, limit, and offset
    """
    # Filter out soft-deleted rows by default. Callers can opt in to
    # deleted rows by passing status='DELETED' explicitly.
    where = []
    params = []

    if region:
        where.append("region = ?")
        params.append(region)
    if status:
        where.append("status = ?")
        params.append(status)
    else:
        where.append("(status IS NULL OR status != 'DELETED')")

    where_sql = " AND ".join(where) if where else "1=1"

    total = query(f"SELECT COUNT(*) as cnt FROM sale_customers WHERE {where_sql}", params)[0]["cnt"]
    items = query(f"""
        SELECT * FROM sale_customers
        WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """, params + [limit, offset])

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/search")
async def search_customers(
    q: str = Query(..., description="Search query (name, code, country, or business_description)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Search customers by name, code, country, or business description.

    Joins sale_customer_contacts to also match contact emails.

    Returns:
        dict: Total count, items list, limit, and offset.
    """
    search_param = f"%{q}%"

    total = query("""
        SELECT COUNT(DISTINCT c.id) as cnt
        FROM sale_customers c
        LEFT JOIN sale_customer_contacts ct ON ct.customer_id = c.id
        WHERE c.name LIKE ? OR c.code LIKE ?
           OR c.country LIKE ? OR c.business_description LIKE ?
           OR ct.email LIKE ? OR ct.name LIKE ?
    """, [search_param] * 6)[0]["cnt"]

    items = query("""
        SELECT DISTINCT c.*
        FROM sale_customers c
        LEFT JOIN sale_customer_contacts ct ON ct.customer_id = c.id
        WHERE c.name LIKE ? OR c.code LIKE ?
           OR c.country LIKE ? OR c.business_description LIKE ?
           OR ct.email LIKE ? OR ct.name LIKE ?
        ORDER BY c.name ASC
        LIMIT ? OFFSET ?
    """, [search_param] * 6 + [limit, offset])

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/duplicates")
async def find_customer_duplicates(
    threshold: int = Query(3, ge=2, le=10, description="Min token-overlap to flag as a possible dup"),
    limit: int = Query(50, ge=1, le=200),
):
    """Find candidate customer duplicates using normalised name tokens.

    Strategy: lower-case the name, strip company suffixes (Co., Ltd, Inc., etc.),
    group by the first `threshold` characters of the cleaned name. Returns
    groups with 2+ rows.
    """
    rows = query("""
        SELECT id, name, code, country, status FROM sale_customers
        WHERE status != 'DELETED' OR status IS NULL
    """)

    suffix_words = {
        "co", "co.", "ltd", "ltd.", "inc", "inc.", "corp", "corp.",
        "company", "limited", "incorporated", "corporation",
        "jsc", "joint", "stock", "group", "holdings",
        "the", "and", "&",
    }

    def normalize(name: str) -> str:
        if not name:
            return ""
        clean = name.lower()
        for ch in [",", ".", "-", "_", "/", "\\", "(", ")"]:
            clean = clean.replace(ch, " ")
        tokens = [t for t in clean.split() if t and t not in suffix_words]
        return " ".join(tokens)

    buckets: dict[str, list[dict]] = {}
    for r in rows:
        norm = normalize(r.get("name") or "")
        if not norm or len(norm) < threshold:
            continue
        key = norm[:threshold]
        buckets.setdefault(key, []).append({
            "id": r["id"],
            "name": r.get("name"),
            "code": r.get("code"),
            "country": r.get("country"),
            "normalised": norm,
        })

    groups = []
    for key, members in buckets.items():
        if len(members) >= 2:
            groups.append({
                "match_prefix": key,
                "count": len(members),
                "members": members,
            })

    groups.sort(key=lambda g: g["count"], reverse=True)
    return {"threshold": threshold, "groups": groups[:limit], "group_count": len(groups)}


# Cross-customer interactions, contacts, quotations live in their own routers
# (/interactions, /contacts, /quotations). This file only owns the
# /customers/{id}/* nested sub-resources below.


@router.get("/{customer_id}")
async def get_customer_detail(customer_id: str):
    """Get customer detail with contacts, opportunities, and recent interactions."""
    customer = query(
        "SELECT * FROM sale_customers WHERE id = ?",
        [customer_id],
        one=True
    )

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    contacts = query(
        "SELECT * FROM sale_customer_contacts WHERE customer_id = ? "
        "ORDER BY is_primary DESC, created_at DESC",
        [customer_id]
    )

    opportunities = query(
        "SELECT * FROM sale_opportunities WHERE customer_id = ? "
        "ORDER BY created_at DESC",
        [customer_id]
    )

    interactions = query(
        "SELECT * FROM sale_customer_interactions WHERE customer_id = ? "
        "ORDER BY interaction_date DESC LIMIT 20",
        [customer_id]
    )

    return {
        "customer": dict(customer),
        "contacts": contacts,
        "opportunities": opportunities,
        "interactions": interactions,
    }


@router.get("/{customer_id}/contacts")
async def list_customer_contacts(customer_id: str):
    """All contacts for a customer (primary first)."""
    items = query(
        """
        SELECT * FROM sale_customer_contacts
        WHERE customer_id = ?
        ORDER BY is_primary DESC, name ASC
        """,
        [customer_id],
    )
    return {"customer_id": customer_id, "items": items, "count": len(items)}


@router.get("/{customer_id}/interactions")
async def list_customer_interactions(
    customer_id: str,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """All interactions for a customer (newest first)."""
    total = query(
        "SELECT COUNT(*) as cnt FROM sale_customer_interactions WHERE customer_id = ?",
        [customer_id],
    )[0]["cnt"]

    items = query(
        """
        SELECT * FROM sale_customer_interactions
        WHERE customer_id = ?
        ORDER BY interaction_date DESC
        LIMIT ? OFFSET ?
        """,
        [customer_id, limit, offset],
    )
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/{customer_id}/quotations")
async def list_customer_quotations(
    customer_id: str,
    status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Quotation history for a customer.

    Matches by linked customer_id OR by customer_code (legacy import rows
    weren't always backfilled with the canonical customer_id).
    """
    customer = query(
        "SELECT id, code FROM sale_customers WHERE id = ?",
        [customer_id],
        one=True,
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    where = ["(qh.customer_id = ? OR qh.customer_code = ?)"]
    params: list = [customer_id, customer.get("code") or ""]
    if status:
        where.append("qh.status = ?")
        params.append(status)
    where_sql = " AND ".join(where)

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_quotation_history qh WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT qh.* FROM sale_quotation_history qh
        WHERE {where_sql}
        ORDER BY qh.date_offer DESC, qh.quotation_no DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/{customer_id}/contracts")
async def list_customer_contracts(customer_id: str):
    """Active contracts linked to this customer."""
    customer = query(
        "SELECT id FROM sale_customers WHERE id = ?",
        [customer_id],
        one=True,
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    items = query(
        """
        SELECT * FROM sale_active_contracts
        WHERE customer_id = ?
        ORDER BY latest_activity DESC, start_date DESC
        """,
        [customer_id],
    )
    return {"customer_id": customer_id, "items": items, "count": len(items)}


@router.get("/{customer_id}/timeline")
async def customer_activity_timeline(
    customer_id: str,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Unified activity timeline for a customer (UNIFIED step 10).

    Merges interactions + emails + quotations + contracts into a single
    chronologically sorted feed. Each event has the same shape so the
    frontend can render them with one template.
    """
    customer = query(
        "SELECT id, name FROM sale_customers WHERE id = ?",
        [customer_id], one=True,
    )
    if not customer:
        raise EntityNotFoundError("Customer", customer_id)

    # UNION ALL across the four event sources, normalising columns:
    #   event_type | title | description | event_date | entity_id
    # COALESCE on date columns keeps the rows ordered consistently
    # regardless of which source has the most-fresh timestamp.
    rows = query(
        """
        SELECT * FROM (
            SELECT
                'interaction' AS event_type,
                COALESCE(subject, interaction_type, 'INTERACTION') AS title,
                summary AS description,
                COALESCE(interaction_date, created_at) AS event_date,
                id AS entity_id
            FROM sale_customer_interactions
            WHERE customer_id = ?

            UNION ALL

            SELECT
                'email' AS event_type,
                COALESCE(subject, '(no subject)') AS title,
                snippet AS description,
                COALESCE(received_at, created_at) AS event_date,
                id AS entity_id
            FROM sale_emails
            WHERE customer_id = ?

            UNION ALL

            SELECT
                'quotation' AS event_type,
                COALESCE(project_name, 'Quotation #' || quotation_no) AS title,
                'Status: ' || COALESCE(status, '?') ||
                  ' | Value: ' || COALESCE(CAST(value_usd AS TEXT), '-') AS description,
                COALESCE(date_offer, created_at) AS event_date,
                id AS entity_id
            FROM sale_quotation_history
            WHERE customer_id = ?

            UNION ALL

            SELECT
                'contract' AS event_type,
                COALESCE(project_name, po_number, 'Contract') AS title,
                'PO: ' || COALESCE(po_number, '-') ||
                  ' | Status: ' || COALESCE(contract_status, '-') AS description,
                COALESCE(latest_activity, start_date, created_at) AS event_date,
                id AS entity_id
            FROM sale_active_contracts
            WHERE customer_id = ?
        )
        WHERE event_date IS NOT NULL
        ORDER BY event_date DESC
        LIMIT ? OFFSET ?
        """,
        [customer_id, customer_id, customer_id, customer_id, limit, offset],
    )

    total_row = query(
        """
        SELECT
            (SELECT COUNT(*) FROM sale_customer_interactions WHERE customer_id = ?)
          + (SELECT COUNT(*) FROM sale_emails WHERE customer_id = ?)
          + (SELECT COUNT(*) FROM sale_quotation_history WHERE customer_id = ?)
          + (SELECT COUNT(*) FROM sale_active_contracts WHERE customer_id = ?)
            AS cnt
        """,
        [customer_id, customer_id, customer_id, customer_id],
        one=True,
    ) or {}

    return {
        "customer_id": customer_id,
        "customer_name": customer.get("name"),
        "total": int(total_row.get("cnt") or 0),
        "items": rows,
        "limit": limit,
        "offset": offset,
    }


# ═══════════════════════════════════════════════════════════════
# Writes — POST / PATCH / soft DELETE
# ═══════════════════════════════════════════════════════════════

def _generate_code_from_name(name: str) -> str:
    """Auto-derive a customer code from name when caller leaves it blank.

    First 3 alphanumeric uppercased + numeric suffix to avoid collisions.
    Falls back to UUID slice if name has no usable letters.
    """
    letters = "".join(ch for ch in name if ch.isalnum())[:3].upper()
    if not letters:
        letters = uuid.uuid4().hex[:3].upper()

    # Find next sequence not in use
    for n in range(1, 1000):
        candidate = f"{letters}{n:03d}"
        existing = query(
            "SELECT 1 FROM sale_customers WHERE code = ?",
            [candidate],
            one=True,
        )
        if not existing:
            return candidate
    # Last-ditch unique fallback
    return f"{letters}-{uuid.uuid4().hex[:6].upper()}"


@router.post("")
async def create_customer(
    payload: CustomerCreate,
    user: UserContext = Depends(get_current_writer),
):
    """Create a new customer.

    Auto-generates a customer code when none is supplied.
    Rejects duplicate names (case-insensitive) and codes via DuplicateError.
    """
    # Duplicate detection on name (case-insensitive). Mirrors what the team
    # would otherwise enforce manually — see UNIFIED step 13.
    name_clash = query(
        "SELECT id, code FROM sale_customers "
        "WHERE LOWER(name) = LOWER(?) AND status != 'DELETED'",
        [payload.name],
        one=True,
    )
    if name_clash:
        raise DuplicateError("Customer", "name", payload.name)

    if payload.code:
        existing = query(
            "SELECT id FROM sale_customers WHERE code = ?",
            [payload.code],
            one=True,
        )
        if existing:
            raise DuplicateError("Customer", "code", payload.code)
        code = payload.code
    else:
        code = _generate_code_from_name(payload.name)

    customer_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    status = payload.status or "ACTIVE"

    execute(
        """
        INSERT INTO sale_customers
            (id, code, name, country, region, address, website,
             business_description, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            customer_id, code, payload.name, payload.country, payload.region,
            payload.address, payload.website, payload.business_description,
            status, now, now,
        ],
    )

    logger.info(
        "customer_created",
        customer_id=customer_id,
        code=code,
        name=payload.name,
    )

    return {
        "id": customer_id,
        "code": code,
        "name": payload.name,
        "status": status,
        "message": f"Customer created: {payload.name} ({code})",
    }


@router.patch("/{customer_id}")
async def update_customer(
    customer_id: str,
    payload: CustomerUpdate,
    user: UserContext = Depends(get_current_writer),
):
    """Update an existing customer.

    Audit-logs status changes. Only fields explicitly set in the payload
    are updated.
    """
    existing = query(
        "SELECT * FROM sale_customers WHERE id = ?",
        [customer_id],
        one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Customer not found")

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Code uniqueness check when changing code
    if "code" in data and data["code"] and data["code"] != existing.get("code"):
        clash = query(
            "SELECT id FROM sale_customers WHERE code = ? AND id != ?",
            [data["code"], customer_id],
            one=True,
        )
        if clash:
            raise DuplicateError("Customer", "code", data["code"])

    sets = [f"{k} = ?" for k in data.keys()]
    params = list(data.values()) + [datetime.now().isoformat(), customer_id]
    sets.append("updated_at = ?")

    execute(
        f"UPDATE sale_customers SET {', '.join(sets)} WHERE id = ?",
        params,
    )

    if "status" in data and data["status"] != existing.get("status"):
        log_status_change(
            "customer", customer_id,
            existing.get("status") or "", data["status"],
            changed_by=user.actor,
        )

    return {"id": customer_id, "status": "ok", "updated_fields": list(data.keys())}


@router.delete("/{customer_id}")
async def soft_delete_customer(
    customer_id: str,
    user: UserContext = Depends(get_current_admin),
):
    """Soft-delete: set status='DELETED', do NOT remove the row.

    Hard delete is intentionally unsupported — child records (opportunities,
    contacts, interactions, quotations) reference this customer.
    """
    existing = query(
        "SELECT id, status FROM sale_customers WHERE id = ?",
        [customer_id],
        one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Customer not found")

    if existing.get("status") == "DELETED":
        return {"id": customer_id, "status": "already_deleted"}

    now = datetime.now().isoformat()
    execute(
        "UPDATE sale_customers SET status = 'DELETED', updated_at = ? WHERE id = ?",
        [now, customer_id],
    )

    log_status_change(
        "customer", customer_id,
        existing.get("status") or "", "DELETED",
        changed_by=user.actor,
    )

    logger.info("customer_soft_deleted", customer_id=customer_id)

    return {"id": customer_id, "status": "deleted",
            "message": "Customer deactivated (soft delete)"}


# ═══════════════════════════════════════════════════════════════
# Create-from-context (Phase 2 step 8)
# ═══════════════════════════════════════════════════════════════

class _FollowUpFromCustomer(BaseModel):
    """Body for /customers/{id}/create-follow-up.

    Schema requires opportunity_id (NOT NULL FK) so callers must
    supply one — pick the opportunity to attach the follow-up to.
    """
    opportunity_id: str
    schedule_type: str   # CALL | EMAIL | VISIT | MEETING
    next_follow_up: str  # ISO datetime
    contact_id: Optional[str] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


@router.post("/{customer_id}/create-follow-up")
async def create_follow_up_from_customer(
    customer_id: str,
    payload: _FollowUpFromCustomer,
    user: UserContext = Depends(get_current_writer),
):
    """Create a follow-up scheduled against this customer.

    Pre-fills customer_id; the opportunity_id must come from the body
    because the schema enforces it.
    """
    cust = query(
        "SELECT id FROM sale_customers WHERE id = ?",
        [customer_id], one=True,
    )
    if not cust:
        raise EntityNotFoundError("Customer", customer_id)

    opp = query(
        "SELECT id FROM sale_opportunities WHERE id = ?",
        [payload.opportunity_id], one=True,
    )
    if not opp:
        raise EntityNotFoundError("Opportunity", payload.opportunity_id)

    follow_up_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute(
        """
        INSERT INTO sale_follow_up_schedules
            (id, opportunity_id, customer_id, contact_id, schedule_type,
             next_follow_up, follow_up_count, is_active, status,
             assigned_to, notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, 0, 1, 'PENDING', ?, ?, ?, ?)
        """,
        [
            follow_up_id, payload.opportunity_id, customer_id,
            payload.contact_id, payload.schedule_type,
            payload.next_follow_up,
            payload.assigned_to or user.actor,
            payload.notes, now, now,
        ],
    )

    return {
        "id": follow_up_id,
        "customer_id": customer_id,
        "opportunity_id": payload.opportunity_id,
        "next_follow_up": payload.next_follow_up,
        "status": "PENDING",
    }
