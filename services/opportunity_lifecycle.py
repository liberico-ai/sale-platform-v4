"""Opportunity lifecycle side-effects (UNIFIED Phase 2 step 3).

When an opportunity transitions to WON or LOST, several downstream
records need to be created or updated. Routers shouldn't hardcode
this — call into here so the logic stays consistent across the API,
the SPA's stage buttons, and any future automation.
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

import structlog

try:
    from ..database import query, execute
    from ..services.audit import log_change, log_status_change
    from ..services.notify import write_notification
except ImportError:
    from database import query, execute
    from services.audit import log_change, log_status_change
    from services.notify import write_notification

logger = structlog.get_logger(__name__)


# Default 3-milestone skeleton when an opportunity becomes a contract.
# Days are ISO offsets from contract creation; weights are share of value.
_DEFAULT_MILESTONES = [
    {"type": "SIGNING",  "title": "Contract signing",  "days": 0,  "share": 0.30},
    {"type": "KICKOFF",  "title": "Project kickoff",   "days": 14, "share": 0.30},
    {"type": "DELIVERY", "title": "Final delivery",    "days": 90, "share": 0.40},
]


def on_won(
    opportunity: Dict[str, Any],
    user_actor: str,
) -> Dict[str, Any]:
    """Run WON side effects: contract + milestones + commission + notify.

    Idempotent — if a contract already exists for this opportunity (by
    project_name + customer match), no new contract is created. Returns
    a summary of what was created so the caller can include it in the
    response payload.
    """
    opp_id = opportunity["id"]
    customer_id = opportunity.get("customer_id")
    customer_name = opportunity.get("customer_name") or ""
    project_name = opportunity.get("project_name") or "Unnamed Project"
    contract_value_usd = opportunity.get("contract_value_usd") or 0
    assigned_to = opportunity.get("assigned_to")

    summary: Dict[str, Any] = {
        "contract_id": None,
        "milestone_ids": [],
        "commission_id": None,
        "notifications": [],
    }

    # 1. Auto-create contract (if not already created for this opp)
    contract_id = _find_or_create_contract(
        opp_id, customer_id, customer_name, project_name,
        opportunity.get("product_group"),
        opportunity.get("start_date"),
        user_actor,
    )
    summary["contract_id"] = contract_id

    # 2. Skeleton milestones — only if opp has no existing milestones
    existing_ms = query(
        "SELECT COUNT(*) AS cnt FROM sale_contract_milestones WHERE opportunity_id = ?",
        [opp_id], one=True,
    ) or {}
    if (existing_ms.get("cnt") or 0) == 0:
        summary["milestone_ids"] = _create_default_milestones(
            opp_id, contract_value_usd, user_actor,
        )

    # 3. Commission auto-calc — only if salesperson present
    if assigned_to:
        summary["commission_id"] = _maybe_create_commission(
            opp_id, opportunity, assigned_to, user_actor,
        )

    # 4. Notifications: assigned_to + admin team
    if assigned_to:
        nid = write_notification(
            notification_type="OPPORTUNITY_WON",
            title=f"Won: {project_name}",
            message=(
                f"Customer: {customer_name} · "
                f"Value: ${contract_value_usd:,.0f} USD · "
                f"Contract: {contract_id}"
            ),
            user_id=assigned_to,
            entity_type="opportunity",
            entity_id=opp_id,
            severity="INFO",
        )
        if nid:
            summary["notifications"].append(nid)

    logger.info(
        "opportunity_won_side_effects",
        opp_id=opp_id,
        contract_id=contract_id,
        milestones=len(summary["milestone_ids"]),
        commission_id=summary["commission_id"],
    )
    return summary


def on_lost(
    opportunity: Dict[str, Any],
    loss_reason: str,
    competitor: Optional[str],
    user_actor: str,
) -> Dict[str, Any]:
    """Run LOST side effects: persist reason, cancel tasks, notify.

    ``loss_reason`` is required — the router must reject the request
    when it's missing. ``competitor`` is optional but recorded when
    provided so the win-loss analytics has full context.
    """
    opp_id = opportunity["id"]
    project_name = opportunity.get("project_name") or "Opportunity"
    assigned_to = opportunity.get("assigned_to")

    now = datetime.now().isoformat()
    execute(
        """
        UPDATE sale_opportunities
        SET loss_reason = ?, competitor = ?, updated_at = ?
        WHERE id = ?
        """,
        [loss_reason, competitor, now, opp_id],
    )

    # Audit the new loss fields explicitly so reports can trace them.
    log_change(
        "opportunity", opp_id, "UPDATE", "loss_reason",
        opportunity.get("loss_reason"), loss_reason,
        changed_by=user_actor,
    )
    if competitor:
        log_change(
            "opportunity", opp_id, "UPDATE", "competitor",
            opportunity.get("competitor"), competitor,
            changed_by=user_actor,
        )

    # Cancel any PENDING tasks tied to this opportunity. They no longer
    # have a downstream goal worth chasing.
    cancelled_tasks = _cancel_pending_tasks(opp_id, user_actor)

    summary = {
        "loss_reason": loss_reason,
        "competitor": competitor,
        "cancelled_task_count": cancelled_tasks,
        "notifications": [],
    }

    # Notify assigned AM so the loss appears in their queue.
    if assigned_to:
        nid = write_notification(
            notification_type="OPPORTUNITY_LOST",
            title=f"Lost: {project_name}",
            message=(
                f"Reason: {loss_reason}"
                + (f" · Competitor: {competitor}" if competitor else "")
            ),
            user_id=assigned_to,
            entity_type="opportunity",
            entity_id=opp_id,
            severity="WARN",
        )
        if nid:
            summary["notifications"].append(nid)

    logger.info(
        "opportunity_lost_side_effects",
        opp_id=opp_id,
        loss_reason=loss_reason,
        cancelled_tasks=cancelled_tasks,
    )
    return summary


# ─────────────────────────────────────────────────────────────────
# Internals
# ─────────────────────────────────────────────────────────────────

def _find_or_create_contract(
    opp_id: str,
    customer_id: Optional[str],
    customer_name: str,
    project_name: str,
    product_type: Optional[str],
    start_date: Optional[str],
    user_actor: str,
) -> str:
    """Look for an existing contract for this opportunity; create if absent.

    Match on (customer_id, project_name) — opportunities don't have a
    direct FK to contracts but the natural key works in practice.
    """
    if customer_id:
        existing = query(
            """
            SELECT id FROM sale_active_contracts
            WHERE customer_id = ? AND project_name = ?
            LIMIT 1
            """,
            [customer_id, project_name],
            one=True,
        )
        if existing:
            return existing["id"]

    contract_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    today = now[:10]
    po_number = f"CTR-{opp_id[:6].upper()}-{datetime.now().year}"

    execute(
        """
        INSERT INTO sale_active_contracts
            (id, po_number, customer_name, project_name, product_type,
             contract_status, start_date, latest_activity, customer_id,
             source, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 'ACTIVE', ?, ?, ?, 'OPPORTUNITY_WON', ?, ?)
        """,
        [
            contract_id, po_number, customer_name, project_name, product_type,
            start_date or today, today, customer_id, now, now,
        ],
    )

    log_status_change(
        "active_contract", contract_id, "", "ACTIVE",
        changed_by=user_actor,
    )
    return contract_id


def _create_default_milestones(
    opp_id: str,
    contract_value_usd: float,
    user_actor: str,
) -> list:
    """Insert 3 default milestones (SIGNING / KICKOFF / DELIVERY)."""
    now = datetime.now().isoformat()
    today = datetime.now().date()
    ids = []

    for idx, ms in enumerate(_DEFAULT_MILESTONES, start=1):
        ms_id = str(uuid.uuid4())
        planned_date = (today.toordinal() + ms["days"])
        # Convert ordinal back to ISO date.
        from datetime import date
        planned_iso = date.fromordinal(planned_date).isoformat()
        amount = round((contract_value_usd or 0) * ms["share"], 2)

        execute(
            """
            INSERT INTO sale_contract_milestones
                (id, opportunity_id, milestone_number, milestone_type,
                 title, planned_date, invoice_amount_usd, invoice_status,
                 payment_term_days, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'NOT_INVOICED', 30, ?, ?)
            """,
            [
                ms_id, opp_id, idx, ms["type"], ms["title"],
                planned_iso, amount, now, now,
            ],
        )
        ids.append(ms_id)
    return ids


def _maybe_create_commission(
    opp_id: str,
    opportunity: Dict[str, Any],
    salesperson: str,
    user_actor: str,
) -> Optional[str]:
    """Insert a CALCULATED commission row. Skips if one already exists.

    Uses a flat 0.5% standard rate as a placeholder — the commissions
    router has the full tier logic via /commissions/calculate. We avoid
    importing it here to keep the dependency direction one-way
    (services → no router imports).
    """
    existing = query(
        "SELECT id FROM sale_commissions WHERE opportunity_id = ?",
        [opp_id], one=True,
    )
    if existing:
        return existing["id"]

    contract_value = opportunity.get("contract_value_usd") or 0
    rate = 0.005  # 0.5% baseline — adjustable via /commissions/calculate later
    amount_usd = contract_value * rate
    fy = str(datetime.now().year)
    now = datetime.now().isoformat()
    cid = str(uuid.uuid4())

    execute(
        """
        INSERT INTO sale_commissions
            (id, opportunity_id, salesperson, fiscal_year,
             contract_value_usd, gm_value_usd, gm_percent,
             commission_tier, commission_rate,
             commission_amount_usd,
             status, calculation_date, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'STANDARD', ?, ?,
                'CALCULATED', ?, ?, ?)
        """,
        [
            cid, opp_id, salesperson, fy,
            contract_value, opportunity.get("gm_value_usd"),
            opportunity.get("gm_percent"),
            rate, amount_usd, now, now, now,
        ],
    )
    return cid


def _cancel_pending_tasks(opp_id: str, user_actor: str) -> int:
    """Cancel PENDING / IN_PROGRESS tasks tied to a lost opportunity.

    Returns number of tasks cancelled. Audit-logs each transition.
    """
    pending = query(
        """
        SELECT id, status FROM sale_tasks
        WHERE opportunity_id = ? AND status IN ('PENDING', 'IN_PROGRESS')
        """,
        [opp_id],
    )
    if not pending:
        return 0

    now = datetime.now().isoformat()
    for task in pending:
        execute(
            "UPDATE sale_tasks SET status = 'CANCELLED', updated_at = ? "
            "WHERE id = ?",
            [now, task["id"]],
        )
        log_status_change(
            "task", task["id"], task["status"], "CANCELLED",
            changed_by=user_actor,
        )
    return len(pending)
