"""Opportunities Router — Sales pipeline management.

Manages creation, updates, stale deal tracking, with state machine
validation for stage transitions and audit logging for financial changes.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import json
import uuid

import structlog

try:
    from ..database import query, execute
    from ..auth import UserContext, get_current_writer, get_current_admin
    from ..errors import EntityNotFoundError
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
    from auth import UserContext, get_current_writer, get_current_admin
    from errors import EntityNotFoundError
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
async def create_opportunity(
    opp: OpportunityCreate,
    user: UserContext = Depends(get_current_writer),
):
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
async def update_opportunity(
    opp_id: str,
    update: OpportunityUpdate,
    user: UserContext = Depends(get_current_writer),
):
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
        log_status_change(
            "opportunity", opp_id, current_stage, update.stage,
            changed_by=user.actor,
        )

        logger.info("opportunity_stage_changed",
                     opp_id=opp_id,
                     from_stage=current_stage,
                     to_stage=update.stage)

        # Follow-up schedule management
        if update.stage == "QUOTED":
            # Create post-quotation follow-up schedule (INSERT OR IGNORE for idempotency)
            schedule_id = str(uuid.uuid4())
            now_ts = datetime.utcnow().isoformat()
            next_follow_up = (datetime.utcnow() + timedelta(days=3)).isoformat()
            reminder_days_json = json.dumps([3, 7, 14, 30])
            execute("""
                INSERT OR IGNORE INTO sale_follow_up_schedules
                    (id, opportunity_id, schedule_type, reminder_days,
                     next_follow_up, follow_up_count, is_active,
                     created_at)
                VALUES (?, ?, 'POST_QUOTATION', ?, ?, 0, 1, ?)
            """, [
                schedule_id, opp_id, reminder_days_json,
                next_follow_up, now_ts,
            ])
            logger.info("followup_schedule_created",
                         opp_id=opp_id, schedule_type="POST_QUOTATION")

        elif update.stage in ("WON", "LOST", "IN_PROGRESS"):
            # Deactivate any active follow-up schedules
            execute("""
                UPDATE sale_follow_up_schedules
                SET is_active = 0
                WHERE opportunity_id = ? AND is_active = 1
            """, [opp_id])
            logger.info("followup_schedules_deactivated",
                         opp_id=opp_id, reason=f"stage_changed_to_{update.stage}")

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
        log_financial_change(
            "opportunity", opp_id, financial_changes,
            changed_by=user.actor,
        )

    # Return current stage and allowed next transitions
    current_stage = update.stage or existing.get("stage", "PROSPECT")
    allowed_next = get_allowed_opportunity_transitions(current_stage)

    return {
        "id": opp_id,
        "status": "ok",
        "current_stage": current_stage,
        "allowed_next_stages": allowed_next,
    }


@router.delete("/{opp_id}")
async def soft_delete_opportunity(
    opp_id: str,
    user: UserContext = Depends(get_current_admin),
):
    """Soft-delete an opportunity: set stage='DELETED'. Admin only.

    Hard delete is unsupported because emails, tasks, follow-ups, and
    audit history reference the opportunity ID.
    """
    existing = query(
        "SELECT id, stage FROM sale_opportunities WHERE id = ?",
        [opp_id], one=True,
    )
    if not existing:
        raise EntityNotFoundError("Opportunity", opp_id)

    if existing.get("stage") == "DELETED":
        return {"id": opp_id, "status": "already_deleted"}

    now_iso = datetime.now().isoformat()
    execute(
        "UPDATE sale_opportunities SET stage = 'DELETED', updated_at = ? "
        "WHERE id = ?",
        [now_iso, opp_id],
    )

    log_status_change(
        "opportunity", opp_id,
        existing.get("stage") or "", "DELETED",
        changed_by=user.actor,
    )

    logger.info("opportunity_soft_deleted", opp_id=opp_id)
    return {"id": opp_id, "status": "deleted"}


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


# Quotation history, active contracts, and per-opportunity revisions
# moved to dedicated routers /quotations and /contracts. Use:
#   GET /quotations?customer_code=X
#   GET /contracts (sale_active_contracts list)
#   GET /quotations/by-opportunity/{opp_id}/revisions
