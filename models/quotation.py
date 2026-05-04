"""Quotation models — sale_quotation_history (968) + sale_quotation_revisions (147).

Consolidated per UNIFIED step 5: Create/Update/Revise + history/revision
response shapes live here. Routers import these instead of defining inline.
"""

from typing import Optional

from pydantic import BaseModel

from .enums import QuotationStatus


class QuotationBase(BaseModel):
    """Fields shared between Create / Update."""

    project_name: Optional[str] = None
    customer_name: Optional[str] = None
    scope_of_work: Optional[str] = None
    weight_ton: Optional[float] = None
    price_usd_mt: Optional[float] = None
    value_vnd: Optional[float] = None
    value_usd: Optional[float] = None
    gross_profit_usd: Optional[float] = None
    gp_percent: Optional[float] = None
    date_offer: Optional[str] = None
    incharge: Optional[str] = None
    remark: Optional[str] = None
    owner: Optional[str] = None


class QuotationCreate(QuotationBase):
    """New quotation. Required: project_name + (customer_id|customer_code|customer_name).

    ``opportunity_id`` links the quote to an opportunity so WIN/LOSS on
    the quote can fan out to the opportunity (Phase 2 step 4).
    """

    project_name: str
    customer_id: Optional[str] = None
    customer_code: Optional[str] = None
    opportunity_id: Optional[str] = None
    country: Optional[str] = None
    market: Optional[str] = None
    product_type: Optional[str] = None
    launch_date: Optional[str] = None
    duration_months: Optional[float] = None


class QuotationUpdate(QuotationBase):
    """Update existing quotation. Status changes go through state machine."""

    status: Optional[QuotationStatus] = None


class QuotationRevise(BaseModel):
    """New revision. Attaches to opportunity_id of parent quotation or override."""

    revision_reason: Optional[str] = None
    opportunity_id: Optional[str] = None
    weight_ton: Optional[float] = None
    unit_price_usd: Optional[float] = None
    total_value_usd: Optional[float] = None
    total_value_vnd: Optional[float] = None
    material_cost: Optional[float] = None
    labor_cost: Optional[float] = None
    overhead_cost: Optional[float] = None
    gm_percent: Optional[float] = None
    gm_value: Optional[float] = None
    scope_summary: Optional[str] = None
    valid_until: Optional[str] = None
    sent_to: Optional[str] = None
    notes: Optional[str] = None


class QuotationResponse(BaseModel):
    """Response shape for sale_quotation_history rows."""

    id: str
    quotation_no: int
    customer_code: Optional[str] = None
    customer_name: Optional[str] = None
    country: Optional[str] = None
    market: Optional[str] = None
    product_type: Optional[str] = None
    project_name: Optional[str] = None
    scope_of_work: Optional[str] = None
    launch_date: Optional[str] = None
    duration_months: Optional[float] = None
    weight_ton: Optional[float] = None
    price_usd_mt: Optional[float] = None
    value_vnd: Optional[float] = None
    value_usd: Optional[float] = None
    gross_profit_usd: Optional[float] = None
    gp_percent: Optional[float] = None
    date_offer: Optional[str] = None
    incharge: Optional[str] = None
    status: Optional[QuotationStatus] = None
    remark: Optional[str] = None
    owner: Optional[str] = None
    customer_id: Optional[str] = None
    source: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


# Legacy alias kept for back-compat with imports in models/__init__.py.
QuotationHistoryResponse = QuotationResponse


class QuotationRevisionResponse(BaseModel):
    """Mirror of sale_quotation_revisions."""

    id: str
    opportunity_id: Optional[str] = None
    revision_number: int
    revision_date: str
    revision_reason: Optional[str] = None
    quotation_ref: Optional[str] = None
    weight_ton: Optional[float] = None
    unit_price_usd: Optional[float] = None
    total_value_usd: Optional[float] = None
    total_value_vnd: Optional[float] = None
    material_cost: Optional[float] = None
    labor_cost: Optional[float] = None
    overhead_cost: Optional[float] = None
    gm_percent: Optional[float] = None
    gm_value: Optional[float] = None
    scope_summary: Optional[str] = None
    price_delta_pct: Optional[float] = None
    nas_file_path: Optional[str] = None
    sent_to: Optional[str] = None
    sent_at: Optional[str] = None
    customer_response: Optional[str] = None
    response_date: Optional[str] = None
    valid_until: Optional[str] = None
    prepared_by: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
