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


# ═══════════════════════════════════════════════════════════════
# Active Contracts — sale_active_contracts (14 records)
# Registered AFTER the literal sub-resources so /milestones, /settlements,
# /change-orders, /khkd-targets win path-matching.
# ═══════════════════════════════════════════════════════════════

@router.get("")
async def list_active_contracts(
    contract_status: Optional[str] = Query(None),
    project_manager: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
    product_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List active contracts (live PO registry)."""
    where = []
    params: list = []
    if contract_status:
        where.append("ac.contract_status = ?")
        params.append(contract_status)
    if project_manager:
        where.append("ac.project_manager = ?")
        params.append(project_manager)
    if customer_id:
        where.append("ac.customer_id = ?")
        params.append(customer_id)
    if product_type:
        where.append("ac.product_type = ?")
        params.append(product_type)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_active_contracts ac WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT ac.*, c.name AS linked_customer_name
        FROM sale_active_contracts ac
        LEFT JOIN sale_customers c ON c.id = ac.customer_id
        WHERE {where_sql}
        ORDER BY ac.latest_activity DESC, ac.start_date DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


def _resolve_contract_opportunities(contract: dict) -> list:
    """Best-effort opportunity lookup for an active contract.

    sale_active_contracts has no FK to sale_opportunities — match on
    customer_id + project_name (case-insensitive LIKE).
    """
    if not contract:
        return []
    customer_id = contract.get("customer_id")
    project_name = contract.get("project_name")
    if not project_name:
        return []
    where = ["LOWER(o.project_name) LIKE LOWER(?)"]
    params: list = [f"%{project_name}%"]
    if customer_id:
        where.append("o.customer_id = ?")
        params.append(customer_id)
    return query(
        f"SELECT o.id, o.project_name, o.stage "
        f"FROM sale_opportunities o "
        f"WHERE {' AND '.join(where)}",
        params,
    )


@router.get("/{contract_id}")
async def get_active_contract(contract_id: str):
    """Active contract detail with best-effort milestone + settlement join."""
    contract = query(
        """
        SELECT ac.*, c.name AS linked_customer_name,
               c.country AS customer_country
        FROM sale_active_contracts ac
        LEFT JOIN sale_customers c ON c.id = ac.customer_id
        WHERE ac.id = ?
        """,
        [contract_id],
        one=True,
    )
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    opps = _resolve_contract_opportunities(dict(contract))
    opp_ids = [o["id"] for o in opps]

    if opp_ids:
        placeholders = ",".join("?" * len(opp_ids))
        milestones = query(
            f"SELECT * FROM sale_contract_milestones "
            f"WHERE opportunity_id IN ({placeholders}) "
            f"ORDER BY milestone_number ASC",
            opp_ids,
        )
        settlements = query(
            f"SELECT * FROM sale_settlements "
            f"WHERE opportunity_id IN ({placeholders})",
            opp_ids,
        )
        change_orders = query(
            f"SELECT * FROM sale_change_orders "
            f"WHERE opportunity_id IN ({placeholders}) "
            f"ORDER BY change_order_number ASC",
            opp_ids,
        )
    else:
        milestones = []
        settlements = []
        change_orders = []

    return {
        "contract": dict(contract),
        "linked_opportunities": opps,
        "milestones": milestones,
        "settlements": settlements,
        "change_orders": change_orders,
    }


@router.get("/{contract_id}/milestones")
async def list_active_contract_milestones(contract_id: str):
    """Milestones associated with an active contract (via project-name match)."""
    contract = query(
        "SELECT * FROM sale_active_contracts WHERE id = ?",
        [contract_id],
        one=True,
    )
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    opps = _resolve_contract_opportunities(dict(contract))
    if not opps:
        return {"contract_id": contract_id, "items": [], "count": 0}

    opp_ids = [o["id"] for o in opps]
    placeholders = ",".join("?" * len(opp_ids))
    items = query(
        f"SELECT * FROM sale_contract_milestones "
        f"WHERE opportunity_id IN ({placeholders}) "
        f"ORDER BY milestone_number ASC",
        opp_ids,
    )
    return {"contract_id": contract_id, "items": items, "count": len(items)}


@router.get("/{contract_id}/settlements")
async def list_active_contract_settlements(contract_id: str):
    """Settlements associated with an active contract (via project-name match)."""
    contract = query(
        "SELECT * FROM sale_active_contracts WHERE id = ?",
        [contract_id],
        one=True,
    )
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    opps = _resolve_contract_opportunities(dict(contract))
    if not opps:
        return {"contract_id": contract_id, "items": [], "count": 0}

    opp_ids = [o["id"] for o in opps]
    placeholders = ",".join("?" * len(opp_ids))
    items = query(
        f"SELECT * FROM sale_settlements "
        f"WHERE opportunity_id IN ({placeholders})",
        opp_ids,
    )
    return {"contract_id": contract_id, "items": items, "count": len(items)}
