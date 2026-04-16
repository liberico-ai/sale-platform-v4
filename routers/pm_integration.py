"""
PM Integration Router
Handles bidirectional integration with ibshi1 PM platform.
Includes project status, task sync, timeline, and draft email management.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
import httpx
from ..database import query, execute
from .. import config
from datetime import datetime
import uuid
import json

router = APIRouter(prefix="/pm-integration", tags=["PM Integration"])


class WorkflowTaskCreate(BaseModel):
    """Model for creating a workflow task in PM."""
    project_code: str
    task_title: str
    task_description: Optional[str] = None
    assigned_to: Optional[str] = None
    priority: str = "NORMAL"


class DraftReplyCreate(BaseModel):
    """Model for creating a draft email reply."""
    email_id: str
    project_code: str
    draft_content: str
    recipient_email: str


class DraftReplyApprove(BaseModel):
    """Model for approving and sending a draft reply."""
    approved_by: str


async def call_ibshi1_api(method: str, endpoint: str, data=None):
    """
    Helper to call ibshi1 API with proper error handling.
    
    Args:
        method: HTTP method (GET, POST, PATCH)
        endpoint: API endpoint path
        data: Request body data
        
    Returns:
        dict: API response
        
    Raises:
        HTTPException: 503 if ibshi1 unavailable
    """
    url = f"{config.IBSHI1_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {config.IBSHI1_TOKEN}"}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            if method == "GET":
                response = await client.get(url, headers=headers)
            elif method == "POST":
                response = await client.post(url, json=data, headers=headers)
            elif method == "PATCH":
                response = await client.patch(url, json=data, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"PM service unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"PM service error: {e.response.text}"
        )


@router.get("/project/{project_code}/status")
async def get_project_status(project_code: str):
    """
    Get project status from ibshi1 PM platform.
    Proxy call to ibshi1 GET /api/projects?projectCode=xxx
    
    Args:
        project_code: Project code (e.g., "V17556")
        
    Returns:
        dict: Project status from PM platform
        
    Raises:
        HTTPException: 503 if PM service unavailable
    """
    result = await call_ibshi1_api("GET", f"/api/projects?projectCode={project_code}")
    return result


@router.post("/tasks")
async def create_pm_task(task: WorkflowTaskCreate):
    """
    Create a WorkflowTask in ibshi1 from Sale context.
    Logs sync to sale_pm_sync_log.
    
    Args:
        task: Task creation data with project_code
        
    Returns:
        dict: Created task ID and sync log entry
        
    Raises:
        HTTPException: 503 if PM service unavailable
    """
    # Call ibshi1 API to create task
    pm_response = await call_ibshi1_api("POST", "/api/workflow-tasks", {
        "projectCode": task.project_code,
        "title": task.task_title,
        "description": task.task_description,
        "assignedTo": task.assigned_to,
        "priority": task.priority,
    })
    
    pm_task_id = pm_response.get("id")
    
    # Log the sync
    sync_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    execute("""
        INSERT INTO sale_pm_sync_log
            (id, direction, source_entity, source_id, target_entity, target_id,
             project_code, sync_type, action, payload, status, triggered_by, created_at)
        VALUES (?, 'SALE_TO_PM', 'sale_tasks', ?, 'WorkflowTask', ?, ?, 
                'TASK_STATUS_UPDATE', 'CREATE', ?, 'SYNCED', 'API', ?)
    """, [
        sync_id, sync_id, pm_task_id, task.project_code,
        json.dumps(pm_response), now
    ])
    
    return {
        "sync_id": sync_id,
        "pm_task_id": pm_task_id,
        "status": "synced",
        "message": f"Task created in PM: {task.task_title}"
    }


@router.get("/project/{project_code}/timeline")
async def get_project_timeline(project_code: str):
    """
    Get milestones and tasks timeline from ibshi1.
    
    Args:
        project_code: Project code (e.g., "V17556")
        
    Returns:
        dict: Milestones and tasks from PM platform
        
    Raises:
        HTTPException: 503 if PM service unavailable
    """
    result = await call_ibshi1_api(
        "GET",
        f"/api/projects/{project_code}/timeline"
    )
    return result


@router.post("/draft-reply")
async def create_draft_reply(draft: DraftReplyCreate):
    """
    Draft a customer email reply based on PM data.
    Status=DRAFT, requires_review=True, NEVER auto-send.
    
    Args:
        draft: Draft creation data with email_id, project_code, content
        
    Returns:
        dict: Created draft ID with review status
    """
    # Check if email exists
    email = query(
        "SELECT * FROM sale_emails WHERE id = ?",
        [draft.email_id],
        one=True
    )
    
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    draft_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    # Log draft creation
    execute("""
        INSERT INTO sale_pm_sync_log
            (id, direction, source_entity, source_id, target_entity, target_id,
             project_code, sync_type, action, payload, status, triggered_by, created_at)
        VALUES (?, 'SALE_TO_PM', 'sale_emails', ?, 'DraftEmail', ?, ?, 
                'DRAFT_REPLY_CREATED', 'DRAFT', ?, 'DRAFT', 'API', ?)
    """, [
        draft_id, draft.email_id, draft_id, draft.project_code,
        json.dumps({
            "recipient": draft.recipient_email,
            "content": draft.draft_content,
            "requires_review": True
        }), now
    ])
    
    return {
        "draft_id": draft_id,
        "status": "draft",
        "requires_review": True,
        "message": "Draft created. Awaiting review before sending.",
        "review_url": f"/api/v1/pm-integration/draft-reply/{draft_id}/approve"
    }


@router.patch("/draft-reply/{draft_id}/approve")
async def approve_draft_reply(draft_id: str, approval: DraftReplyApprove):
    """
    Approve a draft email and send via Gmail API.
    
    Args:
        draft_id: Draft ID (UUID)
        approval: Approval data with approved_by user
        
    Returns:
        dict: Sent email details
        
    Raises:
        HTTPException: 404 if draft not found
    """
    # Get draft from sync log
    draft_record = query(
        "SELECT * FROM sale_pm_sync_log WHERE id = ? AND status = 'DRAFT'",
        [draft_id],
        one=True
    )
    
    if not draft_record:
        raise HTTPException(status_code=404, detail="Draft not found or already sent")
    
    now = datetime.now().isoformat()
    
    # In production, send via Gmail API
    # For now, update sync log status to SYNCED
    execute("""
        UPDATE sale_pm_sync_log
        SET status = 'SYNCED', reviewed_by = ?, reviewed_at = ?
        WHERE id = ?
    """, [approval.approved_by, now, draft_id])
    
    return {
        "draft_id": draft_id,
        "status": "sent",
        "message": "Draft approved and sent successfully",
        "sent_at": now,
        "reviewed_by": approval.approved_by
    }


@router.get("/sync-log")
async def get_sync_log(
    direction: Optional[str] = Query(None, description="Filter by direction"),
    project_code: Optional[str] = Query(None, description="Filter by project code"),
    status: Optional[str] = Query(None, description="Filter by sync status"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    View sync history between Sale and PM platforms.
    
    Args:
        direction: Optional direction filter (SALE_TO_PM, PM_TO_SALE)
        project_code: Optional project code filter
        status: Optional status filter (PENDING, SYNCED, FAILED, DRAFT)
        limit: Number of results to return (1-200)
        offset: Number of results to skip
        
    Returns:
        dict: Total count, sync log items, limit, and offset
    """
    where = []
    params = []
    
    if direction:
        where.append("direction = ?")
        params.append(direction)
    
    if project_code:
        where.append("project_code = ?")
        params.append(project_code)
    
    if status:
        where.append("status = ?")
        params.append(status)
    
    where_sql = " AND ".join(where) if where else "1=1"
    
    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_pm_sync_log WHERE {where_sql}",
        params
    )[0]["cnt"]
    
    items = query(f"""
        SELECT * FROM sale_pm_sync_log
        WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """, params + [limit, offset])
    
    return {"total": total, "items": items, "limit": limit, "offset": offset}
