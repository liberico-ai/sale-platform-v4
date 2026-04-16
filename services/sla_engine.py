"""SLA monitoring engine for IBS HI Sale Platform.

Tracks task deadlines, defines SLA targets by task type,
and provides escalation chain logic.

Escalation chain: assigned_to → dept head → BD Director → ADMIN.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

import structlog

logger = structlog.get_logger(__name__)

# Default SLA targets by task type (in hours)
SLA_TARGETS: Dict[str, int] = {
    "COST_ESTIMATE": 48,
    "TECHNICAL_REVIEW": 24,
    "CAPACITY_CHECK": 24,
    "MATERIAL_PRICING": 48,
    "QUOTATION_REVIEW": 8,
    "CUSTOMER_FOLLOW_UP": 24,
    "PROJECT_HANDOFF": 72,
    "INVOICE_REQUEST": 4,
    "QUALITY_REVIEW": 48,
    "CONTRACT_REVIEW": 72,
    "GENERAL": 48,
}

# Escalation chain: role → next role
ESCALATION_CHAIN: Dict[str, str] = {
    "MEMBER": "MANAGER",
    "MANAGER": "BD_DIRECTOR",
    "BD_DIRECTOR": "ADMIN",
}


def get_sla_hours(task_type: str) -> int:
    """Get SLA target hours for task type.

    Args:
        task_type: Task type string (e.g., 'COST_ESTIMATE').

    Returns:
        Hours until due, or 48 hours if type not found.
    """
    return SLA_TARGETS.get(task_type, 48)


def calculate_due_date(
    task_type: str,
    start_date: Optional[datetime] = None,
) -> str:
    """Calculate due date based on task type SLA.

    Args:
        task_type: Task type.
        start_date: When to start counting (defaults to now).

    Returns:
        ISO format due date string.
    """
    if start_date is None:
        start_date = datetime.utcnow()

    sla_hours = get_sla_hours(task_type)
    due_dt = start_date + timedelta(hours=sla_hours)
    return due_dt.isoformat()


def get_next_escalation(current_role: str) -> Optional[str]:
    """Get next escalation target for a role.

    Args:
        current_role: Current assigned role.

    Returns:
        Next role in escalation chain, or None if at top.
    """
    return ESCALATION_CHAIN.get(current_role)


def get_escalation_path(role: str) -> List[str]:
    """Get full escalation path starting from a role.

    Args:
        role: Starting role.

    Returns:
        List of roles from current to final escalation.
    """
    chain = [role]
    current = role
    while current in ESCALATION_CHAIN:
        current = ESCALATION_CHAIN[current]
        chain.append(current)
    return chain
