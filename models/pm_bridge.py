"""
PM Bridge models for IBS HI Sale Platform.
Defines schemas for Sale ↔ PM integration and synchronization.
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class PMTaskCreate(BaseModel):
    """Request schema for creating a PM task via Sale platform."""
    opportunity_id: str
    task_type: str
    title: str
    description: str
    assigned_role: str

    class Config:
        json_schema_extra = {
            "example": {
                "opportunity_id": "opp-001",
                "task_type": "MILESTONE_UPDATE",
                "title": "Technical design review",
                "description": "Customer approved technical specifications",
                "assigned_role": "TECHNICAL_LEAD",
            }
        }


class DraftReplyRequest(BaseModel):
    """Request schema for drafting an email reply via AI."""
    opportunity_id: str
    context: str
    template_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "opportunity_id": "opp-001",
                "context": "Customer asked about delivery timeline for steel tank project",
                "template_type": "DELIVERY_TIMELINE_RESPONSE",
            }
        }


class PMSyncLog(BaseModel):
    """Response schema for PM sync log entry."""
    id: str
    direction: str
    source_entity: str
    source_id: str
    target_entity: str
    target_id: Optional[str]
    opportunity_id: Optional[str]
    project_code: Optional[str]
    sync_type: str
    action: str
    status: str
    error_message: Optional[str]
    triggered_by: str
    reviewed_by: Optional[str]
    reviewed_at: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


class DraftReplyResponse(BaseModel):
    """Response schema for draft reply."""
    id: str
    opportunity_id: str
    email_id: Optional[str]
    draft_body: str
    template_type: str
    status: str
    created_by: str
    reviewed_by: Optional[str]
    reviewed_at: Optional[str]
    sent_at: Optional[str]
    created_at: str

    class Config:
        from_attributes = True
