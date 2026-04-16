"""
Opportunity models for IBS HI Sale Platform.
Defines schemas for sales pipeline opportunities.
"""

from pydantic import BaseModel
from typing import Optional


class OpportunityCreate(BaseModel):
    """Request schema for creating a new opportunity."""
    project_name: str
    customer_id: str
    product_group: str
    stage: str
    win_probability: float
    contract_value_usd: float
    weight_ton: Optional[float] = None
    specifications: Optional[str] = None
    technical_requirements: Optional[str] = None
    delivery_timeline: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "project_name": "Steel Tank Manufacturing",
                "customer_id": "cust-001",
                "product_group": "Storage Tanks",
                "stage": "RFQ_RECEIVED",
                "win_probability": 0.75,
                "contract_value_usd": 50000.00,
                "weight_ton": 25.5,
                "specifications": "ISO 1200 compliant",
                "technical_requirements": "Stainless steel 304",
                "delivery_timeline": "Q2 2026",
                "notes": "High priority client",
            }
        }


class OpportunityUpdate(BaseModel):
    """Request schema for updating an opportunity."""
    project_name: Optional[str] = None
    customer_id: Optional[str] = None
    product_group: Optional[str] = None
    stage: Optional[str] = None
    win_probability: Optional[float] = None
    contract_value_usd: Optional[float] = None
    weight_ton: Optional[float] = None
    specifications: Optional[str] = None
    technical_requirements: Optional[str] = None
    delivery_timeline: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "stage": "QUOTED",
                "win_probability": 0.85,
                "notes": "Customer approved technical specs",
            }
        }


class OpportunityResponse(BaseModel):
    """Response schema for opportunity data."""
    id: str
    project_name: str
    customer_id: str
    customer_name: str
    product_group: str
    stage: str
    win_probability: float
    contract_value_usd: float
    weight_ton: Optional[float]
    specifications: Optional[str]
    technical_requirements: Optional[str]
    delivery_timeline: Optional[str]
    notes: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
