"""Email models for IBS HI Sale Platform.

Field names mirror sale_emails (schema_all.sql).
"""

from pydantic import BaseModel
from typing import Optional


class EmailClassify(BaseModel):
    """Request schema for (re)classifying an email.

    `email_type` should match one of config.EMAIL_TYPES.
    """
    email_type: str
    confidence: Optional[float] = None


class EmailLinkOpp(BaseModel):
    """Request schema for linking an email to an opportunity / customer."""
    opportunity_id: Optional[str] = None
    customer_id: Optional[str] = None


class EmailResponse(BaseModel):
    """Response schema mirroring sale_emails."""
    id: str
    gmail_id: Optional[str] = None
    thread_id: Optional[str] = None
    mailbox_id: Optional[str] = None
    source_dept: Optional[str] = None
    email_type: Optional[str] = None
    confidence: Optional[float] = None
    from_address: Optional[str] = None
    from_name: Optional[str] = None
    to_addresses: Optional[str] = None
    cc_addresses: Optional[str] = None
    subject: Optional[str] = None
    snippet: Optional[str] = None
    body_text: Optional[str] = None
    has_attachments: Optional[int] = 0
    attachment_names: Optional[str] = None
    received_at: Optional[str] = None
    processed_at: Optional[str] = None
    opportunity_id: Optional[str] = None
    customer_id: Optional[str] = None
    is_read: Optional[int] = 0
    is_actioned: Optional[int] = 0
    actioned_by: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
