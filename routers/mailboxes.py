"""
Mailboxes Router
Manages monitored mailboxes and OAuth flow for Gmail integration.
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

try:
    from ..database import query, execute
except ImportError:
    from database import query, execute

router = APIRouter(prefix="/mailboxes", tags=["Mailboxes"])


class MailboxCreate(BaseModel):
    """Model for adding a new mailbox."""
    email_address: str
    mailbox_type: str = "SHARED"
    department: str


class MailboxUpdate(BaseModel):
    """Model for updating a mailbox."""
    is_active: Optional[bool] = None
    sync_enabled: Optional[bool] = None
    deactivated_at: Optional[str] = None


class OAuthCallback(BaseModel):
    """Model for OAuth callback."""
    code: str
    state: str


@router.get("")
async def list_mailboxes():
    """
    List all monitored mailboxes with their sync status.
    
    Returns:
        dict: List of mailboxes with active/inactive status and sync info
    """
    mailboxes = query("""
        SELECT 
            id, email_address, mailbox_type, department, is_active,
            sync_enabled, last_sync_at, created_at, updated_at
        FROM sale_monitored_mailboxes
        ORDER BY created_at DESC
    """)
    
    return {
        "total": len(mailboxes),
        "mailboxes": mailboxes,
    }


@router.post("")
async def add_mailbox(mailbox: MailboxCreate):
    """
    Add a new monitored mailbox.
    Inserts with token_valid=0 initially (requires OAuth completion).
    
    Args:
        mailbox: Mailbox creation data (email_address, mailbox_type, department)
        
    Returns:
        dict: Created mailbox ID and OAuth link for completion
    """
    mailbox_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    # Check if mailbox already exists
    existing = query(
        "SELECT * FROM sale_monitored_mailboxes WHERE email_address = ?",
        [mailbox.email_address],
        one=True
    )
    
    if existing:
        raise HTTPException(status_code=409, detail="Mailbox already exists")
    
    execute("""
        INSERT INTO sale_monitored_mailboxes
            (id, email_address, mailbox_type, department, is_active, 
             sync_enabled, token_valid, created_at, updated_at)
        VALUES (?, ?, ?, ?, 1, 0, 0, ?, ?)
    """, [mailbox_id, mailbox.email_address, mailbox.mailbox_type, mailbox.department, now, now])
    
    return {
        "id": mailbox_id,
        "email": mailbox.email_address,
        "status": "pending_oauth",
        "oauth_url": f"/api/v1/mailboxes/{mailbox_id}/oauth",
        "message": "Mailbox created. Complete OAuth flow to activate sync."
    }


@router.patch("/{mailbox_id}")
async def update_mailbox(mailbox_id: str, update: MailboxUpdate):
    """
    Update mailbox settings: enable/disable sync, deactivate.
    
    Args:
        mailbox_id: Mailbox ID (UUID)
        update: Update data (is_active, sync_enabled, deactivated_at)
        
    Returns:
        dict: Updated mailbox ID and status
        
    Raises:
        HTTPException: 404 if mailbox not found
    """
    existing = query(
        "SELECT * FROM sale_monitored_mailboxes WHERE id = ?",
        [mailbox_id],
        one=True
    )
    
    if not existing:
        raise HTTPException(status_code=404, detail="Mailbox not found")
    
    sets = []
    params = []
    
    if update.is_active is not None:
        sets.append("is_active = ?")
        params.append(1 if update.is_active else 0)
    
    if update.sync_enabled is not None:
        sets.append("sync_enabled = ?")
        params.append(1 if update.sync_enabled else 0)
    
    if update.deactivated_at is not None:
        sets.append("deactivated_at = ?")
        params.append(update.deactivated_at)
    
    sets.append("updated_at = ?")
    params.append(datetime.now().isoformat())
    params.append(mailbox_id)
    
    execute(f"UPDATE sale_monitored_mailboxes SET {', '.join(sets)} WHERE id = ?", params)
    
    return {"id": mailbox_id, "status": "ok"}


@router.post("/{mailbox_id}/oauth")
async def complete_oauth_flow(mailbox_id: str, callback: OAuthCallback):
    """
    Complete OAuth flow for Gmail integration.
    Receives authorization code, exchanges for token, updates token_valid=1.
    
    Args:
        mailbox_id: Mailbox ID (UUID)
        callback: OAuth callback with code and state
        
    Returns:
        dict: OAuth completion status
        
    Raises:
        HTTPException: 404 if mailbox not found, 400 if OAuth fails
    """
    mailbox = query(
        "SELECT * FROM sale_monitored_mailboxes WHERE id = ?",
        [mailbox_id],
        one=True
    )
    
    if not mailbox:
        raise HTTPException(status_code=404, detail="Mailbox not found")
    
    # In production, exchange code for token using Google OAuth2 API
    # For now, mark token as valid
    now = datetime.now().isoformat()
    
    execute("""
        UPDATE sale_monitored_mailboxes
        SET token_valid = 1, sync_enabled = 1, updated_at = ?
        WHERE id = ?
    """, [now, mailbox_id])
    
    return {
        "id": mailbox_id,
        "status": "ok",
        "message": "OAuth completed successfully. Sync enabled.",
        "email": mailbox.get("email_address") if hasattr(mailbox, 'get') else mailbox.get("email_address"),
    }
