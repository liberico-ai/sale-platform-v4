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


# ═══════════════════════════════════════════════════════════════
# CONTRACT STATUS TRANSITIONS (sale_active_contracts.contract_status)
# ═══════════════════════════════════════════════════════════════
#
# DRAFT → ACTIVE → IN_PROGRESS → COMPLETED → CLOSED
#                ↘ CANCELLED                ↘ ON_HOLD ↺
#
# DRAFT     = paperwork in progress, not yet signed
# ACTIVE    = signed, work not yet started
# IN_PROGRESS = production / delivery underway
# COMPLETED = work delivered, awaiting closeout
# CLOSED    = settled, no further activity
# CANCELLED = terminated before completion
# ON_HOLD   = paused (can resume to IN_PROGRESS)

CONTRACT_TRANSITIONS: Dict[str, Set[str]] = {
    "DRAFT":       {"ACTIVE", "CANCELLED"},
    "ACTIVE":      {"IN_PROGRESS", "ON_HOLD", "CANCELLED"},
    "IN_PROGRESS": {"COMPLETED", "ON_HOLD", "CANCELLED"},
    "ON_HOLD":     {"IN_PROGRESS", "CANCELLED"},
    "COMPLETED":   {"CLOSED"},
    "CLOSED":      set(),
    "CANCELLED":   set(),
}

CONTRACT_STATUSES = list(CONTRACT_TRANSITIONS.keys())


def validate_contract_transition(current_status: str, new_status: str) -> bool:
    """Validate a contract status transition.

    Raises:
        InvalidTransitionError: If the transition is not allowed.
        ValueError: If the status is not recognized.
    """
    cur = (current_status or "DRAFT").upper()
    new = (new_status or "").upper()
    if cur not in CONTRACT_TRANSITIONS:
        raise ValueError(f"Unknown contract status: {current_status}")
    if new not in CONTRACT_TRANSITIONS:
        raise ValueError(f"Unknown contract status: {new_status}")
    allowed = CONTRACT_TRANSITIONS[cur]
    if new not in allowed:
        raise InvalidTransitionError("contract_status", cur, new, allowed)
    return True


def get_allowed_contract_transitions(current_status: str) -> List[str]:
    cur = (current_status or "DRAFT").upper()
    return sorted(CONTRACT_TRANSITIONS.get(cur, set()))


# ═══════════════════════════════════════════════════════════════
# SETTLEMENT STATUS TRANSITIONS (sale_settlements.settlement_status)
# ═══════════════════════════════════════════════════════════════
#
# OPEN → IN_REVIEW → APPROVED → CLOSED
#      ↘                       ↗
#       CANCELLED (any non-terminal)

SETTLEMENT_TRANSITIONS: Dict[str, Set[str]] = {
    "OPEN":      {"IN_REVIEW", "CANCELLED"},
    "IN_REVIEW": {"APPROVED", "OPEN", "CANCELLED"},
    "APPROVED":  {"CLOSED", "IN_REVIEW"},
    "CLOSED":    set(),
    "CANCELLED": set(),
}

SETTLEMENT_STATUSES = list(SETTLEMENT_TRANSITIONS.keys())


def validate_settlement_transition(current_status: str, new_status: str) -> bool:
    cur = (current_status or "OPEN").upper()
    new = (new_status or "").upper()
    if cur not in SETTLEMENT_TRANSITIONS:
        raise ValueError(f"Unknown settlement status: {current_status}")
    if new not in SETTLEMENT_TRANSITIONS:
        raise ValueError(f"Unknown settlement status: {new_status}")
    allowed = SETTLEMENT_TRANSITIONS[cur]
    if new not in allowed:
        raise InvalidTransitionError("settlement_status", cur, new, allowed)
    return True


def get_allowed_settlement_transitions(current_status: str) -> List[str]:
    cur = (current_status or "OPEN").upper()
    return sorted(SETTLEMENT_TRANSITIONS.get(cur, set()))


# ═══════════════════════════════════════════════════════════════
# FOLLOW-UP STATUS TRANSITIONS (sale_follow_up_schedules.status)
# ═══════════════════════════════════════════════════════════════
#
# PENDING → IN_PROGRESS → COMPLETED
#         ↘                       ↘
#          RESCHEDULED → PENDING (cycle)
#         ↘ CANCELLED
#
# Aliases: SCHEDULED → PENDING, DONE → COMPLETED (legacy values).

FOLLOW_UP_TRANSITIONS: Dict[str, Set[str]] = {
    "PENDING":      {"IN_PROGRESS", "RESCHEDULED", "CANCELLED", "COMPLETED"},
    "IN_PROGRESS":  {"COMPLETED", "RESCHEDULED", "CANCELLED"},
    "RESCHEDULED":  {"PENDING"},
    "COMPLETED":    set(),
    "CANCELLED":    set(),
}

# Allow legacy values to flow through transparently.
FOLLOW_UP_ALIASES: Dict[str, str] = {
    "SCHEDULED": "PENDING",
    "DONE":      "COMPLETED",
}

FOLLOW_UP_STATUSES = list(FOLLOW_UP_TRANSITIONS.keys())


def _normalize_follow_up(status: str) -> str:
    s = (status or "PENDING").upper()
    return FOLLOW_UP_ALIASES.get(s, s)


def validate_follow_up_transition(current_status: str, new_status: str) -> bool:
    cur = _normalize_follow_up(current_status)
    new = _normalize_follow_up(new_status)
    if cur not in FOLLOW_UP_TRANSITIONS:
        raise ValueError(f"Unknown follow-up status: {current_status}")
    if new not in FOLLOW_UP_TRANSITIONS:
        raise ValueError(f"Unknown follow-up status: {new_status}")
    allowed = FOLLOW_UP_TRANSITIONS[cur]
    if new not in allowed:
        raise InvalidTransitionError("follow_up_status", cur, new, allowed)
    return True


def get_allowed_follow_up_transitions(current_status: str) -> List[str]:
    cur = _normalize_follow_up(current_status)
    return sorted(FOLLOW_UP_TRANSITIONS.get(cur, set()))


# ═══════════════════════════════════════════════════════════════
# COMMISSION STATUS TRANSITIONS (sale_commissions.status)
# ═══════════════════════════════════════════════════════════════
#
# CALCULATED → APPROVED → PAID
#            ↘ VOIDED
#
# APPROVED and PAID are admin-tier-only (gate enforced in router).

COMMISSION_TRANSITIONS: Dict[str, Set[str]] = {
    "CALCULATED": {"APPROVED", "VOIDED"},
    "APPROVED":   {"PAID", "CALCULATED"},  # back to CALCULATED for adjustment
    "PAID":       set(),
    "VOIDED":     set(),
}

# Status changes that require ADMIN tier (not just MANAGER).
COMMISSION_ADMIN_ONLY: Set[str] = {"APPROVED", "PAID"}

COMMISSION_STATUSES = list(COMMISSION_TRANSITIONS.keys())


def validate_commission_transition(current_status: str, new_status: str) -> bool:
    cur = (current_status or "CALCULATED").upper()
    new = (new_status or "").upper()
    if cur not in COMMISSION_TRANSITIONS:
        raise ValueError(f"Unknown commission status: {current_status}")
    if new not in COMMISSION_TRANSITIONS:
        raise ValueError(f"Unknown commission status: {new_status}")
    allowed = COMMISSION_TRANSITIONS[cur]
    if new not in allowed:
        raise InvalidTransitionError("commission_status", cur, new, allowed)
    return True


def get_allowed_commission_transitions(current_status: str) -> List[str]:
    cur = (current_status or "CALCULATED").upper()
    return sorted(COMMISSION_TRANSITIONS.get(cur, set()))


def commission_requires_admin(new_status: str) -> bool:
    """Check if transitioning to ``new_status`` needs ADMIN tier."""
    return (new_status or "").upper() in COMMISSION_ADMIN_ONLY
