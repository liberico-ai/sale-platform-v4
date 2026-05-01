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
    from ..database import query, execute
    from ..auth import require_write
except ImportError:
    from database import query, execute
    from auth import require_write

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/follow-ups", tags=["Follow-ups"])


class FollowUpCreate(BaseModel):
    """New follow-up. Required: opportunity_id, schedule_type, next_follow_up."""
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
                where.append("(status = 'PENDING' AND next_follow_up < datetime('now'))")
            continue
        if k == "due_today":
            if v:
                where.append("(status = 'PENDING' AND date(next_follow_up) = date('now'))")
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
async def list_overdue_followups(limit: int = Query(50, ge=1, le=200)):
    """Follow-ups with next_follow_up < now AND status = PENDING."""
    items = query(
        """
        SELECT f.*, o.project_name, c.name AS customer_name
        FROM sale_follow_up_schedules f
        LEFT JOIN sale_opportunities o ON o.id = f.opportunity_id
        LEFT JOIN sale_customers c ON c.id = f.customer_id
        WHERE f.status = 'PENDING' AND f.next_follow_up < datetime('now')
        ORDER BY f.next_follow_up ASC
        LIMIT ?
        """,
        [limit],
    )
    return {"items": items, "count": len(items)}


@router.post("", dependencies=[Depends(require_write)])
async def create_follow_up(payload: FollowUpCreate):
    """Create a new follow-up. opportunity_id must point to an existing
    opportunity (NOT NULL FK).
    """
    opp = query(
        "SELECT id, customer_id FROM sale_opportunities WHERE id = ?",
        [payload.opportunity_id],
        one=True,
    )
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

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


@router.patch("/{follow_up_id}", dependencies=[Depends(require_write)])
async def update_follow_up(follow_up_id: str, payload: FollowUpUpdate):
    """Update follow-up.

    status=DONE/CANCELLED → terminal.
    status=RESCHEDULED + next_follow_up → terminal on this row + auto-creates
    a new PENDING follow-up with the new date.
    """
    existing = query(
        "SELECT * FROM sale_follow_up_schedules WHERE id = ?",
        [follow_up_id],
        one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Follow-up not found")

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Auto-bump follow_up_count when transitioning out of PENDING
    new_status = data.get("status")
    if (
        new_status
        and new_status != existing.get("status")
        and existing.get("status") == "PENDING"
    ):
        data["last_follow_up"] = data.get("last_follow_up") or datetime.now().isoformat()

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
