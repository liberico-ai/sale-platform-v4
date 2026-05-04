"""Customer models for IBS HI Sale Platform.

Pilot for the models-consolidation pattern (UNIFIED step 5):
    - CustomerBase: shared fields, used by Create/Update/Response
    - CustomerCreate: required + optional fields for INSERT
    - CustomerUpdate: all fields optional for PATCH
    - CustomerResponse: full row mirror for GET responses

Routers import these instead of redefining inline (rule #16).
"""

from typing import Optional

from pydantic import BaseModel

from .enums import CustomerStatus


class CustomerBase(BaseModel):
    """Fields shared between create / update / response."""

    code: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    business_description: Optional[str] = None


class CustomerCreate(CustomerBase):
    """Request schema for creating a new customer.

    Schema (sale_customers): only ``name`` is NOT NULL. All other columns
    nullable. ``status`` defaults to ACTIVE.
    """

    name: str
    status: Optional[CustomerStatus] = CustomerStatus.ACTIVE


class CustomerUpdate(CustomerBase):
    """Request schema for updating a customer — every field optional."""

    name: Optional[str] = None
    status: Optional[CustomerStatus] = None


class CustomerResponse(CustomerBase):
    """Response schema for customer data — mirrors sale_customers."""

    id: str
    name: str
    status: Optional[CustomerStatus] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
