"""
Customers Router
Manages customer data, search, and customer details with contacts and opportunities.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from ..database import query, execute
from datetime import datetime
import uuid

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
    q: str = Query(..., description="Search query (name, code, or email)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    Search customers by name, code, or email using LIKE query.
    
    Args:
        q: Search query string
        limit: Number of results to return (1-200)
        offset: Number of results to skip
        
    Returns:
        dict: Total count, items list, limit, and offset
    """
    search_param = f"%{q}%"
    
    total = query("""
        SELECT COUNT(*) as cnt FROM sale_customers
        WHERE customer_name LIKE ? OR customer_code LIKE ? OR email LIKE ?
    """, [search_param, search_param, search_param])[0]["cnt"]
    
    items = query("""
        SELECT * FROM sale_customers
        WHERE customer_name LIKE ? OR customer_code LIKE ? OR email LIKE ?
        ORDER BY customer_name ASC
        LIMIT ? OFFSET ?
    """, [search_param, search_param, search_param, limit, offset])
    
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/{customer_id}")
async def get_customer_detail(customer_id: str):
    """
    Get customer detail with associated contacts and opportunities.
    
    Args:
        customer_id: Customer ID (UUID)
        
    Returns:
        dict: Customer detail with nested contacts and opportunities
        
    Raises:
        HTTPException: 404 if customer not found
    """
    customer = query(
        "SELECT * FROM sale_customers WHERE id = ?",
        [customer_id],
        one=True
    )
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    contacts = query(
        "SELECT * FROM sale_customer_contacts WHERE customer_id = ? ORDER BY created_at DESC",
        [customer_id]
    )
    
    opportunities = query(
        "SELECT * FROM sale_opportunities WHERE customer_id = ? ORDER BY created_at DESC",
        [customer_id]
    )
    
    return {
        "customer": dict(customer),
        "contacts": contacts,
        "opportunities": opportunities,
    }
