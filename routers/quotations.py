"""Quotations Router — sale_quotation_history (968) + sale_quotation_revisions (147).

Quotation_history is the historical xlsx import (each row = one quote).
Quotation_revisions belong to a specific opportunity (opp-scoped revisions).
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

import structlog

try:
    from ..database import query
except ImportError:
    from database import query

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/quotations", tags=["Quotations"])


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
