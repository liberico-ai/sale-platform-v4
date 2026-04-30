"""Models for sale_market_signals + sale_product_opportunities (Z4 — read-only)."""

from typing import Optional

from pydantic import BaseModel


class MarketSignalResponse(BaseModel):
    """Mirror of sale_market_signals (12 rows)."""
    id: str
    signal_type: str
    title: str
    description: Optional[str] = None
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    region: Optional[str] = None
    industry: Optional[str] = None
    competitor_name: Optional[str] = None
    relevance_score: Optional[float] = None
    impact_level: Optional[str] = "MEDIUM"
    related_product_group: Optional[str] = None
    related_customer_id: Optional[str] = None
    expires_at: Optional[str] = None
    is_actionable: Optional[int] = 1
    actioned_by: Optional[str] = None
    actioned_at: Optional[str] = None
    tags: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class ProductOpportunityResponse(BaseModel):
    """Mirror of sale_product_opportunities (51 rows)."""
    id: str
    product_category_id: Optional[str] = None
    customer_id: Optional[str] = None
    fit_score: Optional[float] = None
    capability_status: Optional[str] = "FULL"
    gap_description: Optional[str] = None
    past_project_count: Optional[int] = 0
    last_quoted_at: Optional[str] = None
    last_won_at: Optional[str] = None
    avg_unit_price: Optional[float] = None
    avg_gm_pct: Optional[float] = None
    total_revenue: Optional[float] = None
    total_weight_ton: Optional[float] = None
    competitor_threat: Optional[str] = None
    notes: Optional[str] = None
    is_strategic: Optional[int] = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
