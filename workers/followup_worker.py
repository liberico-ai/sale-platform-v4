"""Follow-up reminder worker for IBS HI Sale Platform.

Runs daily at 7:00 AM via APScheduler. Looks at sale_follow_up_schedules
and writes notifications for follow-ups that are:
  - due today (PENDING + date(next_follow_up) = today)
  - overdue (PENDING + next_follow_up < now)

Dedupe in services.notify keeps re-runs from spamming the same row.
"""

from datetime import datetime

import structlog

try:
    from ..database import query
    from ..services.notify import write_notification
except ImportError:
    from database import query
    from services.notify import write_notification

logger = structlog.get_logger(__name__)


def check_followups():
    """Surface PENDING follow-ups that are due today or overdue."""
    try:
        logger.info("followup_check_start")

        rows = query(
            """
            SELECT f.id, f.opportunity_id, f.assigned_to, f.next_follow_up,
                   f.schedule_type, f.status,
                   o.project_name, c.name AS customer_name
            FROM sale_follow_up_schedules f
            LEFT JOIN sale_opportunities o ON o.id = f.opportunity_id
            LEFT JOIN sale_customers c ON c.id = f.customer_id
            WHERE f.status = 'PENDING'
              AND f.next_follow_up <= datetime('now', '+1 day')
            ORDER BY f.next_follow_up ASC
            """
        )

        if not rows:
            logger.debug("followup_check_skip", reason="no_due_followups")
            return

        now = datetime.utcnow()
        notified = 0

        for row in rows:
            next_str = row.get("next_follow_up") or ""
            try:
                next_dt = datetime.fromisoformat(next_str.replace("Z", "+00:00"))
            except Exception:
                next_dt = now

            is_overdue = next_dt < now
            severity = "WARN" if is_overdue else "INFO"
            label = "Overdue follow-up" if is_overdue else "Follow-up due today"
            project = row.get("project_name") or "(unknown opportunity)"
            customer = row.get("customer_name") or ""

            result = write_notification(
                notification_type="FOLLOWUP_DUE",
                title=f"{label}: {row.get('schedule_type') or 'follow-up'} — {project}",
                message=(
                    f"Customer: {customer} · scheduled {next_str} · "
                    f"opportunity: {project}"
                ),
                user_id=row.get("assigned_to"),
                entity_type="follow_up",
                entity_id=row["id"],
                severity=severity,
            )
            if result:
                notified += 1

        logger.info("followup_check_complete",
                     checked=len(rows), notified=notified)

    except Exception as exc:
        logger.error("followup_check_failed", error=str(exc))
