"""Inter-department Tasks Router — sale_inter_dept_tasks.

Cross-department workflow tasks (Sale → KTKH → KT → QLDA → SX → TCKT etc.).
Each row tracks one step in a multi-step workflow with SLA + escalation.
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
    from ..services.audit import log_status_change
    from ..services.notify import write_notification
except ImportError:
    from database import query, execute
    from auth import require_write
    from services.audit import log_status_change
    from services.notify import write_notification

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/inter-dept", tags=["Inter-Dept"])


# Status flow:
# PENDING → IN_PROGRESS → COMPLETED
#         → REJECTED                 (by reviewer)
#         → CANCELLED                (by sender)
_TRANSITIONS = {
    "PENDING":     {"IN_PROGRESS", "REJECTED", "CANCELLED"},
    "IN_PROGRESS": {"COMPLETED", "REJECTED", "CANCELLED"},
    "COMPLETED":   set(),
    "REJECTED":    {"PENDING"},     # can re-open after revisions
    "CANCELLED":   set(),
}


class InterDeptCreate(BaseModel):
    """New inter-dept task. Required: workflow_type, title, from_dept, to_dept."""
    workflow_type: str               # COST_REVIEW | TECHNICAL_SPEC | DRAWING_APPROVAL | etc.
    title: str
    from_dept: str
    to_dept: str
    description: Optional[str] = None
    task_id: Optional[str] = None
    opportunity_id: Optional[str] = None
    workflow_ref: Optional[str] = None
    from_user: Optional[str] = None
    to_user: Optional[str] = None
    cc_depts: Optional[str] = None       # comma-separated
    step_number: Optional[int] = 1
    total_steps: Optional[int] = 1
    priority: Optional[str] = "NORMAL"
    sla_hours: Optional[int] = None
    due_date: Optional[str] = None
    input_data: Optional[str] = None     # JSON blob
    requires_approval: Optional[bool] = False
    comments: Optional[str] = None


class InterDeptUpdate(BaseModel):
    """Status transitions go through validate_transition."""
    status: Optional[str] = None
    to_user: Optional[str] = None
    output_data: Optional[str] = None
    deliverable_path: Optional[str] = None
    rejection_reason: Optional[str] = None
    comments: Optional[str] = None
    approved_by: Optional[str] = None
    sla_met: Optional[bool] = None


def _validate(current: str, new: str) -> bool:
    cur = (current or "PENDING").upper()
    nxt = (new or "").upper()
    if nxt not in _TRANSITIONS.get(cur, set()):
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid inter-dept transition: {cur} → {nxt}. "
                f"Allowed from {cur}: {sorted(_TRANSITIONS.get(cur, set())) or 'terminal'}"
            ),
        )
    return True


@router.get("")
async def list_inter_dept_tasks(
    status: Optional[str] = Query(None),
    workflow_type: Optional[str] = Query(None),
    from_dept: Optional[str] = Query(None),
    to_dept: Optional[str] = Query(None),
    to_user: Optional[str] = Query(None),
    opportunity_id: Optional[str] = Query(None),
    overdue_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List inter-department tasks."""
    where = []
    params: list = []
    if status:
        where.append("idt.status = ?"); params.append(status)
    if workflow_type:
        where.append("idt.workflow_type = ?"); params.append(workflow_type)
    if from_dept:
        where.append("idt.from_dept = ?"); params.append(from_dept)
    if to_dept:
        where.append("idt.to_dept = ?"); params.append(to_dept)
    if to_user:
        where.append("idt.to_user = ?"); params.append(to_user)
    if opportunity_id:
        where.append("idt.opportunity_id = ?"); params.append(opportunity_id)
    if overdue_only:
        where.append("idt.status IN ('PENDING', 'IN_PROGRESS') AND idt.due_date < datetime('now')")
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_inter_dept_tasks idt WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT idt.*, o.project_name
        FROM sale_inter_dept_tasks idt
        LEFT JOIN sale_opportunities o ON o.id = idt.opportunity_id
        WHERE {where_sql}
        ORDER BY
            CASE idt.priority WHEN 'HIGH' THEN 0 WHEN 'NORMAL' THEN 1 ELSE 2 END,
            idt.due_date ASC,
            idt.created_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/board")
async def board_inter_dept_tasks(
    to_dept: Optional[str] = Query(None, description="Filter the kanban view by destination dept"),
):
    """Kanban view grouped by status."""
    base = "SELECT * FROM sale_inter_dept_tasks WHERE status = ?"
    params: list = []
    if to_dept:
        base += " AND to_dept = ?"
        params.append(to_dept)
    base += " ORDER BY created_at DESC LIMIT 50"

    board = {}
    for st in ("PENDING", "IN_PROGRESS", "COMPLETED", "REJECTED", "CANCELLED"):
        board[st] = query(base, [st] + params)
    return board


@router.get("/{idt_id}")
async def get_inter_dept_task(idt_id: str):
    item = query(
        """
        SELECT idt.*, o.project_name, o.customer_name
        FROM sale_inter_dept_tasks idt
        LEFT JOIN sale_opportunities o ON o.id = idt.opportunity_id
        WHERE idt.id = ?
        """,
        [idt_id],
        one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Inter-dept task not found")
    return {"task": dict(item)}


@router.post("", dependencies=[Depends(require_write)])
async def create_inter_dept_task(payload: InterDeptCreate):
    """Create a new cross-department task. Notifies the to_user when set."""
    idt_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute(
        """
        INSERT INTO sale_inter_dept_tasks
            (id, task_id, opportunity_id, workflow_type, workflow_ref,
             title, description, from_dept, from_user, to_dept, to_user,
             cc_depts, step_number, total_steps, status, priority,
             sla_hours, due_date, input_data, requires_approval,
             comments, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', ?,
                ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            idt_id, payload.task_id, payload.opportunity_id,
            payload.workflow_type, payload.workflow_ref,
            payload.title, payload.description,
            payload.from_dept, payload.from_user,
            payload.to_dept, payload.to_user,
            payload.cc_depts, payload.step_number or 1, payload.total_steps or 1,
            payload.priority or "NORMAL",
            payload.sla_hours, payload.due_date, payload.input_data,
            1 if payload.requires_approval else 0,
            payload.comments, now, now,
        ],
    )

    if payload.to_user:
        write_notification(
            notification_type="INTER_DEPT_ASSIGNED",
            title=f"New cross-dept task: {payload.title}",
            message=f"{payload.from_dept} → {payload.to_dept}: {payload.workflow_type}",
            user_id=payload.to_user,
            entity_type="inter_dept_task",
            entity_id=idt_id,
            severity="INFO",
        )

    logger.info(
        "inter_dept_task_created",
        idt_id=idt_id, workflow_type=payload.workflow_type,
        from_dept=payload.from_dept, to_dept=payload.to_dept,
    )

    return {"id": idt_id, "status": "PENDING",
            "message": f"Inter-dept task created: {payload.title}"}


@router.patch("/{idt_id}", dependencies=[Depends(require_write)])
async def update_inter_dept_task(idt_id: str, payload: InterDeptUpdate):
    """Update an inter-dept task. Status transitions are validated.

    Auto-stamps started_at on first IN_PROGRESS, completed_at on COMPLETED,
    approved_at when approved_by is set.
    """
    existing = query(
        "SELECT * FROM sale_inter_dept_tasks WHERE id = ?",
        [idt_id], one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Inter-dept task not found")

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    new_status = data.get("status")
    if new_status and new_status != existing.get("status"):
        _validate(existing.get("status") or "PENDING", new_status)
        log_status_change("inter_dept_task", idt_id,
                          existing.get("status") or "", new_status)

        if new_status == "IN_PROGRESS" and not existing.get("started_at"):
            data["started_at"] = datetime.now().isoformat()
        elif new_status == "COMPLETED":
            data["completed_at"] = datetime.now().isoformat()
            # SLA evaluation
            due = existing.get("due_date")
            if due and "sla_met" not in data:
                try:
                    due_dt = datetime.fromisoformat(due.replace("Z", "+00:00"))
                    data["sla_met"] = 1 if datetime.now() <= due_dt else 0
                except Exception:
                    pass

    if "approved_by" in data and data["approved_by"]:
        data["approved_at"] = data.get("approved_at") or datetime.now().isoformat()

    if "sla_met" in data and isinstance(data["sla_met"], bool):
        data["sla_met"] = 1 if data["sla_met"] else 0

    sets = [f"{k} = ?" for k in data.keys()]
    sets.append("updated_at = ?")
    params = list(data.values()) + [datetime.now().isoformat(), idt_id]

    execute(
        f"UPDATE sale_inter_dept_tasks SET {', '.join(sets)} WHERE id = ?",
        params,
    )

    return {"id": idt_id, "status": "ok", "updated_fields": list(data.keys())}


@router.post("/{idt_id}/escalate", dependencies=[Depends(require_write)])
async def escalate_inter_dept_task(
    idt_id: str,
    escalated_to: str = Query(..., description="User to escalate to"),
    reason: Optional[str] = Query(None),
):
    """Escalate to a higher authority — flips is_escalated and writes a CRIT
    notification for the escalation target.
    """
    existing = query(
        "SELECT id, title, status FROM sale_inter_dept_tasks WHERE id = ?",
        [idt_id], one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Inter-dept task not found")

    now = datetime.now().isoformat()
    execute(
        """
        UPDATE sale_inter_dept_tasks
        SET is_escalated = 1, escalated_to = ?, escalated_at = ?,
            escalation_reason = ?, updated_at = ?
        WHERE id = ?
        """,
        [escalated_to, now, reason, now, idt_id],
    )

    write_notification(
        notification_type="INTER_DEPT_ESCALATED",
        title=f"Escalation: {existing.get('title')}",
        message=reason or "Task escalated for review",
        user_id=escalated_to,
        entity_type="inter_dept_task",
        entity_id=idt_id,
        severity="CRIT",
    )

    return {"id": idt_id, "status": "ok", "escalated_to": escalated_to}
