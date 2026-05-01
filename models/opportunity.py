"""Opportunity models for IBS HI Sale Platform.

Field set mirrors sale_opportunities (schema_all.sql). Only `project_name`,
`product_group`, and `stage` are NOT NULL — everything else is Optional.
Routers carry their own inline Pydantic models for endpoint-specific shapes;
these are reusable canonical types for tooling.
"""

from pydantic import BaseModel
from typing import Optional


class OpportunityCreate(BaseModel):
    """Request schema for creating a new opportunity."""
    project_name: str
    product_group: str
    stage: Optional[str] = "PROSPECT"

    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    pl_hd: Optional[str] = None
    scope_en: Optional[str] = None
    scope_vn: Optional[str] = None

    win_probability: Optional[int] = 50
    weight_ton: Optional[float] = None
    contract_value_vnd: Optional[float] = None
    contract_value_usd: Optional[float] = None
    unit_price_usd: Optional[float] = None
    gm_percent: Optional[float] = None
    gm_value_usd: Optional[float] = None
    material_cost_usd: Optional[float] = None
    labor_cost_usd: Optional[float] = None
    subcontractor_cost_usd: Optional[float] = None
    profit_usd: Optional[float] = None

    estimated_signing: Optional[str] = None
    start_date: Optional[str] = None
    duration_months: Optional[int] = None
    end_date: Optional[str] = None
    quotation_date: Optional[str] = None

    qty_2025: Optional[float] = None
    value_2025: Optional[float] = None
    gp_2025: Optional[float] = None
    qty_2026: Optional[float] = None
    value_2026: Optional[float] = None
    gp_2026: Optional[float] = None

    milestones: Optional[str] = None
    assigned_to: Optional[str] = None
    nas_quotation_path: Optional[str] = None
    nas_contract_path: Optional[str] = None
    notes: Optional[str] = None
    loss_reason: Optional[str] = None
    competitor: Optional[str] = None


class OpportunityUpdate(BaseModel):
    """Request schema for updating an opportunity. All fields optional."""
    project_name: Optional[str] = None
    product_group: Optional[str] = None
    stage: Optional[str] = None
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    pl_hd: Optional[str] = None
    scope_en: Optional[str] = None
    scope_vn: Optional[str] = None
    win_probability: Optional[int] = None
    weight_ton: Optional[float] = None
    contract_value_vnd: Optional[float] = None
    contract_value_usd: Optional[float] = None
    unit_price_usd: Optional[float] = None
    gm_percent: Optional[float] = None
    gm_value_usd: Optional[float] = None
    material_cost_usd: Optional[float] = None
    labor_cost_usd: Optional[float] = None
    subcontractor_cost_usd: Optional[float] = None
    profit_usd: Optional[float] = None
    estimated_signing: Optional[str] = None
    start_date: Optional[str] = None
    duration_months: Optional[int] = None
    end_date: Optional[str] = None
    quotation_date: Optional[str] = None
    milestones: Optional[str] = None
    assigned_to: Optional[str] = None
    nas_quotation_path: Optional[str] = None
    nas_contract_path: Optional[str] = None
    notes: Optional[str] = None
    loss_reason: Optional[str] = None
    competitor: Optional[str] = None


class OpportunityResponse(BaseModel):
    """Response schema mirroring the persisted opportunity row."""
    id: str
    project_name: str
    product_group: str
    stage: str

    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    pl_hd: Optional[str] = None
    scope_en: Optional[str] = None
    scope_vn: Optional[str] = None

    win_probability: Optional[int] = None
    weight_ton: Optional[float] = None
    contract_value_vnd: Optional[float] = None
    contract_value_usd: Optional[float] = None
    unit_price_usd: Optional[float] = None
    gm_percent: Optional[float] = None
    gm_value_usd: Optional[float] = None
    material_cost_usd: Optional[float] = None
    labor_cost_usd: Optional[float] = None
    subcontractor_cost_usd: Optional[float] = None
    profit_usd: Optional[float] = None

    estimated_signing: Optional[str] = None
    start_date: Optional[str] = None
    duration_months: Optional[int] = None
    end_date: Optional[str] = None
    quotation_date: Optional[str] = None
    qty_2025: Optional[float] = None
    value_2025: Optional[float] = None
    gp_2025: Optional[float] = None
    qty_2026: Optional[float] = None
    value_2026: Optional[float] = None
    gp_2026: Optional[float] = None

    milestones: Optional[str] = None
    assigned_to: Optional[str] = None
    nas_quotation_path: Optional[str] = None
    nas_contract_path: Optional[str] = None
    notes: Optional[str] = None
    last_activity_date: Optional[str] = None
    stale_flag: Optional[int] = 0
    loss_reason: Optional[str] = None
    competitor: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
