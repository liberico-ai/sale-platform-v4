"""Follow-up schedule worker for IBS HI Sale Platform.

Runs every 60 minutes via APScheduler.
Checks sale_follow_up_schedules for due follow-ups, creates tasks,
and advances the reminder schedule (e.g. [3, 7, 14, 30] days).

Deactivates schedules when the opportunity leaves QUOTED/NEGOTIATION
or when all reminders are exhausted.
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

import structlog

try:
    from ..database import query, execute
except ImportError:
    from database import query, execute

logger = structlog.get_logger(__name__)


def process_follow_ups():
    """Check due follow-up schedules and create tasks.

    Process:
    1. Query active schedules where next_follow_up <= now
    2. Join with sale_opportunities for context
    3. Skip/deactivate if opportunity not in QUOTED or NEGOTIATION
    4. Create CUSTOMER_FOLLOW_UP task with 24h SLA
    5. Advance reminder_days array; deactivate if exhausted
    """
    try:
        now = datetime.utcnow().isoformat()

        due_schedules = query("""
            SELECT
                s.id AS schedule_id,
                s.opportunity_id,
                s.reminder_days,
                s.follow_up_count,
                s.schedule_type,
                o.assigned_to,
                o.project_name,
                o.customer_name,
                o.stage
            FROM sale_follow_up_schedules s
            JOIN sale_opportunities o ON o.id = s.opportunity_id
            WHERE s.is_active = 1
              AND s.next_follow_up <= ?
        """, [now])

        if not due_schedules:
            logger.debug("followup_worker_skip", reason="no_due_schedules")
            return

        logger.info("followup_worker_start", due_count=len(due_schedules))

        created = 0
        deactivated = 0

        for schedule in due_schedules:
            result = _process_single_schedule(schedule)
            if result == "created":
                created += 1
            elif result == "deactivated":
                deactivated += 1

        logger.info(
            "followup_worker_complete",
            tasks_created=created,
            schedules_deactivated=deactivated,
        )

    except Exception as e:
        logger.error("followup_worker_failed", error=str(e))


def _process_single_schedule(schedule: Dict[str, Any]) -> str:
    """Process a single due follow-up schedule.

    Returns:
        'created' if a task was created, 'deactivated' if schedule was
        deactivated, or 'error' on failure.
    """
    schedule_id = schedule["schedule_id"]
    opp_id = schedule["opportunity_id"]
    stage = schedule.get("stage", "")
    project_name = schedule.get("project_name", "Unknown")

    try:
        # Deactivate if opportunity is no longer in a follow-up-eligible stage
        if stage not in ("QUOTED", "NEGOTIATION"):
            execute(
                "UPDATE sale_follow_up_schedules SET is_active = 0, updated_at = ? WHERE id = ?",
                [datetime.utcnow().isoformat(), schedule_id],
            )
            logger.info(
                "followup_schedule_deactivated",
                schedule_id=schedule_id,
                reason="stage_not_eligible",
                stage=stage,
            )
            return "deactivated"

        # Parse reminder_days
        reminder_days_raw = schedule.get("reminder_days", "[]")
        if isinstance(reminder_days_raw, str):
            reminder_days = json.loads(reminder_days_raw)
        else:
            reminder_days = reminder_days_raw

        follow_up_count = schedule.get("follow_up_count", 0) or 0

        # Create the follow-up task
        task_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        execute("""
            INSERT INTO sale_tasks
                (id, opportunity_id, task_type, title, description,
                 assigned_to, status, priority, sla_hours,
                 created_at, updated_at)
            VALUES (?, ?, 'CUSTOMER_FOLLOW_UP', ?, ?, ?, 'PENDING', 'NORMAL', 24, ?, ?)
        """, [
            task_id,
            opp_id,
            f"Follow-up #{follow_up_count + 1}: {project_name}",
            (
                f"Scheduled follow-up for {project_name} "
                f"(customer: {schedule.get('customer_name', 'N/A')}, "
                f"stage: {stage}). "
                f"Schedule type: {schedule.get('schedule_type', 'POST_QUOTATION')}."
            ),
            schedule.get("assigned_to"),
            now,
            now,
        ])

        logger.info(
            "followup_task_created",
            task_id=task_id,
            schedule_id=schedule_id,
            opp_id=opp_id,
            follow_up_number=follow_up_count + 1,
        )

        # Advance the schedule
        new_count = follow_up_count + 1
        next_index = new_count  # index into reminder_days for the NEXT reminder

        if next_index < len(reminder_days):
            # Calculate next follow-up from now + reminder_days[next_index]
            days_ahead = reminder_days[next_index]
            next_follow_up = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat()

            execute("""
                UPDATE sale_follow_up_schedules
                SET follow_up_count = ?, next_follow_up = ?, updated_at = ?
                WHERE id = ?
            """, [new_count, next_follow_up, datetime.utcnow().isoformat(), schedule_id])

            logger.info(
                "followup_schedule_advanced",
                schedule_id=schedule_id,
                next_follow_up=next_follow_up,
                next_reminder_day=days_ahead,
            )
        else:
            # All reminders exhausted — deactivate
            execute("""
                UPDATE sale_follow_up_schedules
                SET follow_up_count = ?, is_active = 0, updated_at = ?
                WHERE id = ?
            """, [new_count, datetime.utcnow().isoformat(), schedule_id])

            logger.info(
                "followup_schedule_exhausted",
                schedule_id=schedule_id,
                total_follow_ups=new_count,
            )

        return "created"

    except Exception as e:
        logger.error(
            "followup_schedule_error",
            schedule_id=schedule_id,
            opp_id=opp_id,
            error=str(e),
        )
        return "error"
