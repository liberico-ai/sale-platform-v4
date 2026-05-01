"""Models for sale_customer_contacts (2,990 records)."""

from typing import Optional

from pydantic import BaseModel


class CustomerContactCreate(BaseModel):
    """Required: customer_id + name. Everything else nullable."""
    customer_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    linkedin: Optional[str] = None
    is_primary: Optional[bool] = False


class CustomerContactUpdate(BaseModel):
    """All fields optional. customer_id immutable — use POST to move."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    linkedin: Optional[str] = None
    is_primary: Optional[bool] = None


class CustomerContactResponse(BaseModel):
    """Mirror of sale_customer_contacts."""
    id: str
    customer_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    linkedin: Optional[str] = None
    is_primary: Optional[int] = 0
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
