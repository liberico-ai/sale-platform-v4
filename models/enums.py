"""Canonical enums for status / stage / type fields across the platform.

Pydantic models import from here instead of typing fields as ``Optional[str]``,
so the API rejects unknown values at validation time (HTTP 422) rather than
silently accepting garbage and letting it surface later as a state-machine
mystery.

The string values match exactly what's stored in SQL, so an enum member is
substitutable wherever the raw string is expected (each enum is ``str, Enum``).
"""

from enum import Enum


class OpportunityStage(str, Enum):
    """Pipeline stages — see services.state_machine for transitions."""

    PROSPECT = "PROSPECT"
    CONTACTED = "CONTACTED"
    RFQ_RECEIVED = "RFQ_RECEIVED"
    COSTING = "COSTING"
    QUOTED = "QUOTED"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    LOST = "LOST"
    IN_PROGRESS = "IN_PROGRESS"
    DELETED = "DELETED"


class TaskStatus(str, Enum):
    """Task lifecycle — see services.state_machine for transitions."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"


class EmailType(str, Enum):
    """Canonical 10 email types — must match config.EMAIL_TYPES exactly."""

    RFQ = "RFQ"
    TECHNICAL = "TECHNICAL"
    NEGOTIATION = "NEGOTIATION"
    CONTRACT = "CONTRACT"
    PAYMENT = "PAYMENT"
    FOLLOWUP = "FOLLOWUP"
    INTERNAL = "INTERNAL"
    VENDOR = "VENDOR"
    COMPLAINT = "COMPLAINT"
    GENERAL = "GENERAL"


class QuotationStatus(str, Enum):
    """sale_quotation_history.status values."""

    DRAFT = "DRAFT"
    SENT = "SENT"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    LOST = "LOST"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class FollowUpType(str, Enum):
    """sale_follow_up_schedules.schedule_type values."""

    CALL = "CALL"
    EMAIL = "EMAIL"
    VISIT = "VISIT"
    MEETING = "MEETING"


class NotificationType(str, Enum):
    """Notification categories surfaced in /notifications."""

    SLA_BREACH = "SLA_BREACH"
    STALE_DEAL = "STALE_DEAL"
    FOLLOWUP_DUE = "FOLLOWUP_DUE"
    QUOTATION_EXPIRING = "QUOTATION_EXPIRING"
    TASK_ASSIGNED = "TASK_ASSIGNED"
    ESCALATION = "ESCALATION"
    INTER_DEPT_ASSIGNED = "INTER_DEPT_ASSIGNED"


class CommissionStatus(str, Enum):
    """sale_commissions.status lifecycle."""

    CALCULATED = "CALCULATED"
    APPROVED = "APPROVED"
    PAID = "PAID"
    VOID = "VOID"


class CustomerStatus(str, Enum):
    """sale_customers.status — soft-delete is a status here."""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class ContractStatus(str, Enum):
    """sale_active_contracts.contract_status values."""

    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ON_HOLD = "ON_HOLD"


class InvoiceStatus(str, Enum):
    """sale_contract_milestones.invoice_status values."""

    NOT_INVOICED = "NOT_INVOICED"
    INVOICED = "INVOICED"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
