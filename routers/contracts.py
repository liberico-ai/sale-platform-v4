"""Contracts Router — Active Contracts, Milestones, Settlements, Change Orders.

Reads are gated by router-level auth_dep. Writes (POST/PATCH) require
write tier per-route.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel

import structlog

try:
    from ..database import query, execute
    from ..auth import UserContext, get_current_writer
    from ..services.audit import log_status_change, log_financial_change
except ImportError:
    from database import query, execute
    from auth import UserContext, get_current_writer
    from services.audit import log_status_change, log_financial_change

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/contracts", tags=["Contracts"])


# ═══════════════════════════════════════════════════════════════
# Pydantic models — local to this router
# ═══════════════════════════════════════════════════════════════

class ActiveContractCreate(BaseModel):
    """New active contract.

    Required: po_number + customer info (customer_id or customer_name).
    Optional quotation_id auto-fills project_name + product_type from a
    won quotation when supplied.
    """
    po_number: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    project_name: Optional[str] = None
    product_type: Optional[str] = None
    contract_status: Optional[str] = "ACTIVE"
    start_date: Optional[str] = None
    project_manager: Optional[str] = None
    value_notes: Optional[str] = None
    quotation_id: Optional[str] = None
    source: Optional[str] = "API"


class ActiveContractUpdate(BaseModel):
    """Update an active contract. Status changes are audit-logged."""
    customer_name: Optional[str] = None
    project_name: Optional[str] = None
    product_type: Optional[str] = None
    contract_status: Optional[str] = None
    start_date: Optional[str] = None
    latest_activity: Optional[str] = None
    project_manager: Optional[str] = None
    value_notes: Optional[str] = None
    customer_id: Optional[str] = None


class MilestoneCreate(BaseModel):
    """New milestone. opportunity_id required (resolved from contract if
    not supplied — see endpoint docstring).
    """
    milestone_type: str
    title: str
    description: Optional[str] = None
    opportunity_id: Optional[str] = None
    planned_date: Optional[str] = None
    weight_ton: Optional[float] = None
    invoice_amount_usd: Optional[float] = None
    invoice_amount_vnd: Optional[float] = None
    payment_term_days: Optional[int] = None
    nas_contract_path: Optional[str] = None
    notes: Optional[str] = None


class MilestoneUpdate(BaseModel):
    """Update milestone. invoice_status changes are audit-logged."""
    title: Optional[str] = None
    description: Optional[str] = None
    planned_date: Optional[str] = None
    actual_date: Optional[str] = None
    weight_ton: Optional[float] = None
    invoice_amount_usd: Optional[float] = None
    invoice_amount_vnd: Optional[float] = None
    payment_term_days: Optional[int] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_status: Optional[str] = None
    payment_received_date: Optional[str] = None
    payment_amount: Optional[float] = None
    overdue_days: Optional[int] = None
    penalty_amount: Optional[float] = None
    nas_contract_path: Optional[str] = None
    nas_invoice_path: Optional[str] = None
    notes: Optional[str] = None


class SettlementCreate(BaseModel):
    """New settlement (post-project P&L close-out).

    opportunity_id required (resolved from contract if not supplied).
    sale_settlements has UNIQUE(opportunity_id) — only one settlement
    per opportunity allowed.
    """
    opportunity_id: Optional[str] = None
    settlement_date: Optional[str] = None
    settlement_status: Optional[str] = "OPEN"
    planned_value_usd: Optional[float] = None
    planned_weight_ton: Optional[float] = None
    planned_gm_pct: Optional[float] = None
    planned_gm_value: Optional[float] = None
    actual_revenue_usd: Optional[float] = None
    actual_weight_ton: Optional[float] = None
    actual_total_cost: Optional[float] = None
    actual_gm_pct: Optional[float] = None
    actual_gm_value: Optional[float] = None
    notes: Optional[str] = None


_AUDITED_CONTRACT_FIELDS = {"contract_status"}
_AUDITED_MILESTONE_FIELDS = {
    "invoice_status", "invoice_amount_usd", "payment_amount",
}


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


# ═══════════════════════════════════════════════════════════════
# Writes — POST / PATCH for contracts, milestones, settlements
# ═══════════════════════════════════════════════════════════════

def _resolve_opp_for_contract(contract: dict) -> Optional[str]:
    """Pick the single best-fit opportunity for a contract — None if 0 or many."""
    opps = _resolve_contract_opportunities(contract)
    return opps[0]["id"] if len(opps) == 1 else None


@router.post("")
async def create_active_contract(
    payload: ActiveContractCreate,
    user: UserContext = Depends(get_current_writer),
):
    """Create a new active contract.

    If `quotation_id` is supplied, project_name + product_type + customer
    info are auto-filled from the won quotation when not explicitly set.
    """
    customer_id = payload.customer_id
    customer_name = payload.customer_name
    project_name = payload.project_name
    product_type = payload.product_type

    if payload.quotation_id:
        quote = query(
            "SELECT * FROM sale_quotation_history WHERE id = ?",
            [payload.quotation_id],
            one=True,
        )
        if not quote:
            raise HTTPException(status_code=404, detail="Quotation not found")
        # Status is informational — we won't block creation if not WON,
        # but we do log it.
        if (quote.get("status") or "").upper() != "WON":
            logger.warning(
                "contract_from_non_won_quotation",
                quotation_id=payload.quotation_id,
                quotation_status=quote.get("status"),
            )
        customer_id = customer_id or quote.get("customer_id")
        customer_name = customer_name or quote.get("customer_name")
        project_name = project_name or quote.get("project_name")
        product_type = product_type or quote.get("product_type")

    if customer_id:
        cust = query(
            "SELECT id, name FROM sale_customers WHERE id = ?",
            [customer_id],
            one=True,
        )
        if not cust:
            raise HTTPException(status_code=404, detail="Customer not found")
        customer_name = customer_name or cust.get("name")

    if not customer_name:
        raise HTTPException(
            status_code=400,
            detail="customer_name (or customer_id, or quotation_id) required",
        )

    contract_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute(
        """
        INSERT INTO sale_active_contracts
            (id, po_number, customer_name, project_name, product_type,
             contract_status, start_date, latest_activity, value_notes,
             project_manager, customer_id, source, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            contract_id, payload.po_number, customer_name, project_name,
            product_type, payload.contract_status or "ACTIVE",
            payload.start_date, now[:10], payload.value_notes,
            payload.project_manager, customer_id,
            payload.source or "API", now, now,
        ],
    )

    logger.info(
        "contract_created",
        contract_id=contract_id,
        po_number=payload.po_number,
        customer_name=customer_name,
    )

    return {
        "id": contract_id,
        "po_number": payload.po_number,
        "status": payload.contract_status or "ACTIVE",
        "message": f"Contract created: {payload.po_number}",
    }


@router.patch("/{contract_id}")
async def update_active_contract(
    contract_id: str,
    payload: ActiveContractUpdate,
    user: UserContext = Depends(get_current_writer),
):
    """Update an active contract. Status changes are audit-logged."""
    existing = query(
        "SELECT * FROM sale_active_contracts WHERE id = ?",
        [contract_id],
        one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Contract not found")

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    if (
        "contract_status" in data
        and data["contract_status"] != existing.get("contract_status")
    ):
        log_status_change(
            "active_contract", contract_id,
            existing.get("contract_status") or "",
            data["contract_status"],
            changed_by=user.actor,
        )

    now = datetime.now().isoformat()
    sets = [f"{k} = ?" for k in data.keys()]
    sets.extend(["latest_activity = ?", "updated_at = ?"])
    params = list(data.values()) + [now[:10], now, contract_id]

    execute(
        f"UPDATE sale_active_contracts SET {', '.join(sets)} WHERE id = ?",
        params,
    )

    return {"id": contract_id, "status": "ok",
            "updated_fields": list(data.keys())}


@router.post("/{contract_id}/milestones")
async def create_milestone(
    contract_id: str,
    payload: MilestoneCreate,
    user: UserContext = Depends(get_current_writer),
):
    """Create a new milestone for an active contract.

    Milestones are FK'd to sale_opportunities (not sale_active_contracts).
    Resolution order for opportunity_id:
      1. payload.opportunity_id (explicit)
      2. unique opportunity matching contract's customer_id + project_name
      3. error 400 if neither resolves
    """
    contract = query(
        "SELECT * FROM sale_active_contracts WHERE id = ?",
        [contract_id],
        one=True,
    )
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    opportunity_id = payload.opportunity_id or _resolve_opp_for_contract(dict(contract))
    if not opportunity_id:
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not resolve opportunity_id from contract — pass it "
                "explicitly in the request body"
            ),
        )

    # Next milestone_number for this opportunity (UNIQUE(opp_id, num))
    next_row = query(
        "SELECT COALESCE(MAX(milestone_number), 0) + 1 AS n "
        "FROM sale_contract_milestones WHERE opportunity_id = ?",
        [opportunity_id],
        one=True,
    ) or {}
    next_num = int(next_row.get("n") or 1)

    milestone_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute(
        """
        INSERT INTO sale_contract_milestones
            (id, opportunity_id, milestone_number, milestone_type, title,
             description, planned_date, weight_ton,
             invoice_amount_usd, invoice_amount_vnd, payment_term_days,
             invoice_status, nas_contract_path, notes,
             created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'NOT_INVOICED', ?, ?, ?, ?)
        """,
        [
            milestone_id, opportunity_id, next_num, payload.milestone_type,
            payload.title, payload.description, payload.planned_date,
            payload.weight_ton, payload.invoice_amount_usd,
            payload.invoice_amount_vnd, payload.payment_term_days,
            payload.nas_contract_path, payload.notes, now, now,
        ],
    )

    logger.info(
        "milestone_created",
        milestone_id=milestone_id,
        contract_id=contract_id,
        opportunity_id=opportunity_id,
        milestone_number=next_num,
    )

    return {
        "id": milestone_id,
        "opportunity_id": opportunity_id,
        "milestone_number": next_num,
        "status": "ok",
    }


@router.patch("/{contract_id}/milestones/{milestone_id}")
async def update_milestone(
    contract_id: str,
    milestone_id: str,
    payload: MilestoneUpdate,
    user: UserContext = Depends(get_current_writer),
):
    """Update a milestone. invoice_status / financial fields are audit-logged.

    contract_id is informational — the milestone resolves by milestone_id.
    """
    existing = query(
        "SELECT * FROM sale_contract_milestones WHERE id = ?",
        [milestone_id],
        one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Milestone not found")

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    if (
        "invoice_status" in data
        and data["invoice_status"] != existing.get("invoice_status")
    ):
        log_status_change(
            "milestone", milestone_id,
            existing.get("invoice_status") or "",
            data["invoice_status"],
            changed_by=user.actor,
        )

    financial_diffs = {}
    for field in _AUDITED_MILESTONE_FIELDS:
        if (
            field in data
            and field != "invoice_status"
            and data[field] != existing.get(field)
        ):
            financial_diffs[field] = (existing.get(field), data[field])
    if financial_diffs:
        log_financial_change(
            "milestone", milestone_id, financial_diffs,
            changed_by=user.actor,
        )

    now = datetime.now().isoformat()
    sets = [f"{k} = ?" for k in data.keys()]
    sets.append("updated_at = ?")
    params = list(data.values()) + [now, milestone_id]

    execute(
        f"UPDATE sale_contract_milestones SET {', '.join(sets)} WHERE id = ?",
        params,
    )

    return {"id": milestone_id, "status": "ok",
            "updated_fields": list(data.keys())}


@router.post("/{contract_id}/settlements")
async def create_settlement(
    contract_id: str,
    payload: SettlementCreate,
    user: UserContext = Depends(get_current_writer),
):
    """Create the settlement for a contract.

    sale_settlements has UNIQUE(opportunity_id) — only one per opportunity.
    Returns 409 if a settlement already exists.
    """
    contract = query(
        "SELECT * FROM sale_active_contracts WHERE id = ?",
        [contract_id],
        one=True,
    )
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    opportunity_id = payload.opportunity_id or _resolve_opp_for_contract(dict(contract))
    if not opportunity_id:
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not resolve opportunity_id from contract — pass it "
                "explicitly in the request body"
            ),
        )

    existing_settlement = query(
        "SELECT id FROM sale_settlements WHERE opportunity_id = ?",
        [opportunity_id],
        one=True,
    )
    if existing_settlement:
        raise HTTPException(
            status_code=409,
            detail=f"Settlement already exists for opportunity {opportunity_id}",
        )

    settlement_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute(
        """
        INSERT INTO sale_settlements
            (id, opportunity_id, settlement_date, settlement_status,
             planned_value_usd, planned_weight_ton, planned_gm_pct, planned_gm_value,
             actual_revenue_usd, actual_weight_ton, actual_total_cost,
             actual_gm_pct, actual_gm_value, notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            settlement_id, opportunity_id, payload.settlement_date or now[:10],
            payload.settlement_status or "OPEN",
            payload.planned_value_usd, payload.planned_weight_ton,
            payload.planned_gm_pct, payload.planned_gm_value,
            payload.actual_revenue_usd, payload.actual_weight_ton,
            payload.actual_total_cost, payload.actual_gm_pct,
            payload.actual_gm_value, payload.notes, now, now,
        ],
    )

    logger.info(
        "settlement_created",
        settlement_id=settlement_id,
        contract_id=contract_id,
        opportunity_id=opportunity_id,
    )

    return {
        "id": settlement_id,
        "opportunity_id": opportunity_id,
        "status": "ok",
    }
