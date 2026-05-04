"""Tasks Router — Unified task engine for cross-department work routing.

Manages task creation, updates with state machine validation,
escalation, kanban board, and personal task lists.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

import structlog

try:
    from ..database import query, execute
    from ..auth import UserContext, get_current_writer, get_current_admin
    from ..errors import EntityNotFoundError
    from ..services.state_machine import (
        validate_task_transition,
        get_allowed_task_transitions,
        InvalidTransitionError,
    )
    from ..services.audit import log_status_change
    from ..services.notify import write_notification
except ImportError:
    from database import query, execute
    from auth import UserContext, get_current_writer, get_current_admin
    from errors import EntityNotFoundError
    from services.state_machine import (
        validate_task_transition,
        get_allowed_task_transitions,
        InvalidTransitionError,
    )
    from services.audit import log_status_change
    from services.notify import write_notification

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


class TaskCreate(BaseModel):
    """Model for creating a new task."""
    task_type: str
    title: str
    description: Optional[str] = None
    opportunity_id: Optional[str] = None
    email_id: Optional[str] = None
    from_dept: str
    to_dept: str
    assigned_to: Optional[str] = None
    assigned_by: Optional[str] = None
    sla_hours: Optional[int] = None
    due_date: Optional[str] = None
    priority: str = "NORMAL"


class TaskUpdate(BaseModel):
    """Model for updating a task.

    sale_tasks has no `notes` column — use `result` for completion notes
    or `description` for ongoing context.
    """
    status: Optional[str] = None
    result: Optional[str] = None
    assigned_to: Optional[str] = None
    description: Optional[str] = None


class TaskEscalate(BaseModel):
    """Model for escalating a task."""
    escalated_to: str


@router.get("")
async def list_tasks(
    status: Optional[str] = Query(None, description="Filter by status"),
    to_dept: Optional[str] = Query(None, description="Filter by destination department"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned user"),
    overdue_only: bool = Query(False, description="Show only overdue tasks"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List tasks with optional filtering, ordered by priority.

    Args:
        status: Filter by task status.
        to_dept: Filter by destination department.
        assigned_to: Filter by assigned user.
        overdue_only: Show overdue tasks only.
        limit: Results per page (1-200).
        offset: Number of results to skip.

    Returns:
        Paginated list of tasks with opportunity context.
    """
    where = []
    params = []

    if status:
        where.append("t.status = ?")
        params.append(status)
    if to_dept:
        where.append("t.to_dept = ?")
        params.append(to_dept)
    if assigned_to:
        where.append("t.assigned_to = ?")
        params.append(assigned_to)
    if overdue_only:
        where.append("t.status = 'OVERDUE'")

    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_tasks t WHERE {where_sql}",
        params
    )[0]["cnt"]

    items = query(f"""
        SELECT t.*, o.project_name, o.customer_name
        FROM sale_tasks t
        LEFT JOIN sale_opportunities o ON t.opportunity_id = o.id
        WHERE {where_sql}
        ORDER BY
            CASE t.status WHEN 'OVERDUE' THEN 0 WHEN 'PENDING' THEN 1
                          WHEN 'IN_PROGRESS' THEN 2 ELSE 3 END,
            t.due_date ASC,
            CASE t.priority WHEN 'HIGH' THEN 0 WHEN 'NORMAL' THEN 1 ELSE 2 END
        LIMIT ? OFFSET ?
    """, params + [limit, offset])

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/board")
async def get_task_board():
    """Get kanban board data grouped by status.

    Returns:
        Tasks grouped by status (PENDING, IN_PROGRESS, COMPLETED, OVERDUE).
    """
    statuses = ["PENDING", "IN_PROGRESS", "COMPLETED", "OVERDUE"]
    board = {}

    for status_val in statuses:
        items = query("""
            SELECT t.*, o.project_name, o.customer_name
            FROM sale_tasks t
            LEFT JOIN sale_opportunities o ON t.opportunity_id = o.id
            WHERE t.status = ?
            ORDER BY t.created_at DESC
            LIMIT 50
        """, [status_val])
        board[status_val] = items

    return board


@router.get("/my")
async def get_my_tasks(
    current_user: Optional[str] = Query(
        None,
        description="Override identity. Defaults to authenticated user.",
    ),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    user: UserContext = Depends(get_current_writer),
):
    """Get tasks assigned to the current user (Phase 2 step 7).

    Identity resolves automatically from the X-API-Key — the
    ``current_user`` query param is now optional and exists only so
    ADMIN can pull someone else's queue.
    """
    # Match the dashboard /my pattern: prefer authenticated identity.
    target = current_user or user.user_email or user.user_name or user.actor

    total = query(
        "SELECT COUNT(*) as cnt FROM sale_tasks WHERE assigned_to = ?",
        [target]
    )[0]["cnt"]

    items = query("""
        SELECT t.*, o.project_name, o.customer_name
        FROM sale_tasks t
        LEFT JOIN sale_opportunities o ON t.opportunity_id = o.id
        WHERE t.assigned_to = ?
        ORDER BY
            CASE t.status WHEN 'OVERDUE' THEN 0 WHEN 'PENDING' THEN 1
                          WHEN 'IN_PROGRESS' THEN 2 ELSE 3 END,
            t.due_date ASC
        LIMIT ? OFFSET ?
    """, [target, limit, offset])

    return {
        "user": target,
        "total": total,
        "items": items,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{task_id}")
async def get_task_detail(task_id: str):
    """Detailed view of a single task (Phase 2 step 7).

    Joins linked opportunity + email so the SPA's task drawer renders
    the full context without N+1 round-trips.
    """
    task = query(
        """
        SELECT t.*,
               o.project_name AS opportunity_project,
               o.customer_name AS opportunity_customer,
               o.stage AS opportunity_stage,
               e.subject AS email_subject,
               e.from_address AS email_from
        FROM sale_tasks t
        LEFT JOIN sale_opportunities o ON o.id = t.opportunity_id
        LEFT JOIN sale_emails e ON e.id = t.email_id
        WHERE t.id = ?
        """,
        [task_id], one=True,
    )
    if not task:
        raise EntityNotFoundError("Task", task_id)

    # Allowed transitions for the SPA's status buttons.
    allowed_next = get_allowed_task_transitions(task.get("status") or "PENDING")

    return {
        "task": dict(task),
        "allowed_next_statuses": allowed_next,
    }


@router.post("")
async def create_task(
    task: TaskCreate,
    user: UserContext = Depends(get_current_writer),
):
    """Create a new task with optional email activity logging.

    Args:
        task: Task creation data.

    Returns:
        Created task ID and status.
    """
    task_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute("""
        INSERT INTO sale_tasks
            (id, opportunity_id, email_id, task_type, title, description,
             from_dept, to_dept, assigned_to, assigned_by, sla_hours, due_date,
             status, priority, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', ?, ?, ?)
    """, [
        task_id, task.opportunity_id, task.email_id, task.task_type,
        task.title, task.description, task.from_dept, task.to_dept,
        task.assigned_to, task.assigned_by, task.sla_hours,
        task.due_date, task.priority, now, now
    ])

    # Log activity if linked to email
    if task.email_id:
        execute("""
            INSERT INTO sale_email_activity_log
                (id, email_id, opportunity_id, task_id, action_type, action_by, created_at)
            VALUES (?, ?, ?, ?, 'TASK_CREATED', ?, ?)
        """, [str(uuid.uuid4()), task.email_id, task.opportunity_id,
              task_id, task.assigned_by, now])

    logger.info("task_created",
                task_id=task_id,
                task_type=task.task_type,
                from_dept=task.from_dept,
                to_dept=task.to_dept)

    # Notify the assignee on creation (if any). Uses dedupe so the same
    # assignee won't get spammed if the task is bounced back-and-forth.
    if task.assigned_to:
        write_notification(
            notification_type="TASK_ASSIGNED",
            title=f"New task: {task.title}",
            message=(
                f"{task.from_dept} → {task.to_dept}: {task.task_type}"
                + (f" (priority: {task.priority})" if task.priority else "")
            ),
            user_id=task.assigned_to,
            entity_type="task",
            entity_id=task_id,
            severity="INFO",
        )

    return {"id": task_id, "status": "ok", "message": f"Task created: {task.title}"}


@router.patch("/{task_id}")
async def update_task(
    task_id: str,
    update: TaskUpdate,
    user: UserContext = Depends(get_current_writer),
):
    """Update task with state machine validation for status changes.

    Auto-timestamps: started_at on IN_PROGRESS, completed_at on COMPLETED.

    Args:
        task_id: Task ID (UUID).
        update: Fields to update.

    Returns:
        Updated task ID with allowed next statuses.

    Raises:
        HTTPException: 404 if not found, 422 if invalid transition.
    """
    existing = query(
        "SELECT * FROM sale_tasks WHERE id = ?",
        [task_id],
        one=True
    )

    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")

    sets = []
    params = []

    if update.status is not None and update.status != existing.get("status"):
        current_status = existing.get("status", "PENDING")

        # Validate transition via state machine
        try:
            validate_task_transition(current_status, update.status)
        except InvalidTransitionError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        sets.append("status = ?")
        params.append(update.status)

        # Auto-timestamps
        if update.status == "IN_PROGRESS" and not existing.get("started_at"):
            sets.append("started_at = ?")
            params.append(datetime.now().isoformat())
        elif update.status == "COMPLETED":
            sets.append("completed_at = ?")
            params.append(datetime.now().isoformat())

        # Audit log
        log_status_change(
            "task", task_id, current_status, update.status,
            changed_by=user.actor,
        )

        logger.info("task_status_changed",
                     task_id=task_id,
                     from_status=current_status,
                     to_status=update.status)

    if update.result is not None:
        sets.append("result = ?")
        params.append(update.result)
    if update.assigned_to is not None:
        sets.append("assigned_to = ?")
        params.append(update.assigned_to)
        # Notify the new assignee when the task is reassigned to a
        # different person.
        if update.assigned_to != existing.get("assigned_to"):
            write_notification(
                notification_type="TASK_ASSIGNED",
                title=f"Task reassigned to you: {existing.get('title') or 'Task'}",
                message=existing.get("description") or existing.get("task_type"),
                user_id=update.assigned_to,
                entity_type="task",
                entity_id=task_id,
                severity="INFO",
            )
    if update.description is not None:
        sets.append("description = ?")
        params.append(update.description)

    if not sets:
        raise HTTPException(status_code=400, detail="No fields to update")

    sets.append("updated_at = ?")
    params.append(datetime.now().isoformat())
    params.append(task_id)

    execute(f"UPDATE sale_tasks SET {', '.join(sets)} WHERE id = ?", params)

    current_status = update.status or existing.get("status", "PENDING")
    allowed_next = get_allowed_task_transitions(current_status)

    return {
        "id": task_id,
        "status": "ok",
        "current_status": current_status,
        "allowed_next_statuses": allowed_next,
    }


@router.post("/{task_id}/escalate")
async def escalate_task(
    task_id: str,
    escalate: TaskEscalate,
    user: UserContext = Depends(get_current_writer),
):
    """Escalate a task by incrementing escalation_count.

    Args:
        task_id: Task ID (UUID).
        escalate: Escalation target user.

    Returns:
        Escalated task ID and new escalation count.

    Raises:
        HTTPException: 404 if not found.
    """
    existing = query(
        "SELECT * FROM sale_tasks WHERE id = ?",
        [task_id],
        one=True
    )

    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")

    current_count = existing.get("escalation_count", 0) or 0
    new_count = current_count + 1
    now = datetime.now().isoformat()

    execute("""
        UPDATE sale_tasks
        SET is_escalated = 1, escalation_count = ?, escalated_to = ?,
            escalated_at = ?, updated_at = ?
        WHERE id = ?
    """, [new_count, escalate.escalated_to, now, now, task_id])

    logger.info("task_escalated",
                task_id=task_id,
                escalated_to=escalate.escalated_to,
                escalation_count=new_count)

    return {
        "id": task_id,
        "status": "ok",
        "escalation_count": new_count,
        "escalated_to": escalate.escalated_to,
    }


@router.delete("/{task_id}")
async def soft_delete_task(
    task_id: str,
    user: UserContext = Depends(get_current_admin),
):
    """Soft-delete a task: set status='CANCELLED'. Admin only.

    Tasks aren't truly deleted because email_activity_log and audit
    history reference task IDs.
    """
    existing = query(
        "SELECT id, status FROM sale_tasks WHERE id = ?",
        [task_id], one=True,
    )
    if not existing:
        raise EntityNotFoundError("Task", task_id)

    if existing.get("status") == "CANCELLED":
        return {"id": task_id, "status": "already_cancelled"}

    now = datetime.now().isoformat()
    execute(
        "UPDATE sale_tasks SET status = 'CANCELLED', updated_at = ? WHERE id = ?",
        [now, task_id],
    )

    log_status_change(
        "task", task_id,
        existing.get("status") or "", "CANCELLED",
        changed_by=user.actor,
    )
    logger.info("task_soft_deleted", task_id=task_id)
    return {"id": task_id, "status": "cancelled"}
