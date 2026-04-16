"""
Dashboard models for IBS HI Sale Platform.
Defines schemas for KPI and analytics responses.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class PipelineKPI(BaseModel):
    """Pipeline KPI metrics."""
    total_opportunities: int
    by_stage: Dict[str, int]
    total_value_usd: float
    weighted_value_usd: float
    avg_win_probability: float
    overdue_opportunities: int

    class Config:
        json_schema_extra = {
            "example": {
                "total_opportunities": 15,
                "by_stage": {
                    "PROSPECT": 3,
                    "RFQ_RECEIVED": 4,
                    "COSTING": 5,
                    "QUOTED": 2,
                    "NEGOTIATION": 1,
                },
                "total_value_usd": 250000.00,
                "weighted_value_usd": 198750.00,
                "avg_win_probability": 0.65,
                "overdue_opportunities": 2,
            }
        }


class TaskStats(BaseModel):
    """Task statistics."""
    total_tasks: int
    by_status: Dict[str, int]
    by_department: Dict[str, int]
    pending_tasks: int
    overdue_tasks: int
    avg_completion_time_hours: Optional[float]

    class Config:
        json_schema_extra = {
            "example": {
                "total_tasks": 42,
                "by_status": {
                    "PENDING": 15,
                    "IN_PROGRESS": 18,
                    "COMPLETED": 8,
                    "OVERDUE": 1,
                },
                "by_department": {
                    "TCKT": 12,
                    "KT": 10,
                    "QLDA": 8,
                    "QAQC": 7,
                    "SX": 5,
                },
                "pending_tasks": 15,
                "overdue_tasks": 1,
                "avg_completion_time_hours": 24.5,
            }
        }


class EmailStats(BaseModel):
    """Email statistics."""
    total_emails: int
    by_type: Dict[str, int]
    unclassified: int
    linked_to_opp: int
    avg_response_time_hours: Optional[float]
    today_received: int

    class Config:
        json_schema_extra = {
            "example": {
                "total_emails": 156,
                "by_type": {
                    "RFQ": 45,
                    "INQUIRY": 32,
                    "FOLLOW_UP": 28,
                    "QUOTATION_REQUEST": 25,
                    "OTHER": 26,
                },
                "unclassified": 5,
                "linked_to_opp": 98,
                "avg_response_time_hours": 4.2,
                "today_received": 12,
            }
        }


class DashboardSummary(BaseModel):
    """Complete dashboard summary."""
    pipeline: PipelineKPI
    tasks: TaskStats
    emails: EmailStats
    last_updated: str

    class Config:
        from_attributes = True
