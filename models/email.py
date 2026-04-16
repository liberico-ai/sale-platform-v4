"""
Email models for IBS HI Sale Platform.
Defines schemas for email classification and linking.
"""

from pydantic import BaseModel
from typing import Optional


class EmailClassify(BaseModel):
    """Request schema for classifying an email."""
    email_type: str
    confidence: float

    class Config:
        json_schema_extra = {
            "example": {
                "email_type": "RFQ",
                "confidence": 0.95,
            }
        }


class EmailLinkOpp(BaseModel):
    """Request schema for linking email to opportunity."""
    opportunity_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "opportunity_id": "opp-12345",
            }
        }


class EmailResponse(BaseModel):
    """Response schema for email data."""
    id: str
    message_id: str
    from_email: str
    to_email: str
    subject: str
    body: Optional[str]
    email_type: Optional[str]
    type_confidence: Optional[float]
    opportunity_id: Optional[str]
    mailbox_email: str
    received_at: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
