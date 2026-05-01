"""
Emails Router
Manages email data, filtering, threading, Gmail sync, and task creation from emails.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

import structlog

try:
    from ..database import query, execute
    from ..auth import require_write
except ImportError:
    from database import query, execute
    from auth import require_write

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/emails", tags=["Emails"])


class EmailUpdate(BaseModel):
    """Model for updating an email.

    Schema column is `email_type` (10 canonical types from config.EMAIL_TYPES).
    """
    email_type: Optional[str] = None
    opportunity_id: Optional[str] = None
    customer_id: Optional[str] = None
    is_read: Optional[bool] = None
    is_actioned: Optional[bool] = None


class TaskFromEmailCreate(BaseModel):
    """Model for creating a task from email."""
    task_type: str
    title: str
    description: Optional[str] = None
    from_dept: str
    to_dept: str
    assigned_to: Optional[str] = None
    sla_hours: Optional[int] = None
    due_date: Optional[str] = None
    priority: str = "NORMAL"


@router.get("")
async def list_emails(
    email_type: Optional[str] = Query(None, description="Filter by email type"),
    is_read: Optional[bool] = Query(None, description="Filter by read status"),
    is_actioned: Optional[bool] = Query(None, description="Filter by actioned status"),
    source_dept: Optional[str] = Query(None, description="Filter by source department"),
    date_from: Optional[str] = Query(None, description="Filter emails from date (ISO format)"),
    date_to: Optional[str] = Query(None, description="Filter emails to date (ISO format)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    List emails with optional filtering by type, read status, actioned status,
    source department, and date range.
    
    Args:
        email_type: Optional email type filter
        is_read: Optional read status filter
        is_actioned: Optional actioned status filter
        source_dept: Optional source department filter
        date_from: Optional start date for filtering (ISO format)
        date_to: Optional end date for filtering (ISO format)
        limit: Number of results to return (1-200)
        offset: Number of results to skip
        
    Returns:
        dict: Total count, items list, limit, and offset
    """
    where = []
    params = []
    
    if email_type:
        where.append("email_type = ?")
        params.append(email_type)
    if is_read is not None:
        where.append("is_read = ?")
        params.append(1 if is_read else 0)
    if is_actioned is not None:
        where.append("is_actioned = ?")
        params.append(1 if is_actioned else 0)
    if source_dept:
        where.append("source_dept = ?")
        params.append(source_dept)
    if date_from:
        where.append("created_at >= ?")
        params.append(date_from)
    if date_to:
        where.append("created_at <= ?")
        params.append(date_to)
    
    where_sql = " AND ".join(where) if where else "1=1"
    
    total = query(f"SELECT COUNT(*) as cnt FROM sale_emails WHERE {where_sql}", params)[0]["cnt"]
    
    items = query(f"""
        SELECT * FROM sale_emails
        WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """, params + [limit, offset])
    
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/{email_id}")
async def get_email_detail(email_id: str):
    """
    Get email detail with complete thread (emails with same thread_id).
    
    Args:
        email_id: Email ID (UUID)
        
    Returns:
        dict: Email detail with related thread messages
        
    Raises:
        HTTPException: 404 if email not found
    """
    email = query(
        "SELECT * FROM sale_emails WHERE id = ?",
        [email_id],
        one=True
    )
    
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    thread_id = email.get("thread_id") if hasattr(email, 'get') else email["thread_id"]
    
    thread = query(
        "SELECT * FROM sale_emails WHERE thread_id = ? ORDER BY created_at ASC",
        [thread_id]
    )
    
    return {
        "email": dict(email) if not isinstance(email, dict) else email,
        "thread": thread,
    }


@router.post("/sync", dependencies=[Depends(require_write)])
async def trigger_gmail_sync():
    """Trigger Gmail sync.

    Records the trigger in sale_pm_sync_log so workers can pick it up
    on the next poll. Actual fetch happens in workers/gmail_worker.py.

    Returns:
        dict: Sync ID and status.
    """
    sync_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute("""
        INSERT INTO sale_pm_sync_log
            (id, direction, source_entity, source_id,
             target_entity, sync_type, action, status, triggered_by, created_at)
        VALUES (?, 'PM_TO_SALE', 'gmail', ?, 'sale_emails',
                'GMAIL_SYNC', 'TRIGGER', 'PENDING', 'API', ?)
    """, [sync_id, sync_id, now])

    return {
        "sync_id": sync_id,
        "status": "initiated",
        "message": "Gmail sync triggered — worker will pick up on next poll",
    }


@router.patch("/{email_id}", dependencies=[Depends(require_write)])
async def update_email(email_id: str, update: EmailUpdate):
    """
    Update email: classify, link to opportunity, mark read/actioned.
    
    Args:
        email_id: Email ID (UUID)
        update: Update data (classification, opportunity_id, is_read, is_actioned)
        
    Returns:
        dict: Updated email ID and status
        
    Raises:
        HTTPException: 404 if email not found
    """
    existing = query(
        "SELECT * FROM sale_emails WHERE id = ?",
        [email_id],
        one=True
    )
    
    if not existing:
        raise HTTPException(status_code=404, detail="Email not found")
    
    sets = []
    params = []

    if update.email_type is not None:
        sets.append("email_type = ?")
        params.append(update.email_type)
    if update.opportunity_id is not None:
        sets.append("opportunity_id = ?")
        params.append(update.opportunity_id)
    if update.customer_id is not None:
        sets.append("customer_id = ?")
        params.append(update.customer_id)
    if update.is_read is not None:
        sets.append("is_read = ?")
        params.append(1 if update.is_read else 0)
    if update.is_actioned is not None:
        sets.append("is_actioned = ?")
        params.append(1 if update.is_actioned else 0)

    if not sets:
        raise HTTPException(status_code=400, detail="No fields to update")

    # sale_emails has no updated_at column — use processed_at as touch marker
    sets.append("processed_at = ?")
    params.append(datetime.now().isoformat())
    params.append(email_id)

    execute(f"UPDATE sale_emails SET {', '.join(sets)} WHERE id = ?", params)

    return {"id": email_id, "status": "ok"}


@router.post("/{email_id}/create-task", dependencies=[Depends(require_write)])
async def create_task_from_email(email_id: str, task: TaskFromEmailCreate):
    """
    Create a task from email context, auto-linking email_id and opportunity_id.
    
    Args:
        email_id: Email ID (UUID)
        task: Task creation data
        
    Returns:
        dict: Created task ID and status
        
    Raises:
        HTTPException: 404 if email not found
    """
    email = query(
        "SELECT * FROM sale_emails WHERE id = ?",
        [email_id],
        one=True
    )
    
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    task_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    opportunity_id = email.get("opportunity_id") if hasattr(email, 'get') else email.get("opportunity_id")
    
    execute("""
        INSERT INTO sale_tasks
            (id, opportunity_id, email_id, task_type, title, description,
             from_dept, to_dept, assigned_to, assigned_by, sla_hours, due_date,
             status, priority, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', ?, ?, ?)
    """, [
        task_id, opportunity_id, email_id, task.task_type, task.title,
        task.description, task.from_dept, task.to_dept, task.assigned_to,
        task.assigned_to, task.sla_hours, task.due_date, task.priority, now, now
    ])
    
    # Log activity
    execute("""
        INSERT INTO sale_email_activity_log (id, email_id, opportunity_id, task_id, action_type, action_by, created_at)
        VALUES (?, ?, ?, ?, 'TASK_CREATED', ?, ?)
    """, [str(uuid.uuid4()), email_id, opportunity_id, task_id, task.assigned_to, now])

    return {"id": task_id, "status": "ok", "message": f"Task created from email: {task.title}"}


# ═══════════════════════════════════════════════════════════════
# sale_email_labels — Gmail label catalog (47 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/labels/list")
async def list_email_labels(
    customer_id: Optional[str] = Query(None, description="Filter by linked customer"),
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List Gmail labels indexed from ibshi@ mailbox.

    Each label maps to a customer thread and tracks conversation_count.
    """
    where = []
    params: list = []
    if customer_id:
        where.append("label.customer_id = ?")
        params.append(customer_id)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_email_labels label WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT label.*, c.name AS customer_name
        FROM sale_email_labels label
        LEFT JOIN sale_customers c ON c.id = label.customer_id
        WHERE {where_sql}
        ORDER BY label.conversation_count DESC, label.label_name ASC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


# ═══════════════════════════════════════════════════════════════
# sale_email_full — Full ibshi@ email mapping (108 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/full/list")
async def list_email_full(
    project_code: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None),
    action_required: Optional[str] = Query(None, description="URGENT, ACTION_IBS, FOLLOW_UP, PENDING_PAYMENT, PENDING_APPROVAL, NONE"),
    priority: Optional[str] = Query(None, description="HIGH, MEDIUM, LOW"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List the full ibshi@ email mapping with action / priority filters."""
    where = []
    params: list = []
    if project_code:
        where.append("project_code = ?")
        params.append(project_code)
    if customer_name:
        where.append("customer_name LIKE ?")
        params.append(f"%{customer_name}%")
    if action_required:
        where.append("action_required = ?")
        params.append(action_required)
    if priority:
        where.append("priority = ?")
        params.append(priority)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_email_full WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT * FROM sale_email_full
        WHERE {where_sql}
        ORDER BY
            CASE priority WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END,
            email_date DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/views/follow-ups")
async def list_follow_ups(limit: int = Query(50, ge=1, le=200)):
    """Pending follow-ups via v_sale_followups view (action_required != NONE).

    Two-segment path so it doesn't collide with `/emails/{email_id}`.
    """
    items = query(
        "SELECT * FROM v_sale_followups LIMIT ?",
        [limit],
    )
    return {"items": items, "count": len(items)}


# ═══════════════════════════════════════════════════════════════
# Email compose — DRAFT-only (CLAUDE.md rule #8)
# ═══════════════════════════════════════════════════════════════

class EmailDraftCompose(BaseModel):
    """Compose a new outbound email — STORED AS DRAFT, never sent.

    Either supply `template_type` to render from sale_email_templates with
    `variables`, or supply `subject` + `body` directly.
    """
    to_address: str
    customer_id: Optional[str] = None
    opportunity_id: Optional[str] = None
    contact_id: Optional[str] = None
    cc: Optional[str] = None
    template_type: Optional[str] = None
    variables: Optional[dict] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    mailbox_id: Optional[str] = None
    composed_by: Optional[str] = None


def _render_template(subject: str, body: str, variables: dict) -> tuple:
    """Mustache-lite renderer — replaces {{key}} occurrences in subject + body."""
    rendered_subject = subject or ""
    rendered_body = body or ""
    for k, v in (variables or {}).items():
        token = "{{" + str(k) + "}}"
        rendered_subject = rendered_subject.replace(token, str(v))
        rendered_body = rendered_body.replace(token, str(v))
    return rendered_subject, rendered_body


@router.post("/compose", dependencies=[Depends(require_write)])
async def compose_email_draft(payload: EmailDraftCompose):
    """Compose an outbound email and STORE AS DRAFT.

    Per CLAUDE.md rule #8: Sale Platform NEVER auto-sends customer email.
    The frontend collects review + approval before any send action.

    Behavior:
    - If template_type is set, look up the template and render
      {{var}} placeholders from `variables`.
    - Otherwise use the supplied subject/body directly.
    - Insert into sale_emails with email_type=DRAFT, is_actioned=0,
      and an activity log entry.
    """
    subject = payload.subject
    body = payload.body
    template_used = None

    if payload.template_type:
        tpl = query(
            "SELECT subject, body FROM sale_email_templates "
            "WHERE template_type = ? AND is_active = 1",
            [payload.template_type],
            one=True,
        )
        if not tpl:
            raise HTTPException(
                status_code=404,
                detail=f"Email template not found: {payload.template_type}",
            )
        subject, body = _render_template(
            tpl.get("subject") or "", tpl.get("body") or "",
            payload.variables or {},
        )
        template_used = payload.template_type

    if not subject or not body:
        raise HTTPException(
            status_code=400,
            detail="Need subject + body (or template_type that resolves to them)",
        )

    email_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute(
        """
        INSERT INTO sale_emails
            (id, mailbox_id, email_type, from_address, to_addresses, cc_addresses,
             subject, body_text, snippet,
             customer_id, opportunity_id,
             received_at, processed_at, is_read, is_actioned,
             created_at)
        VALUES (?, ?, 'DRAFT', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0, ?)
        """,
        [
            email_id, payload.mailbox_id, "(draft)",
            payload.to_address, payload.cc,
            subject, body, body[:200] if body else None,
            payload.customer_id, payload.opportunity_id,
            now, now, now,
        ],
    )

    execute(
        """
        INSERT INTO sale_email_activity_log
            (id, email_id, opportunity_id, action_type, action_by, details, created_at)
        VALUES (?, ?, ?, 'REPLY_DRAFTED', ?, ?, ?)
        """,
        [
            str(uuid.uuid4()), email_id, payload.opportunity_id,
            payload.composed_by,
            f"Composed via /emails/compose; template={template_used}",
            now,
        ],
    )

    logger.info(
        "email_draft_composed",
        email_id=email_id,
        to=payload.to_address,
        template=template_used,
    )

    return {
        "id": email_id,
        "status": "DRAFT",
        "template_used": template_used,
        "subject": subject,
        "preview": (body or "")[:200],
        "warning": "Draft only — Sale Platform never auto-sends to customers",
    }


@router.post("/{email_id}/render-reply", dependencies=[Depends(require_write)])
async def render_reply_draft(
    email_id: str,
    template_type: str = Query(..., description="Email template type"),
):
    """Render a reply DRAFT for an existing email using a template.

    Auto-fills template variables from the source email + linked customer
    + linked opportunity. Returns the rendered draft without persisting.
    """
    src = query(
        """
        SELECT e.*, c.name AS customer_name, o.project_name
        FROM sale_emails e
        LEFT JOIN sale_customers c ON c.id = e.customer_id
        LEFT JOIN sale_opportunities o ON o.id = e.opportunity_id
        WHERE e.id = ?
        """,
        [email_id], one=True,
    )
    if not src:
        raise HTTPException(status_code=404, detail="Email not found")

    tpl = query(
        "SELECT subject, body, variables FROM sale_email_templates "
        "WHERE template_type = ? AND is_active = 1",
        [template_type], one=True,
    )
    if not tpl:
        raise HTTPException(
            status_code=404,
            detail=f"Email template not found: {template_type}",
        )

    auto_vars = {
        "project_name": src.get("project_name") or "(no project)",
        "customer_name": src.get("customer_name") or "",
        "contact_name": src.get("from_name") or "Sir/Madam",
        "subject": src.get("subject") or "",
        "today": datetime.now().strftime("%Y-%m-%d"),
        "sender_name": "IBS HI Sale Team",
    }
    rendered_subject, rendered_body = _render_template(
        tpl.get("subject") or "", tpl.get("body") or "", auto_vars,
    )

    return {
        "to_address": src.get("from_address"),
        "subject": rendered_subject,
        "body": rendered_body,
        "auto_vars": auto_vars,
        "template_type": template_type,
        "warning": "Render only — call /emails/compose to persist as DRAFT",
    }


@router.get("/views/project-activity")
async def list_project_activity(limit: int = Query(50, ge=1, le=200)):
    """Project-level email activity via v_project_activity view."""
    items = query(
        "SELECT * FROM v_project_activity LIMIT ?",
        [limit],
    )
    return {"items": items, "count": len(items)}
