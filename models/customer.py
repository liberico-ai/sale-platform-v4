"""
Customer models for IBS HI Sale Platform.
Defines schemas for customer data management.
"""

from pydantic import BaseModel
from typing import Optional


class CustomerCreate(BaseModel):
    """Request schema for creating a new customer.

    Schema (sale_customers): only `name` is NOT NULL. All other columns
    nullable.
    """
    name: str
    code: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    business_description: Optional[str] = None
    status: Optional[str] = "ACTIVE"


class CustomerUpdate(BaseModel):
    """Request schema for updating a customer."""
    name: Optional[str] = None
    code: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    business_description: Optional[str] = None
    status: Optional[str] = None


class CustomerResponse(BaseModel):
    """Response schema for customer data."""
    id: str
    name: str
    code: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    business_description: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
