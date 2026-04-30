"""Contracts Router — Milestones, Settlements, Change Orders.

Read-only browsing for now. Writes flow through opportunities.py PATCH or
dedicated milestone-update endpoints (Sprint 2).
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional

import structlog

try:
    from ..database import query
except ImportError:
    from database import query

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/contracts", tags=["Contracts"])


# ═══════════════════════════════════════════════════════════════
# Milestones — sale_contract_milestones (55 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/milestones")
async def list_milestones(
    opportunity_id: Optional[str] = Query(None),
    invoice_status: Optional[str] = Query(None, description="NOT_INVOICED, INVOICED, PAID, OVERDUE, etc."),
    milestone_type: Optional[str] = Query(None),
    overdue_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List contract milestones across all opportunities."""
    where = []
    params: list = []
    if opportunity_id:
        where.append("m.opportunity_id = ?")
        params.append(opportunity_id)
    if invoice_status:
        where.append("m.invoice_status = ?")
        params.append(invoice_status)
    if milestone_type:
        where.append("m.milestone_type = ?")
        params.append(milestone_type)
    if overdue_only:
        where.append("m.overdue_days > 0")
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_contract_milestones m WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT m.*, o.project_name, o.customer_name
        FROM sale_contract_milestones m
        LEFT JOIN sale_opportunities o ON o.id = m.opportunity_id
        WHERE {where_sql}
        ORDER BY m.overdue_days DESC, m.planned_date ASC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/milestones/{milestone_id}")
async def get_milestone(milestone_id: str):
    """Get a single milestone with its parent opportunity."""
    item = query(
        """
        SELECT m.*, o.project_name, o.customer_name, o.product_group, o.stage
        FROM sale_contract_milestones m
        LEFT JOIN sale_opportunities o ON o.id = m.opportunity_id
        WHERE m.id = ?
        """,
        [milestone_id],
        one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return {"milestone": dict(item)}


# ═══════════════════════════════════════════════════════════════
# Settlements — sale_settlements (32 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/settlements")
async def list_settlements(
    settlement_status: Optional[str] = Query(None, description="OPEN, IN_REVIEW, APPROVED, CLOSED"),
    opportunity_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List settlements (post-project P&L close-out)."""
    where = []
    params: list = []
    if settlement_status:
        where.append("s.settlement_status = ?")
        params.append(settlement_status)
    if opportunity_id:
        where.append("s.opportunity_id = ?")
        params.append(opportunity_id)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_settlements s WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT s.*, o.project_name, o.customer_name
        FROM sale_settlements s
        LEFT JOIN sale_opportunities o ON o.id = s.opportunity_id
        WHERE {where_sql}
        ORDER BY s.settlement_date DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/settlements/{settlement_id}")
async def get_settlement(settlement_id: str):
    """Get a single settlement."""
    item = query(
        """
        SELECT s.*, o.project_name, o.customer_name
        FROM sale_settlements s
        LEFT JOIN sale_opportunities o ON o.id = s.opportunity_id
        WHERE s.id = ?
        """,
        [settlement_id],
        one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Settlement not found")
    return {"settlement": dict(item)}


# ═══════════════════════════════════════════════════════════════
# Change Orders — sale_change_orders
# ═══════════════════════════════════════════════════════════════

@router.get("/change-orders")
async def list_change_orders(
    opportunity_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None, description="DRAFT, SUBMITTED, APPROVED, REJECTED, IMPLEMENTED"),
    change_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List change orders against existing contracts."""
    where = []
    params: list = []
    if opportunity_id:
        where.append("co.opportunity_id = ?")
        params.append(opportunity_id)
    if status:
        where.append("co.status = ?")
        params.append(status)
    if change_type:
        where.append("co.change_type = ?")
        params.append(change_type)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_change_orders co WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT co.*, o.project_name, o.customer_name
        FROM sale_change_orders co
        LEFT JOIN sale_opportunities o ON o.id = co.opportunity_id
        WHERE {where_sql}
        ORDER BY co.request_date DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


# ═══════════════════════════════════════════════════════════════
# KHKD targets — sale_khkd_targets
# ═══════════════════════════════════════════════════════════════

@router.get("/khkd-targets")
async def list_khkd_targets():
    """All KHKD fiscal-year targets (revenue/tons/GM/PO baseline)."""
    items = query(
        "SELECT * FROM sale_khkd_targets ORDER BY fiscal_year DESC"
    )
    return {"items": items, "count": len(items)}
