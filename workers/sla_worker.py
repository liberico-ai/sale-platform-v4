"""SLA monitoring worker for IBS HI Sale Platform.

Runs every 15 minutes via APScheduler.
Checks for overdue tasks and auto-escalates through chain:
assigned_to → dept head → BD_DIRECTOR.
"""

from datetime import datetime
from typing import Dict, List, Any

import structlog

try:
    from ..database import query, execute
    from ..services.sla_engine import ESCALATION_CHAIN
    from ..services.audit import log_status_change
    from ..services.notify import write_notification
except ImportError:
    from database import query, execute
    from services.sla_engine import ESCALATION_CHAIN
    from services.audit import log_status_change
    from services.notify import write_notification

logger = structlog.get_logger(__name__)


def check_sla():
    """Check SLA compliance and escalate overdue tasks.

    Process:
    1. Query all non-completed tasks with due_date
    2. Identify those past due_date
    3. Mark as OVERDUE status (with audit log)
    4. Escalate to next level in chain
    """
    try:
        logger.info("sla_check_start")

        tasks = query("""
            SELECT id, task_type, due_date, status, assigned_to,
                   escalation_count, to_dept
            FROM sale_tasks
            WHERE status NOT IN ('COMPLETED', 'CANCELLED')
              AND due_date IS NOT NULL
            ORDER BY due_date ASC
        """)

        if not tasks:
            logger.debug("sla_check_skip", reason="no_active_tasks")
            return

        now = datetime.utcnow()
        overdue_count = 0
        escalated_count = 0

        for task in tasks:
            due_date = task.get("due_date")
            if not due_date:
                continue

            # Parse due_date
            try:
                if isinstance(due_date, str):
                    due_dt = datetime.fromisoformat(
                        due_date.replace("Z", "+00:00")
                    )
                else:
                    due_dt = due_date
            except Exception:
                continue

            # Check if overdue
            if now > due_dt:
                task_id = task["id"]
                current_status = task.get("status", "PENDING")

                if current_status != "OVERDUE":
                    # Mark as overdue
                    execute(
                        "UPDATE sale_tasks SET status = 'OVERDUE', updated_at = ? WHERE id = ?",
                        [now.isoformat(), task_id]
                    )
                    log_status_change("task", task_id, current_status, "OVERDUE",
                                      changed_by="SLA_WORKER")
                    overdue_count += 1
                    logger.info("task_marked_overdue", task_id=task_id)

                    # Notification — first time we flip a task to OVERDUE
                    write_notification(
                        notification_type="SLA_OVERDUE",
                        title=f"Task overdue: {task.get('task_type') or 'task'}",
                        message=f"Due {task.get('due_date')} — please action or escalate.",
                        user_id=task.get("assigned_to"),
                        entity_type="task",
                        entity_id=task_id,
                        severity="WARN",
                    )

                # Escalate if not yet at max level
                escalation_count = task.get("escalation_count", 0) or 0
                if escalation_count < 3:
                    assigned_to = task.get("assigned_to", "")
                    next_role = ESCALATION_CHAIN.get(assigned_to)

                    if next_role:
                        new_count = escalation_count + 1
                        execute("""
                            UPDATE sale_tasks
                            SET is_escalated = 1, escalation_count = ?,
                                escalated_to = ?, escalated_at = ?,
                                updated_at = ?
                            WHERE id = ?
                        """, [new_count, next_role, now.isoformat(),
                              now.isoformat(), task_id])

                        escalated_count += 1
                        logger.info("task_escalated",
                                     task_id=task_id,
                                     from_role=assigned_to,
                                     to_role=next_role,
                                     escalation_count=new_count)

        logger.info("sla_check_complete",
                     overdue=overdue_count,
                     escalated=escalated_count,
                     checked=len(tasks))

    except Exception as e:
        logger.error("sla_check_failed", error=str(e))


def get_sla_report() -> Dict[str, Any]:
    """Generate SLA performance report.

    Returns:
        Dict with overdue/pending/completion metrics.
    """
    try:
        stats = query("""
            SELECT
                COUNT(CASE WHEN status = 'OVERDUE' THEN 1 END) as overdue_count,
                COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pending_count,
                COUNT(CASE WHEN status = 'IN_PROGRESS' THEN 1 END) as in_progress_count,
                COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed_count,
                COUNT(*) as total_count
            FROM sale_tasks
            WHERE status NOT IN ('CANCELLED')
        """, one=True)

        if not stats:
            return {}

        completed = stats.get("completed_count", 0) or 0
        total = stats.get("total_count", 0) or 0
        overdue = stats.get("overdue_count", 0) or 0

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "overdue_count": overdue,
            "pending_count": stats.get("pending_count", 0),
            "in_progress_count": stats.get("in_progress_count", 0),
            "completed_count": completed,
            "total_count": total,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 1),
            "health": "OK" if overdue < max(total * 0.1, 1) else "WARNING",
        }
    except Exception as e:
        logger.error("sla_report_failed", error=str(e))
        return {}
