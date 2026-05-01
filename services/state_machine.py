"""State Machine for Opportunity Stages and Task Statuses.

Enforces valid state transitions per Liberico Engineering Rules:
"State transition qua function kiểm tra transition hợp lệ (state machine pattern)."
"""

from typing import Dict, List, Set


# ═══════════════════════════════════════════════════════════════
# OPPORTUNITY STAGE TRANSITIONS
# ═══════════════════════════════════════════════════════════════
#
# PROSPECT → CONTACTED → RFQ_RECEIVED → COSTING → QUOTED
#                                                      ↓
#                                               NEGOTIATION
#                                              ↙         ↘
#                                           WON           LOST
#                                            ↓             ↓
#                                       IN_PROGRESS    PROSPECT (reopen)

OPPORTUNITY_TRANSITIONS: Dict[str, Set[str]] = {
    "PROSPECT":      {"CONTACTED", "LOST"},
    "CONTACTED":     {"RFQ_RECEIVED", "LOST"},
    "RFQ_RECEIVED":  {"COSTING", "LOST"},
    "COSTING":       {"QUOTED", "LOST"},
    "QUOTED":        {"NEGOTIATION", "LOST"},
    "NEGOTIATION":   {"WON", "LOST"},
    "WON":           {"IN_PROGRESS"},
    "LOST":          {"PROSPECT"},       # Reopen
    "IN_PROGRESS":   set(),              # Terminal (managed by PM)
}

OPPORTUNITY_STAGES = list(OPPORTUNITY_TRANSITIONS.keys())


# ═══════════════════════════════════════════════════════════════
# TASK STATUS TRANSITIONS
# ═══════════════════════════════════════════════════════════════
#
# PENDING → IN_PROGRESS → COMPLETED
#     ↓         ↓    ↑
# CANCELLED  OVERDUE ─┘ (Resume)

TASK_TRANSITIONS: Dict[str, Set[str]] = {
    "PENDING":      {"IN_PROGRESS", "CANCELLED"},
    "IN_PROGRESS":  {"COMPLETED", "OVERDUE", "CANCELLED"},
    "OVERDUE":      {"IN_PROGRESS", "CANCELLED"},  # Resume or cancel
    "COMPLETED":    set(),                           # Terminal
    "CANCELLED":    set(),                           # Terminal
}

TASK_STATUSES = list(TASK_TRANSITIONS.keys())


# ═══════════════════════════════════════════════════════════════
# QUOTATION STATUS TRANSITIONS
# ═══════════════════════════════════════════════════════════════
#
# DRAFT → SENT → NEGOTIATION → WON
#                            → LOST → DRAFT (reopen)
#                            → EXPIRED → DRAFT (reopen)

QUOTATION_TRANSITIONS: Dict[str, Set[str]] = {
    "DRAFT":       {"SENT", "NEGOTIATION", "CANCELLED"},
    "SENT":        {"NEGOTIATION", "WON", "LOST", "EXPIRED"},
    "NEGOTIATION": {"WON", "LOST", "EXPIRED"},
    "WON":         set(),               # Terminal — promoted to contract
    "LOST":        {"DRAFT"},           # Reopen
    "EXPIRED":     {"DRAFT"},           # Reopen with new validity
    "CANCELLED":   set(),               # Terminal
}

QUOTATION_STATUSES = list(QUOTATION_TRANSITIONS.keys())


class InvalidTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""

    def __init__(self, entity_type: str, current: str, target: str, allowed: Set[str]):
        self.entity_type = entity_type
        self.current_state = current
        self.target_state = target
        self.allowed_states = allowed
        allowed_str = ", ".join(sorted(allowed)) if allowed else "none (terminal state)"
        super().__init__(
            f"Invalid {entity_type} transition: {current} → {target}. "
            f"Allowed transitions from {current}: {allowed_str}"
        )


def validate_opportunity_transition(current_stage: str, new_stage: str) -> bool:
    """Validate an opportunity stage transition.

    Args:
        current_stage: Current opportunity stage.
        new_stage: Target opportunity stage.

    Returns:
        True if the transition is valid.

    Raises:
        InvalidTransitionError: If the transition is not allowed.
        ValueError: If the stage is not recognized.
    """
    if current_stage not in OPPORTUNITY_TRANSITIONS:
        raise ValueError(f"Unknown opportunity stage: {current_stage}")
    if new_stage not in OPPORTUNITY_TRANSITIONS:
        raise ValueError(f"Unknown opportunity stage: {new_stage}")

    allowed = OPPORTUNITY_TRANSITIONS[current_stage]
    if new_stage not in allowed:
        raise InvalidTransitionError("opportunity_stage", current_stage, new_stage, allowed)

    return True


def validate_task_transition(current_status: str, new_status: str) -> bool:
    """Validate a task status transition.

    Args:
        current_status: Current task status.
        new_status: Target task status.

    Returns:
        True if the transition is valid.

    Raises:
        InvalidTransitionError: If the transition is not allowed.
        ValueError: If the status is not recognized.
    """
    if current_status not in TASK_TRANSITIONS:
        raise ValueError(f"Unknown task status: {current_status}")
    if new_status not in TASK_TRANSITIONS:
        raise ValueError(f"Unknown task status: {new_status}")

    allowed = TASK_TRANSITIONS[current_status]
    if new_status not in allowed:
        raise InvalidTransitionError("task_status", current_status, new_status, allowed)

    return True


def get_allowed_opportunity_transitions(current_stage: str) -> List[str]:
    """Get list of allowed next stages for an opportunity.

    Args:
        current_stage: Current opportunity stage.

    Returns:
        Sorted list of allowed next stages.
    """
    if current_stage not in OPPORTUNITY_TRANSITIONS:
        return []
    return sorted(OPPORTUNITY_TRANSITIONS[current_stage])


def get_allowed_task_transitions(current_status: str) -> List[str]:
    """Get list of allowed next statuses for a task.

    Args:
        current_status: Current task status.

    Returns:
        Sorted list of allowed next statuses.
    """
    if current_status not in TASK_TRANSITIONS:
        return []
    return sorted(TASK_TRANSITIONS[current_status])


def validate_quotation_transition(current_status: str, new_status: str) -> bool:
    """Validate a quotation status transition.

    Raises:
        InvalidTransitionError: If the transition is not allowed.
        ValueError: If the status is not recognized.
    """
    # Treat NULL/empty current as DRAFT for legacy rows that predate
    # the workflow status convention.
    cur = (current_status or "DRAFT").upper()
    new = (new_status or "").upper()

    if cur not in QUOTATION_TRANSITIONS:
        raise ValueError(f"Unknown quotation status: {current_status}")
    if new not in QUOTATION_TRANSITIONS:
        raise ValueError(f"Unknown quotation status: {new_status}")

    allowed = QUOTATION_TRANSITIONS[cur]
    if new not in allowed:
        raise InvalidTransitionError("quotation_status", cur, new, allowed)
    return True


def get_allowed_quotation_transitions(current_status: str) -> List[str]:
    """Get list of allowed next statuses for a quotation."""
    cur = (current_status or "DRAFT").upper()
    if cur not in QUOTATION_TRANSITIONS:
        return []
    return sorted(QUOTATION_TRANSITIONS[cur])
