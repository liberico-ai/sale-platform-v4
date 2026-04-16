"""IBS HI Sale Platform v4 - Services module.

Services provide core business logic for Gmail integration, email classification,
SLA monitoring, state machine validation, audit logging, and PM bridge synchronization.
"""

from .gmail_service import GmailService
from .classifier import classify_email, match_customer
from .sla_engine import get_sla_hours, calculate_due_date, ESCALATION_CHAIN
from .state_machine import (
    validate_opportunity_transition,
    validate_task_transition,
    get_allowed_opportunity_transitions,
    get_allowed_task_transitions,
)
from .audit import log_change, log_financial_change, log_status_change

# PM Bridge and KHKD Tracker imported on demand (Sprint 3)
# from .pm_bridge import PMBridge
# from .khkd_tracker import get_pipeline_vs_khkd

__all__ = [
    "GmailService",
    "classify_email",
    "match_customer",
    "get_sla_hours",
    "calculate_due_date",
    "ESCALATION_CHAIN",
    "validate_opportunity_transition",
    "validate_task_transition",
    "get_allowed_opportunity_transitions",
    "get_allowed_task_transitions",
    "log_change",
    "log_financial_change",
    "log_status_change",
]
