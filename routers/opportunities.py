"""Opportunities Router — Sales pipeline management.

Manages creation, updates, stale deal tracking, with state machine
validation for stage transitions and audit logging for financial changes.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

import structlog

try:
    from ..database import query, execute
    from ..services.state_machine import (
        validate_opportunity_transition,
        get_allowed_opportunity_transitions,
        InvalidTransitionError,
    )
    from ..services.audit import (
        log_status_change,
        log_financial_change,
        AUDITED_OPPORTUNITY_FIELDS,
    )
except ImportError:
    from database import query, execute
    from services.state_machine import (
        validate_opportunity_transition,
        get_allowed_opportunity_transitions,
        InvalidTransitionError,
    )
    from services.audit import (
        log_status_change,
        log_financial_change,
        AUDITED_OPPORTUNITY_FIELDS,
    )

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


class OpportunityCreate(BaseModel):
    """Model for creating a new opportunity."""
    customer_id: Optional[str] = None
    project_name: str
    customer_name: str
    product_group: str
    stage: str = "PROSPECT"
    contract_value_usd: Optional[float] = None
    win_probability: int = 50
    estimated_signing: Optional[str] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


class OpportunityUpdate(BaseModel):
    """Model for updating an opportunity."""
    stage: Optional[str] = None
    win_probability: Optional[int] = None
    contract_value_usd: Optional[float] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None


@router.get("")
async def list_opportunities(
    stage: Optional[str] = Query(None, description="Filter by pipeline stage"),
    product_group: Optional[str] = Query(None, description="Filter by product group"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned AM"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List pipeline opportunities with optional filtering.

    Args:
        stage: Optional stage filter.
        product_group: Optional product group filter.
        assigned_to: Optional assigned AM filter.
        limit: Results per page (1-200).
        offset: Number of results to skip.

    Returns:
        Paginated list of opportunities.
    """
    where = []
    params = []

    if stage:
        where.append("stage = ?")
        params.append(stage)
    if product_group:
        where.append("product_group = ?")
        params.append(product_group)
    if assigned_to:
        where.append("assigned_to = ?")
        params.append(assigned_to)

    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_opportunities WHERE {where_sql}",
        params
    )[0]["cnt"]

    items = query(f"""
        SELECT * FROM sale_opportunities
        WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """, params + [limit, offset])

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/stale")
async def get_stale_deals(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Get stale deals (>30 days no activity).

    Args:
        limit: Results per page (1-200).
        offset: Number of results to skip.

    Returns:
        Paginated list of stale opportunities.
    """
    total = query("""
        SELECT COUNT(*) as cnt FROM sale_opportunities
        WHERE stale_flag = 1 OR
              (last_activity_date IS NOT NULL AND
               julianday('now') - julianday(last_activity_date) > 30)
    """)[0]["cnt"]

    items = query("""
        SELECT * FROM sale_opportunities
        WHERE stale_flag = 1 OR
              (last_activity_date IS NOT NULL AND
               julianday('now') - julianday(last_activity_date) > 30)
        ORDER BY last_activity_date ASC
        LIMIT ? OFFSET ?
    """, [limit, offset])

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.post("")
async def create_opportunity(opp: OpportunityCreate):
    """Create a new sales opportunity.

    Args:
        opp: Opportunity creation data.

    Returns:
        Created opportunity ID and status.
    """
    opp_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute("""
        INSERT INTO sale_opportunities
            (id, customer_id, project_name, customer_name, product_group,
             stage, contract_value_usd, win_probability,
             estimated_signing, assigned_to, notes,
             last_activity_date, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        opp_id, opp.customer_id, opp.project_name, opp.customer_name,
        opp.product_group, opp.stage, opp.contract_value_usd,
        opp.win_probability, opp.estimated_signing,
        opp.assigned_to, opp.notes, now, now, now
    ])

    logger.info("opportunity_created",
                opp_id=opp_id,
                project=opp.project_name,
                stage=opp.stage)

    return {"id": opp_id, "status": "ok", "message": f"Opportunity created: {opp.project_name}"}


@router.patch("/{opp_id}")
async def update_opportunity(opp_id: str, update: OpportunityUpdate):
    """Update an existing opportunity with state machine validation.

    Stage changes are validated against allowed transitions.
    Financial field changes are logged to audit trail.

    Args:
        opp_id: Opportunity ID (UUID).
        update: Fields to update.

    Returns:
        Updated opportunity with allowed next stages.

    Raises:
        HTTPException: 404 if not found, 422 if invalid transition.
    """
    existing = query(
        "SELECT * FROM sale_opportunities WHERE id = ?",
        [opp_id],
        one=True
    )

    if not existing:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    sets = []
    params = []
    financial_changes = {}

    # Stage transition with state machine validation
    if update.stage is not None and update.stage != existing.get("stage"):
        current_stage = existing.get("stage", "PROSPECT")
        try:
            validate_opportunity_transition(current_stage, update.stage)
        except InvalidTransitionError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        sets.append("stage = ?")
        params.append(update.stage)

        # Log status change
        log_status_change("opportunity", opp_id, current_stage, update.stage)

        logger.info("opportunity_stage_changed",
                     opp_id=opp_id,
                     from_stage=current_stage,
                     to_stage=update.stage)

    # Financial field: win_probability
    if update.win_probability is not None:
        old_val = existing.get("win_probability")
        if old_val != update.win_probability:
            financial_changes["win_probability"] = (old_val, update.win_probability)
        sets.append("win_probability = ?")
        params.append(update.win_probability)

    # Financial field: contract_value_usd
    if update.contract_value_usd is not None:
        old_val = existing.get("contract_value_usd")
        if old_val != update.contract_value_usd:
            financial_changes["contract_value_usd"] = (old_val, update.contract_value_usd)
        sets.append("contract_value_usd = ?")
        params.append(update.contract_value_usd)

    if update.notes is not None:
        sets.append("notes = ?")
        params.append(update.notes)

    if update.assigned_to is not None:
        old_val = existing.get("assigned_to")
        if old_val != update.assigned_to:
            financial_changes["assigned_to"] = (old_val, update.assigned_to)
        sets.append("assigned_to = ?")
        params.append(update.assigned_to)

    if not sets:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Always update timestamps
    sets.append("updated_at = ?")
    params.append(datetime.now().isoformat())
    sets.append("last_activity_date = ?")
    params.append(datetime.now().isoformat())
    params.append(opp_id)

    execute(f"UPDATE sale_opportunities SET {', '.join(sets)} WHERE id = ?", params)

    # Log financial changes to audit trail
    if financial_changes:
        log_financial_change("opportunity", opp_id, financial_changes)

    # Return current stage and allowed next transitions
    current_stage = update.stage or existing.get("stage", "PROSPECT")
    allowed_next = get_allowed_opportunity_transitions(current_stage)

    return {
        "id": opp_id,
        "status": "ok",
        "current_stage": current_stage,
        "allowed_next_stages": allowed_next,
    }


@router.get("/{opp_id}")
async def get_opportunity_detail(opp_id: str):
    """Get opportunity detail with related emails, tasks, and allowed transitions.

    Args:
        opp_id: Opportunity ID (UUID).

    Returns:
        Opportunity detail with nested emails, tasks, and state machine info.

    Raises:
        HTTPException: 404 if not found.
    """
    opportunity = query(
        "SELECT * FROM sale_opportunities WHERE id = ?",
        [opp_id],
        one=True
    )

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    opp_emails = query(
        "SELECT * FROM sale_emails WHERE opportunity_id = ? ORDER BY created_at DESC",
        [opp_id]
    )

    opp_tasks = query(
        "SELECT * FROM sale_tasks WHERE opportunity_id = ? ORDER BY created_at DESC",
        [opp_id]
    )

    current_stage = opportunity.get("stage", "PROSPECT")
    allowed_next = get_allowed_opportunity_transitions(current_stage)

    revisions = query(
        "SELECT * FROM sale_quotation_revisions WHERE opportunity_id = ? "
        "ORDER BY revision_number DESC",
        [opp_id],
    )

    milestones = query(
        "SELECT * FROM sale_contract_milestones WHERE opportunity_id = ? "
        "ORDER BY milestone_number ASC",
        [opp_id],
    )

    settlement = query(
        "SELECT * FROM sale_settlements WHERE opportunity_id = ?",
        [opp_id],
        one=True,
    )

    return {
        "opportunity": dict(opportunity),
        "emails": opp_emails,
        "tasks": opp_tasks,
        "quotation_revisions": revisions,
        "milestones": milestones,
        "settlement": settlement,
        "allowed_next_stages": allowed_next,
    }


# ═══════════════════════════════════════════════════════════════
# sale_quotation_history — historical quote log (968 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/quotations/history")
async def list_quotation_history(
    customer_code: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    market: Optional[str] = Query(None),
    product_type: Optional[str] = Query(None),
    incharge: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List historical quotations from Quotation Record xlsx import."""
    where = []
    params: list = []
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


# ═══════════════════════════════════════════════════════════════
# sale_active_contracts — live PO/contract registry (14 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/contracts/active")
async def list_active_contracts(
    contract_status: Optional[str] = Query(None),
    project_manager: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List active contracts with running PO references."""
    where = []
    params: list = []
    if contract_status:
        where.append("contract_status = ?")
        params.append(contract_status)
    if project_manager:
        where.append("project_manager = ?")
        params.append(project_manager)
    if customer_id:
        where.append("customer_id = ?")
        params.append(customer_id)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_active_contracts WHERE {where_sql}",
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


@router.get("/{opp_id}/quotation-revisions")
async def list_opportunity_quotation_revisions(opp_id: str):
    """List all quotation revisions for an opportunity (newest first)."""
    items = query(
        """
        SELECT * FROM sale_quotation_revisions
        WHERE opportunity_id = ?
        ORDER BY revision_number DESC
        """,
        [opp_id],
    )
    return {"opportunity_id": opp_id, "items": items, "count": len(items)}
