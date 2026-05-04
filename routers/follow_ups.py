"""Follow-ups Router — sale_follow_up_schedules.

Schema constraint: opportunity_id is NOT NULL FK. Every follow-up has to
be tied to an opportunity — for customer-only follow-ups use the
sale_customer_interactions.next_action_due field instead.

Status values: PENDING | DONE | CANCELLED | RESCHEDULED.
RESCHEDULED + new next_follow_up auto-creates a new PENDING follow-up.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

import structlog

try:
    from ..database import query, execute, now_expr, date_today_expr
    from ..auth import (
        UserContext, require_write, get_current_writer, get_current_admin,
    )
    from ..errors import EntityNotFoundError
    from ..services.audit import log_status_change
    from ..services.state_machine import (
        validate_follow_up_transition,
        get_allowed_follow_up_transitions,
        InvalidTransitionError,
    )
except ImportError:
    from database import query, execute, now_expr, date_today_expr
    from auth import (
        UserContext, require_write, get_current_writer, get_current_admin,
    )
    from errors import EntityNotFoundError
    from services.audit import log_status_change
    from services.state_machine import (
        validate_follow_up_transition,
        get_allowed_follow_up_transitions,
        InvalidTransitionError,
    )

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/follow-ups", tags=["Follow-ups"])


class FollowUpCreate(BaseModel):
    """New follow-up.

    ``opportunity_id`` is required because the underlying schema
    enforces NOT NULL on it (sale_follow_up_schedules.opportunity_id
    REFERENCES sale_opportunities). Customer-only follow-ups are a
    Phase 3 item — they need a schema migration that SQLite ALTER
    cannot express in a backward-compatible way.
    """
    opportunity_id: str
    schedule_type: str               # CALL | EMAIL | VISIT | MEETING | REMINDER
    next_follow_up: str              # ISO date / datetime — when to act
    customer_id: Optional[str] = None
    contact_id: Optional[str] = None
    assigned_to: Optional[str] = None
    reminder_days: Optional[str] = None    # "3,7,14" — days before next_follow_up
    notes: Optional[str] = None


class FollowUpUpdate(BaseModel):
    """Update follow-up. Setting status=RESCHEDULED + new next_follow_up
    auto-creates a fresh PENDING follow-up.
    """
    status: Optional[str] = None
    schedule_type: Optional[str] = None
    next_follow_up: Optional[str] = None
    last_follow_up: Optional[str] = None
    assigned_to: Optional[str] = None
    contact_id: Optional[str] = None
    outcome: Optional[str] = None
    notes: Optional[str] = None


def _build_where(filters: dict) -> tuple:
    where = []
    params: list = []
    for k, v in filters.items():
        if v is None:
            continue
        if k == "overdue_only":
            if v:
                where.append(f"(status = 'PENDING' AND next_follow_up < {now_expr()})")
            continue
        if k == "due_today":
            if v:
                where.append(f"(status = 'PENDING' AND date(next_follow_up) = {date_today_expr()})")
            continue
        where.append(f"{k} = ?")
        params.append(v)
    return (" AND ".join(where) if where else "1=1"), params


@router.get("")
async def list_follow_ups(
    assigned_to: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
    opportunity_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None, description="PENDING, DONE, CANCELLED, RESCHEDULED"),
    schedule_type: Optional[str] = Query(None),
    overdue_only: bool = Query(False),
    due_today: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List follow-ups, ordered by next_follow_up ASC (soonest first)."""
    where_sql, params = _build_where({
        "assigned_to": assigned_to,
        "customer_id": customer_id,
        "opportunity_id": opportunity_id,
        "status": status,
        "schedule_type": schedule_type,
        "overdue_only": overdue_only,
        "due_today": due_today,
    })

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_follow_up_schedules WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT f.*, o.project_name, c.name AS customer_name
        FROM sale_follow_up_schedules f
        LEFT JOIN sale_opportunities o ON o.id = f.opportunity_id
        LEFT JOIN sale_customers c ON c.id = f.customer_id
        WHERE {where_sql}
        ORDER BY f.next_follow_up ASC, f.created_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/overdue")
async def list_overdue_followups(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Follow-ups with next_follow_up < now AND status = PENDING."""
    total = query(
        """
        SELECT COUNT(*) AS cnt
        FROM sale_follow_up_schedules f
        WHERE f.status = 'PENDING' AND f.next_follow_up < """ + now_expr() + """
        """
    )[0]["cnt"]

    items = query(
        """
        SELECT f.*, o.project_name, c.name AS customer_name
        FROM sale_follow_up_schedules f
        LEFT JOIN sale_opportunities o ON o.id = f.opportunity_id
        LEFT JOIN sale_customers c ON c.id = f.customer_id
        WHERE f.status = 'PENDING' AND f.next_follow_up < """ + now_expr() + """
        ORDER BY f.next_follow_up ASC
        LIMIT ? OFFSET ?
        """,
        [limit, offset],
    )
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/{follow_up_id}")
async def get_follow_up_detail(follow_up_id: str):
    """Detailed view of a single follow-up (Phase 2 step 7).

    Joins the linked opportunity, customer, and contact so the SPA's
    detail drawer renders parent context in one round-trip.
    """
    item = query(
        """
        SELECT f.*,
               o.project_name AS opportunity_project,
               o.stage AS opportunity_stage,
               c.name AS customer_name,
               c.code AS customer_code,
               ct.name AS contact_name,
               ct.email AS contact_email
        FROM sale_follow_up_schedules f
        LEFT JOIN sale_opportunities o ON o.id = f.opportunity_id
        LEFT JOIN sale_customers c ON c.id = f.customer_id
        LEFT JOIN sale_customer_contacts ct ON ct.id = f.contact_id
        WHERE f.id = ?
        """,
        [follow_up_id], one=True,
    )
    if not item:
        raise EntityNotFoundError("FollowUp", follow_up_id)

    allowed_next = get_allowed_follow_up_transitions(
        item.get("status") or "PENDING"
    )
    return {
        "follow_up": dict(item),
        "allowed_next_statuses": allowed_next,
    }


@router.post("")
async def create_follow_up(
    payload: FollowUpCreate,
    user: UserContext = Depends(get_current_writer),
):
    """Create a new follow-up. opportunity_id required (NOT NULL FK)."""
    opp = query(
        "SELECT id, customer_id FROM sale_opportunities WHERE id = ?",
        [payload.opportunity_id],
        one=True,
    )
    if not opp:
        raise EntityNotFoundError("Opportunity", payload.opportunity_id)

    # Auto-fill customer_id from opportunity when caller leaves it blank
    customer_id = payload.customer_id or opp.get("customer_id")

    follow_up_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute(
        """
        INSERT INTO sale_follow_up_schedules
            (id, opportunity_id, customer_id, contact_id, schedule_type,
             reminder_days, next_follow_up, follow_up_count, is_active,
             status, assigned_to, notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, 1, 'PENDING', ?, ?, ?, ?)
        """,
        [
            follow_up_id, payload.opportunity_id, customer_id,
            payload.contact_id, payload.schedule_type, payload.reminder_days,
            payload.next_follow_up, payload.assigned_to, payload.notes,
            now, now,
        ],
    )

    logger.info(
        "followup_created",
        follow_up_id=follow_up_id,
        opportunity_id=payload.opportunity_id,
        next_follow_up=payload.next_follow_up,
    )

    return {
        "id": follow_up_id,
        "status": "PENDING",
        "message": f"Follow-up scheduled for {payload.next_follow_up}",
    }


@router.patch("/{follow_up_id}")
async def update_follow_up(
    follow_up_id: str,
    payload: FollowUpUpdate,
    user: UserContext = Depends(get_current_writer),
):
    """Update follow-up.

    status changes go through the follow-up state machine. RESCHEDULED +
    new next_follow_up auto-spawns a fresh PENDING row with the new date.
    """
    existing = query(
        "SELECT * FROM sale_follow_up_schedules WHERE id = ?",
        [follow_up_id],
        one=True,
    )
    if not existing:
        raise EntityNotFoundError("Follow-up", follow_up_id)

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    # State machine — reject illegal transitions before mutation.
    new_status = data.get("status")
    current_status = existing.get("status") or "PENDING"
    if new_status and new_status != current_status:
        try:
            validate_follow_up_transition(current_status, new_status)
        except InvalidTransitionError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        log_status_change(
            "follow_up", follow_up_id,
            current_status, new_status,
            changed_by=user.actor,
        )
        # Stamp last_follow_up when a PENDING row moves on.
        if current_status == "PENDING":
            data["last_follow_up"] = (
                data.get("last_follow_up") or datetime.now().isoformat()
            )

    now = datetime.now().isoformat()
    sets = [f"{k} = ?" for k in data.keys()]
    sets.append("updated_at = ?")
    params = list(data.values()) + [now, follow_up_id]

    execute(
        f"UPDATE sale_follow_up_schedules SET {', '.join(sets)} WHERE id = ?",
        params,
    )

    # If RESCHEDULED + new next_follow_up, spawn a fresh PENDING follow-up
    spawned_id = None
    if (
        new_status == "RESCHEDULED"
        and data.get("next_follow_up")
    ):
        spawned_id = str(uuid.uuid4())
        execute(
            """
            INSERT INTO sale_follow_up_schedules
                (id, opportunity_id, customer_id, contact_id, schedule_type,
                 reminder_days, next_follow_up, follow_up_count, is_active,
                 status, assigned_to, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 'PENDING', ?, ?, ?, ?)
            """,
            [
                spawned_id, existing["opportunity_id"], existing.get("customer_id"),
                existing.get("contact_id"), existing.get("schedule_type"),
                existing.get("reminder_days"), data["next_follow_up"],
                (existing.get("follow_up_count") or 0) + 1,
                existing.get("assigned_to"), existing.get("notes"),
                now, now,
            ],
        )

    return {
        "id": follow_up_id,
        "status": "ok",
        "spawned_follow_up_id": spawned_id,
        "updated_fields": list(data.keys()),
    }


@router.delete("/{follow_up_id}")
async def soft_delete_follow_up(
    follow_up_id: str,
    user: UserContext = Depends(get_current_writer),
):
    """Soft-delete a follow-up: set status='CANCELLED'. Writer tier OK
    because follow-ups are routinely re-scheduled or dropped by the
    person who owns the customer.
    """
    existing = query(
        "SELECT id, status FROM sale_follow_up_schedules WHERE id = ?",
        [follow_up_id], one=True,
    )
    if not existing:
        raise EntityNotFoundError("FollowUp", follow_up_id)

    if existing.get("status") == "CANCELLED":
        return {"id": follow_up_id, "status": "already_cancelled"}

    # Use the state machine — most non-terminal states allow CANCELLED.
    try:
        validate_follow_up_transition(
            existing.get("status") or "PENDING", "CANCELLED",
        )
    except InvalidTransitionError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    now = datetime.now().isoformat()
    execute(
        """
        UPDATE sale_follow_up_schedules
        SET status = 'CANCELLED', is_active = 0, updated_at = ?
        WHERE id = ?
        """,
        [now, follow_up_id],
    )
    log_status_change(
        "follow_up", follow_up_id,
        existing.get("status") or "", "CANCELLED",
        changed_by=user.actor,
    )
    return {"id": follow_up_id, "status": "cancelled"}
