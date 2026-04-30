"""Models for sale_customer_interactions (175 records)."""

from typing import Optional

from pydantic import BaseModel


class CustomerInteractionCreate(BaseModel):
    """Required: customer_id, interaction_type, interaction_date, subject."""
    customer_id: str
    interaction_type: str
    interaction_date: str
    subject: str

    contact_id: Optional[str] = None
    opportunity_id: Optional[str] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    attendees_ibs: Optional[str] = None
    attendees_customer: Optional[str] = None
    summary: Optional[str] = None
    outcome: Optional[str] = None
    next_action: Optional[str] = None
    next_action_due: Optional[str] = None
    sentiment_score: Optional[float] = None
    nas_file_path: Optional[str] = None
    attachments: Optional[str] = None
    recorded_by: Optional[str] = None


class CustomerInteractionUpdate(BaseModel):
    """All fields optional."""
    interaction_type: Optional[str] = None
    interaction_date: Optional[str] = None
    subject: Optional[str] = None
    contact_id: Optional[str] = None
    opportunity_id: Optional[str] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    attendees_ibs: Optional[str] = None
    attendees_customer: Optional[str] = None
    summary: Optional[str] = None
    outcome: Optional[str] = None
    next_action: Optional[str] = None
    next_action_due: Optional[str] = None
    sentiment_score: Optional[float] = None
    nas_file_path: Optional[str] = None
    attachments: Optional[str] = None
    recorded_by: Optional[str] = None


class CustomerInteractionResponse(BaseModel):
    """Mirror of sale_customer_interactions."""
    id: str
    customer_id: str
    interaction_type: str
    interaction_date: str
    subject: str
    contact_id: Optional[str] = None
    opportunity_id: Optional[str] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    attendees_ibs: Optional[str] = None
    attendees_customer: Optional[str] = None
    summary: Optional[str] = None
    outcome: Optional[str] = None
    next_action: Optional[str] = None
    next_action_due: Optional[str] = None
    sentiment_score: Optional[float] = None
    nas_file_path: Optional[str] = None
    attachments: Optional[str] = None
    recorded_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
