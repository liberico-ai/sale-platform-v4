"""Audit logging service for IBS HI Sale Platform.

Logs changes to financial fields, status transitions, and role changes
per Liberico Engineering Rules:
"CREATE/UPDATE/DELETE trên bảng tài chính → ghi audit log."
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

try:
    from ..database import execute
except ImportError:
    from database import execute


def log_change(
    entity_type: str,
    entity_id: str,
    action: str,
    field_name: str,
    old_value: Any,
    new_value: Any,
    changed_by: Optional[str] = None,
) -> str:
    """Log a single field change to the audit trail.

    Args:
        entity_type: Type of entity (e.g., 'opportunity', 'task', 'user_role').
        entity_id: ID of the entity being changed.
        action: Change action (e.g., 'UPDATE', 'CREATE', 'DELETE').
        field_name: Name of the field that changed.
        old_value: Previous value (None for CREATE).
        new_value: New value (None for DELETE).
        changed_by: User or API key tier that made the change.

    Returns:
        Audit log entry ID.
    """
    log_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute("""
        INSERT INTO sale_audit_log
            (id, entity_type, entity_id, action, field_name,
             old_value, new_value, changed_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        log_id, entity_type, entity_id, action, field_name,
        str(old_value) if old_value is not None else None,
        str(new_value) if new_value is not None else None,
        changed_by, now
    ])

    return log_id


def log_financial_change(
    entity_type: str,
    entity_id: str,
    changes: Dict[str, tuple],
    changed_by: Optional[str] = None,
) -> int:
    """Log multiple financial field changes in one batch.

    Args:
        entity_type: Type of entity (e.g., 'opportunity').
        entity_id: ID of the entity.
        changes: Dict of {field_name: (old_value, new_value)}.
        changed_by: User who made changes.

    Returns:
        Number of audit entries created.
    """
    count = 0
    for field_name, (old_val, new_val) in changes.items():
        if old_val != new_val:
            log_change(entity_type, entity_id, "UPDATE",
                       field_name, old_val, new_val, changed_by)
            count += 1
    return count


def log_status_change(
    entity_type: str,
    entity_id: str,
    old_status: str,
    new_status: str,
    changed_by: Optional[str] = None,
) -> str:
    """Log a status/stage transition.

    Args:
        entity_type: Type of entity (e.g., 'opportunity', 'task').
        entity_id: ID of the entity.
        old_status: Previous status/stage.
        new_status: New status/stage.
        changed_by: User who triggered the transition.

    Returns:
        Audit log entry ID.
    """
    return log_change(
        entity_type, entity_id, "STATUS_CHANGE",
        "status" if entity_type == "task" else "stage",
        old_status, new_status, changed_by
    )


# Financial fields that trigger audit logging
AUDITED_OPPORTUNITY_FIELDS = {
    "contract_value_vnd", "contract_value_usd", "unit_price_usd",
    "gm_value_usd", "material_cost_usd", "labor_cost_usd",
    "subcontractor_cost_usd", "profit_usd", "win_probability",
    "stage", "assigned_to",
}
