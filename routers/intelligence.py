"""Intelligence Router — Market Signals & Product-Customer Fit Scores.

Read-only access to AI-derived signals (Z4 in the 4-zone data model).
Writes to these tables come from the AI pipeline, not the API.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional

import structlog

try:
    from ..database import query
except ImportError:
    from database import query

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/intelligence", tags=["Intelligence"])


# ═══════════════════════════════════════════════════════════════
# sale_market_signals — external signals (12 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/signals")
@router.get("/market-signals")
async def list_market_signals(
    signal_type: Optional[str] = Query(None),
    impact_level: Optional[str] = Query(None, description="HIGH, MEDIUM, LOW"),
    region: Optional[str] = Query(None),
    related_product_group: Optional[str] = Query(None),
    actionable_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List market signals (Z4 read-only — AI-curated)."""
    where = []
    params: list = []
    if signal_type:
        where.append("ms.signal_type = ?")
        params.append(signal_type)
    if impact_level:
        where.append("ms.impact_level = ?")
        params.append(impact_level)
    if region:
        where.append("ms.region = ?")
        params.append(region)
    if related_product_group:
        where.append("ms.related_product_group = ?")
        params.append(related_product_group)
    if actionable_only:
        where.append("ms.is_actionable = 1")
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_market_signals ms WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT ms.*, c.name AS related_customer_name
        FROM sale_market_signals ms
        LEFT JOIN sale_customers c ON c.id = ms.related_customer_id
        WHERE {where_sql}
        ORDER BY
            CASE ms.impact_level WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END,
            ms.relevance_score DESC,
            ms.created_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/market-signals/{signal_id}")
async def get_market_signal(signal_id: str):
    """Get a single market signal."""
    item = query(
        """
        SELECT ms.*, c.name AS related_customer_name
        FROM sale_market_signals ms
        LEFT JOIN sale_customers c ON c.id = ms.related_customer_id
        WHERE ms.id = ?
        """,
        [signal_id],
        one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Market signal not found")
    return {"signal": dict(item)}


# ═══════════════════════════════════════════════════════════════
# sale_product_opportunities — fit-score matrix (51 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/products")
@router.get("/product-opportunities")
async def list_product_opportunities(
    customer_id: Optional[str] = Query(None),
    product_category_id: Optional[str] = Query(None),
    capability_status: Optional[str] = Query(None, description="FULL, PARTIAL, GAP"),
    strategic_only: bool = Query(False),
    min_fit_score: Optional[float] = Query(None, ge=0, le=1),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Cross-sell / upsell fit scores between customers and product categories."""
    where = []
    params: list = []
    if customer_id:
        where.append("po.customer_id = ?")
        params.append(customer_id)
    if product_category_id:
        where.append("po.product_category_id = ?")
        params.append(product_category_id)
    if capability_status:
        where.append("po.capability_status = ?")
        params.append(capability_status)
    if strategic_only:
        where.append("po.is_strategic = 1")
    if min_fit_score is not None:
        where.append("po.fit_score >= ?")
        params.append(min_fit_score)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_product_opportunities po WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT po.*,
               c.name AS customer_name,
               pc.code AS product_code,
               pc.name_en AS product_name_en
        FROM sale_product_opportunities po
        LEFT JOIN sale_customers c ON c.id = po.customer_id
        LEFT JOIN sale_product_categories pc ON pc.id = po.product_category_id
        WHERE {where_sql}
        ORDER BY po.is_strategic DESC, po.fit_score DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


# ═══════════════════════════════════════════════════════════════
# sale_digital_content — collateral / case studies (12 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/digital-content")
async def list_digital_content(
    content_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List digital sales collateral indexed for use in customer outreach."""
    where = []
    params: list = []
    if content_type:
        where.append("content_type = ?")
        params.append(content_type)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_digital_content WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT * FROM sale_digital_content
        WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


# ═══════════════════════════════════════════════════════════════
# sale_product_categories — 7 KHKD product groups
# ═══════════════════════════════════════════════════════════════

@router.get("/product-categories")
async def list_product_categories():
    """7 KHKD product groups (HRSG, Diverter, Shipbuilding, PV, Handling, Duct, Other)."""
    items = query(
        "SELECT * FROM sale_product_categories ORDER BY code"
    )
    return {"items": items, "count": len(items)}
