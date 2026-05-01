"""Models for active contracts, milestones, settlements, change orders."""

from typing import Optional

from pydantic import BaseModel


class ActiveContractResponse(BaseModel):
    """Mirror of sale_active_contracts (14 rows)."""
    id: str
    po_number: str
    customer_name: str
    project_name: Optional[str] = None
    product_type: Optional[str] = None
    contract_status: Optional[str] = "ACTIVE"
    start_date: Optional[str] = None
    latest_activity: Optional[str] = None
    value_notes: Optional[str] = None
    project_manager: Optional[str] = None
    customer_id: Optional[str] = None
    source: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class ContractMilestoneResponse(BaseModel):
    """Mirror of sale_contract_milestones (55 rows)."""
    id: str
    opportunity_id: Optional[str] = None
    milestone_number: int
    milestone_type: str
    title: str
    description: Optional[str] = None
    planned_date: Optional[str] = None
    actual_date: Optional[str] = None
    weight_ton: Optional[float] = None
    invoice_amount_usd: Optional[float] = None
    invoice_amount_vnd: Optional[float] = None
    payment_term_days: Optional[int] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_status: Optional[str] = "NOT_INVOICED"
    payment_received_date: Optional[str] = None
    payment_amount: Optional[float] = None
    overdue_days: Optional[int] = 0
    penalty_amount: Optional[float] = None
    nas_contract_path: Optional[str] = None
    nas_invoice_path: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class SettlementResponse(BaseModel):
    """Mirror of sale_settlements (32 rows)."""
    id: str
    opportunity_id: Optional[str] = None
    settlement_date: Optional[str] = None
    settlement_status: Optional[str] = "OPEN"
    planned_value_usd: Optional[float] = None
    planned_weight_ton: Optional[float] = None
    planned_gm_pct: Optional[float] = None
    planned_gm_value: Optional[float] = None
    actual_revenue_usd: Optional[float] = None
    actual_weight_ton: Optional[float] = None
    actual_material_cost: Optional[float] = None
    actual_labor_cost: Optional[float] = None
    actual_overhead_cost: Optional[float] = None
    actual_subcontract_cost: Optional[float] = None
    actual_total_cost: Optional[float] = None
    actual_gm_pct: Optional[float] = None
    actual_gm_value: Optional[float] = None
    revenue_variance_usd: Optional[float] = None
    cost_variance_usd: Optional[float] = None
    gm_variance_pct: Optional[float] = None
    weight_variance_ton: Optional[float] = None
    total_invoiced: Optional[float] = None
    total_received: Optional[float] = None
    outstanding_amount: Optional[float] = None
    retention_held: Optional[float] = None
    retention_released: Optional[float] = None
    prepared_by: Optional[str] = None
    reviewed_by: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    lessons_learned: Optional[str] = None
    nas_file_path: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class ChangeOrderResponse(BaseModel):
    """Mirror of sale_change_orders."""
    id: str
    opportunity_id: Optional[str] = None
    change_order_number: int
    co_ref: Optional[str] = None
    change_type: str
    title: str
    description: Optional[str] = None
    requested_by: Optional[str] = None
    request_date: Optional[str] = None
    original_value_usd: Optional[float] = None
    revised_value_usd: Optional[float] = None
    delta_value_usd: Optional[float] = None
    original_weight_ton: Optional[float] = None
    revised_weight_ton: Optional[float] = None
    delta_weight_ton: Optional[float] = None
    impact_on_gm_pct: Optional[float] = None
    schedule_impact_days: Optional[int] = None
    status: Optional[str] = "DRAFT"
    approved_by_customer: Optional[str] = None
    approved_by_internal: Optional[str] = None
    approved_at: Optional[str] = None
    implemented_at: Optional[str] = None
    nas_file_path: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
