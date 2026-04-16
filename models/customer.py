"""
Customer models for IBS HI Sale Platform.
Defines schemas for customer data management.
"""

from pydantic import BaseModel
from typing import Optional


class CustomerCreate(BaseModel):
    """Request schema for creating a new customer."""
    name: str
    code: str
    country: str
    region: str
    status: str = "ACTIVE"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Acme Corp",
                "code": "ACME001",
                "country": "Vietnam",
                "region": "Ho Chi Minh City",
                "status": "ACTIVE",
            }
        }


class CustomerUpdate(BaseModel):
    """Request schema for updating a customer."""
    name: Optional[str] = None
    code: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    status: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Acme Corp Updated",
                "status": "INACTIVE",
            }
        }


class CustomerResponse(BaseModel):
    """Response schema for customer data."""
    id: str
    name: str
    code: str
    country: str
    region: str
    status: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
