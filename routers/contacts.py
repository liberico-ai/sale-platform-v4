"""Contacts Router — sale_customer_contacts (2,990 records).

Dedicated resource for customer contacts. Customer-scoped browsing also
exists at /customers/{id}/contacts in the customers router.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

import structlog

try:
    from ..database import query, execute
    from ..auth import require_write
except ImportError:
    from database import query, execute
    from auth import require_write

try:
    from ..models.contact import CustomerContactCreate, CustomerContactUpdate
except ImportError:
    from models.contact import CustomerContactCreate, CustomerContactUpdate

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get("")
async def list_contacts(
    customer_id: Optional[str] = Query(None, description="Filter by customer"),
    is_primary: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List customer contacts with optional customer filter."""
    where = []
    params: list = []
    if customer_id:
        where.append("ct.customer_id = ?")
        params.append(customer_id)
    if is_primary is not None:
        where.append("ct.is_primary = ?")
        params.append(1 if is_primary else 0)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_customer_contacts ct WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT ct.*, c.name AS customer_name, c.code AS customer_code
        FROM sale_customer_contacts ct
        LEFT JOIN sale_customers c ON c.id = ct.customer_id
        WHERE {where_sql}
        ORDER BY ct.is_primary DESC, ct.name ASC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/duplicates")
async def find_contact_duplicates(limit: int = Query(50, ge=1, le=200)):
    """Find candidate contact duplicates by exact email or normalised phone.

    Email match: case-insensitive equality.
    Phone match: digits-only equality (strips +, spaces, dashes).
    """
    by_email = query("""
        SELECT LOWER(email) AS k,
               COUNT(*) AS cnt,
               GROUP_CONCAT(id, '|') AS ids,
               GROUP_CONCAT(name, '|') AS names,
               GROUP_CONCAT(customer_id, '|') AS customer_ids
        FROM sale_customer_contacts
        WHERE email IS NOT NULL AND email != ''
        GROUP BY LOWER(email)
        HAVING COUNT(*) > 1
        ORDER BY cnt DESC
        LIMIT ?
    """, [limit])

    rows = query("""
        SELECT id, name, phone, email, customer_id FROM sale_customer_contacts
        WHERE phone IS NOT NULL AND phone != ''
    """)
    phone_buckets: dict[str, list[dict]] = {}
    for r in rows:
        digits = "".join(ch for ch in (r.get("phone") or "") if ch.isdigit())
        if len(digits) < 7:
            continue
        phone_buckets.setdefault(digits, []).append({
            "id": r["id"],
            "name": r.get("name"),
            "phone": r.get("phone"),
            "email": r.get("email"),
            "customer_id": r.get("customer_id"),
        })

    by_phone = []
    for k, members in phone_buckets.items():
        if len(members) >= 2:
            by_phone.append({
                "phone_digits": k,
                "count": len(members),
                "members": members,
            })
    by_phone.sort(key=lambda x: x["count"], reverse=True)
    by_phone = by_phone[:limit]

    return {
        "by_email": [
            {
                "email": r["k"],
                "count": r["cnt"],
                "ids": (r["ids"] or "").split("|"),
                "names": (r["names"] or "").split("|"),
            }
            for r in by_email
        ],
        "by_phone": by_phone,
    }


@router.get("/{contact_id}")
async def get_contact(contact_id: str):
    """Get a single contact with parent customer info."""
    item = query(
        """
        SELECT ct.*, c.name AS customer_name, c.code AS customer_code,
               c.country AS customer_country
        FROM sale_customer_contacts ct
        LEFT JOIN sale_customers c ON c.id = ct.customer_id
        WHERE ct.id = ?
        """,
        [contact_id],
        one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"contact": dict(item)}


@router.post("", dependencies=[Depends(require_write)])
async def create_contact(contact: CustomerContactCreate):
    """Create a new customer contact.

    Verifies customer exists. If is_primary=True, demotes any existing
    primary contact for that customer first.
    """
    customer = query(
        "SELECT id FROM sale_customers WHERE id = ?",
        [contact.customer_id],
        one=True,
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    contact_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    if contact.is_primary:
        execute(
            "UPDATE sale_customer_contacts SET is_primary = 0 "
            "WHERE customer_id = ?",
            [contact.customer_id],
        )

    execute(
        """
        INSERT INTO sale_customer_contacts
            (id, customer_id, name, email, phone, position, linkedin,
             is_primary, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            contact_id, contact.customer_id, contact.name,
            contact.email, contact.phone, contact.position, contact.linkedin,
            1 if contact.is_primary else 0, now,
        ],
    )

    logger.info(
        "contact_created",
        contact_id=contact_id,
        customer_id=contact.customer_id,
        name=contact.name,
    )

    return {"id": contact_id, "status": "ok", "message": f"Contact created: {contact.name}"}


@router.patch("/{contact_id}", dependencies=[Depends(require_write)])
async def update_contact(contact_id: str, update: CustomerContactUpdate):
    """Update an existing contact."""
    existing = query(
        "SELECT * FROM sale_customer_contacts WHERE id = ?",
        [contact_id],
        one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Contact not found")

    sets = []
    params: list = []
    data = update.model_dump(exclude_unset=True) if hasattr(update, "model_dump") else update.dict(exclude_unset=True)

    for field, value in data.items():
        if field == "is_primary":
            if value:
                execute(
                    "UPDATE sale_customer_contacts SET is_primary = 0 "
                    "WHERE customer_id = ? AND id != ?",
                    [existing["customer_id"], contact_id],
                )
            sets.append("is_primary = ?")
            params.append(1 if value else 0)
        else:
            sets.append(f"{field} = ?")
            params.append(value)

    if not sets:
        raise HTTPException(status_code=400, detail="No fields to update")

    params.append(contact_id)
    execute(
        f"UPDATE sale_customer_contacts SET {', '.join(sets)} WHERE id = ?",
        params,
    )

    return {"id": contact_id, "status": "ok"}
