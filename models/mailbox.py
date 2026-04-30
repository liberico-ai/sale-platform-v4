"""
Mailbox models for IBS HI Sale Platform.
Defines schemas for email mailbox management.
"""

from pydantic import BaseModel
from typing import Optional


class MailboxCreate(BaseModel):
    """Request schema for creating a new monitored mailbox.

    Matches sale_monitored_mailboxes — required: email_address, department.
    """
    email_address: str
    department: str
    display_name: Optional[str] = None
    owner_name: Optional[str] = None
    sync_enabled: Optional[bool] = True
    sync_from_date: Optional[str] = None
    is_active: Optional[bool] = True


class MailboxUpdate(BaseModel):
    """Request schema for updating a mailbox."""
    display_name: Optional[str] = None
    department: Optional[str] = None
    owner_name: Optional[str] = None
    sync_enabled: Optional[bool] = None
    is_active: Optional[bool] = None
    sync_from_date: Optional[str] = None


class MailboxResponse(BaseModel):
    """Response schema mirroring sale_monitored_mailboxes."""
    id: str
    email_address: str
    department: str
    display_name: Optional[str] = None
    owner_name: Optional[str] = None
    token_valid: Optional[int] = 0
    sync_enabled: Optional[int] = 1
    sync_from_date: Optional[str] = None
    last_sync_at: Optional[str] = None
    last_sync_count: Optional[int] = 0
    is_active: Optional[int] = 1
    deactivated_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
