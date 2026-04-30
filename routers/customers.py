"""
Customers Router
Manages customer data, search, and customer details with contacts and opportunities.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime
import uuid

try:
    from ..database import query, execute
except ImportError:
    from database import query, execute

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
    where = []
    params = []
    
    if region:
        where.append("region = ?")
        params.append(region)
    if status:
        where.append("status = ?")
        params.append(status)
    
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
