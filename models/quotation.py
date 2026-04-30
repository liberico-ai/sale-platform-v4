"""Models for quotation history + revisions.

- sale_quotation_history (968): historical xlsx import (one row = one quote)
- sale_quotation_revisions (147): opportunity-scoped revision log
"""

from typing import Optional

from pydantic import BaseModel


class QuotationHistoryResponse(BaseModel):
    """Mirror of sale_quotation_history."""
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
    status: Optional[str] = None
    remark: Optional[str] = None
    owner: Optional[str] = None
    customer_id: Optional[str] = None
    source: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


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
