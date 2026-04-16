"""
Task models for IBS HI Sale Platform.
Defines schemas for task management and workflow.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    """Request schema for creating a new task."""
    task_type: str
    title: str
    description: str
    opportunity_id: Optional[str] = None
    email_id: Optional[str] = None
    from_dept: str
    to_dept: str
    assigned_to: str
    assigned_by: str
    sla_hours: int
    due_date: str
    priority: str = "NORMAL"

    class Config:
        json_schema_extra = {
            "example": {
                "task_type": "COST_ESTIMATE",
                "title": "Prepare cost estimate for steel tank project",
                "description": "Customer needs detailed cost breakdown",
                "opportunity_id": "opp-001",
                "email_id": "email-001",
                "from_dept": "SALE",
                "to_dept": "TCKT",
                "assigned_to": "Hiệu",
                "assigned_by": "Tài",
                "sla_hours": 24,
                "due_date": "2026-04-20T17:00:00",
                "priority": "HIGH",
            }
        }


class TaskUpdate(BaseModel):
    """Request schema for updating a task."""
    status: Optional[str] = None
    result: Optional[str] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "COMPLETED",
                "result": "Cost estimate completed and sent to customer",
                "notes": "Estimate includes 15% margin",
            }
        }


class TaskResponse(BaseModel):
    """Response schema for task data."""
    id: str
    task_type: str
    title: str
    description: str
    opportunity_id: Optional[str]
    email_id: Optional[str]
    from_dept: str
    to_dept: str
    assigned_to: str
    assigned_by: str
    sla_hours: int
    due_date: str
    priority: str
    status: str
    result: Optional[str]
    notes: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
