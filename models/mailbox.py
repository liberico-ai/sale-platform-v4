"""
Mailbox models for IBS HI Sale Platform.
Defines schemas for email mailbox management.
"""

from pydantic import BaseModel
from typing import Optional


class MailboxCreate(BaseModel):
    """Request schema for creating a new monitored mailbox."""
    email_address: str
    display_name: str
    department: str
    owner_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "email_address": "sales@example.com",
                "display_name": "Sales Team",
                "department": "SALE",
                "owner_name": "Tài",
            }
        }


class MailboxUpdate(BaseModel):
    """Request schema for updating a mailbox."""
    display_name: Optional[str] = None
    department: Optional[str] = None
    owner_name: Optional[str] = None
    sync_enabled: Optional[bool] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "sync_enabled": False,
                "is_active": True,
            }
        }


class MailboxResponse(BaseModel):
    """Response schema for mailbox data."""
    id: str
    email_address: str
    display_name: str
    department: str
    owner_name: str
    sync_enabled: bool
    is_active: bool
    last_sync: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
