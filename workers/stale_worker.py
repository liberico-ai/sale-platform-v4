"""Stale deal detector worker for IBS HI Sale Platform.

Runs daily at 8:00 AM via APScheduler.
Detects opportunities with no activity in >30 days and flags them.
Auto-creates CUSTOMER_FOLLOW_UP tasks for assigned sales person.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any

import structlog

try:
    from ..database import query, execute
except ImportError:
    from database import query, execute

logger = structlog.get_logger(__name__)

# Stages where staleness is relevant (active pipeline)
STALE_CHECK_STAGES = [
    "CONTACTED", "RFQ_RECEIVED", "COSTING", "QUOTED", "NEGOTIATION"
]

# Days without activity before flagging
STALE_THRESHOLD_DAYS = 30


def detect_stale_deals():
    """Detect and flag opportunities with >30 days no activity.

    Process:
    1. Query opportunities in active stages
    2. Check last_activity_date vs 30 day threshold
    3. Mark stale_flag = 1 for those exceeding threshold
    4. Create CUSTOMER_FOLLOW_UP task for assigned sales person
    """
    try:
        logger.info("stale_detection_start")

        threshold_date = (
            datetime.utcnow() - timedelta(days=STALE_THRESHOLD_DAYS)
        ).isoformat()

        # Build stage filter
        stage_placeholders = ", ".join(["?" for _ in STALE_CHECK_STAGES])

        stale_opps = query(f"""
            SELECT id, project_name, customer_name, assigned_to,
                   last_activity_date, stage, contract_value_usd
            FROM sale_opportunities
            WHERE stage IN ({stage_placeholders})
              AND last_activity_date < ?
              AND (stale_flag = 0 OR stale_flag IS NULL)
        """, STALE_CHECK_STAGES + [threshold_date])

        if not stale_opps:
            logger.debug("stale_detection_skip", reason="no_stale_deals")
            return

        logger.info("stale_deals_found", count=len(stale_opps))
        now = datetime.utcnow().isoformat()

        for opp in stale_opps:
            opp_id = opp["id"]

            # Calculate days inactive
            last_activity = opp.get("last_activity_date", "")
            try:
                last_dt = datetime.fromisoformat(
                    last_activity.replace("Z", "+00:00")
                )
                days_inactive = (datetime.utcnow() - last_dt).days
            except Exception:
                days_inactive = STALE_THRESHOLD_DAYS

            # Mark as stale
            execute("""
                UPDATE sale_opportunities
                SET stale_flag = 1, updated_at = ?
                WHERE id = ?
            """, [now, opp_id])

            logger.info("deal_flagged_stale",
                         opp_id=opp_id,
                         project=opp.get("project_name"),
                         days_inactive=days_inactive)

            # Create follow-up task
            task_id = str(uuid.uuid4())
            value = opp.get("contract_value_usd") or 0

            execute("""
                INSERT INTO sale_tasks
                    (id, opportunity_id, task_type, title, description,
                     from_dept, to_dept, assigned_to,
                     status, priority, created_at, updated_at)
                VALUES (?, ?, 'CUSTOMER_FOLLOW_UP', ?, ?,
                        'SALE', 'SALE', ?, 'PENDING', 'NORMAL', ?, ?)
            """, [
                task_id, opp_id,
                f"Follow-up: {opp.get('project_name', 'Unknown')} — "
                f"No activity for {days_inactive} days",
                f"Opportunity '{opp.get('project_name')}' for "
                f"{opp.get('customer_name')} "
                f"(${value:,.0f} USD) has not been updated in "
                f"{days_inactive} days.\n\n"
                f"Current stage: {opp.get('stage')}\n"
                f"Please reach out to customer to determine status.",
                opp.get("assigned_to", ""),
                now, now
            ])

            logger.info("followup_task_created",
                         task_id=task_id, opp_id=opp_id)

        logger.info("stale_detection_complete",
                     flagged=len(stale_opps))

    except Exception as e:
        logger.error("stale_detection_failed", error=str(e))


def reactivate_deal(opportunity_id: str) -> bool:
    """Clear stale flag when deal becomes active again.

    Called automatically when opportunity is updated.

    Args:
        opportunity_id: Opportunity ID to reactivate.

    Returns:
        True if successful.
    """
    try:
        execute("""
            UPDATE sale_opportunities
            SET stale_flag = 0, last_activity_date = ?, updated_at = ?
            WHERE id = ?
        """, [
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat(),
            opportunity_id
        ])
        logger.info("deal_reactivated", opp_id=opportunity_id)
        return True
    except Exception as e:
        logger.error("deal_reactivate_failed",
                      opp_id=opportunity_id, error=str(e))
        return False
