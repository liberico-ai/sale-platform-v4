"""Task models for IBS HI Sale Platform.

Mirrors sale_tasks (schema_all.sql). NOT NULL columns: task_type, title,
from_dept, to_dept, status. `notes` does NOT exist on the table — use
`description` instead.
"""

from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    """Request schema for creating a new task."""
    task_type: str
    title: str
    from_dept: str
    to_dept: str

    description: Optional[str] = None
    opportunity_id: Optional[str] = None
    email_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_by: Optional[str] = None
    sla_hours: Optional[int] = None
    due_date: Optional[str] = None
    priority: Optional[str] = "NORMAL"
    nas_file_path: Optional[str] = None
    attachments: Optional[str] = None


class TaskUpdate(BaseModel):
    """Request schema for updating a task. All fields optional."""
    status: Optional[str] = None
    result: Optional[str] = None
    assigned_to: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None
    sla_hours: Optional[int] = None


class TaskResponse(BaseModel):
    """Response schema mirroring sale_tasks."""
    id: str
    task_type: str
    title: str
    from_dept: str
    to_dept: str
    status: str

    description: Optional[str] = None
    opportunity_id: Optional[str] = None
    email_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_by: Optional[str] = None
    sla_hours: Optional[int] = None
    due_date: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[str] = None
    is_escalated: Optional[int] = 0
    escalated_to: Optional[str] = None
    escalated_at: Optional[str] = None
    escalation_count: Optional[int] = 0
    nas_file_path: Optional[str] = None
    attachments: Optional[str] = None
    priority: Optional[str] = "NORMAL"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
