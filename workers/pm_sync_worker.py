"""PM sync worker for Sale ↔ ibshi1 bidirectional synchronization.

Runs every 10 minutes via APScheduler.
Polls ibshi1 for changes on active projects linked to WON/IN_PROGRESS opportunities.
Detects milestone completions → auto-draft customer email (DRAFT only).
Detects overdue PM tasks → create Sale follow-up task.
All syncs logged to sale_pm_sync_log.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

import structlog

try:
    from ..database import query, execute
    from ..services.pm_bridge import PMBridge
except ImportError:
    from database import query, execute
    from services.pm_bridge import PMBridge

logger = structlog.get_logger(__name__)


async def sync_from_pm():
    """Poll ibshi1 for changes on active projects linked to opportunities.

    Process:
    1. Get active opportunities with project_code (WON, IN_PROGRESS)
    2. Fetch project status from ibshi1
    3. Detect milestone completions → draft customer email
    4. Detect overdue PM tasks → create Sale follow-up task
    5. Log all syncs to sale_pm_sync_log
    """
    try:
        logger.info("pm_sync_start")

        bridge = PMBridge()

        active_opps = query("""
            SELECT id, project_code, customer_name, customer_email,
                   project_name, assigned_to
            FROM sale_opportunities
            WHERE stage IN ('WON', 'IN_PROGRESS')
              AND project_code IS NOT NULL
        """)

        if not active_opps:
            logger.debug("pm_sync_skip", reason="no_active_projects")
            return

        logger.info("pm_sync_projects", count=len(active_opps))

        for opp in active_opps:
            await _sync_project(bridge, opp)

        logger.info("pm_sync_complete")

    except Exception as e:
        logger.error("pm_sync_failed", error=str(e))


async def _sync_project(bridge: PMBridge, opportunity: Dict[str, Any]):
    """Sync single project from PM."""
    project_code = opportunity.get("project_code")
    opp_id = opportunity["id"]

    logger.info("pm_project_sync", project_code=project_code)

    try:
        status = await bridge.get_project_status(project_code)
        if not status:
            logger.warning("pm_project_fetch_failed",
                            project_code=project_code)
            return

        # Check milestones for completions
        milestones = status.get("milestones", [])
        for milestone in milestones:
            if milestone.get("status") == "COMPLETED":
                await _handle_milestone_completion(bridge, opportunity, milestone)

        # Check tasks for overdue items
        tasks_summary = status.get("tasks_summary", {})
        if tasks_summary.get("overdue", 0) > 0:
            await _handle_overdue_tasks(opportunity, tasks_summary)

    except Exception as e:
        logger.error("pm_project_sync_error",
                      project_code=project_code, error=str(e))


async def _handle_milestone_completion(
    bridge: PMBridge,
    opportunity: Dict[str, Any],
    milestone: Dict[str, Any],
):
    """Handle milestone completion — draft customer email (NEVER auto-send)."""
    try:
        milestone_id = milestone.get("id", "")

        # Check if already synced
        existing = query("""
            SELECT id FROM sale_pm_sync_log
            WHERE project_code = ? AND sync_type = 'MILESTONE_UPDATE'
              AND payload LIKE ?
        """, [opportunity["project_code"], f"%{milestone_id}%"], one=True)

        if existing:
            return

        logger.info("pm_milestone_completed",
                      project_code=opportunity["project_code"],
                      milestone=milestone.get("name"))

        # Draft reply email (status=DRAFT, requires_review=True)
        draft = await bridge.draft_reply_email(
            opportunity["id"],
            context=f"Milestone: {milestone.get('name')}",
            template_type="MILESTONE_UPDATE",
        )

        if draft:
            logger.info("pm_draft_for_milestone",
                          customer=opportunity.get("customer_name"),
                          milestone=milestone.get("name"))

    except Exception as e:
        logger.error("pm_milestone_error",
                      project_code=opportunity.get("project_code"),
                      error=str(e))


async def _handle_overdue_tasks(
    opportunity: Dict[str, Any],
    tasks_summary: Dict[str, int],
):
    """Handle overdue PM tasks — create Sale follow-up task."""
    try:
        overdue_count = tasks_summary.get("overdue", 0)
        if overdue_count <= 0:
            return

        # Throttle: don't create if one was created in last 30 minutes
        existing = query("""
            SELECT id FROM sale_tasks
            WHERE opportunity_id = ? AND task_type = 'PROJECT_HANDOFF'
              AND created_at > datetime('now', '-30 minutes')
        """, [opportunity["id"]], one=True)

        if existing:
            return

        now = datetime.utcnow().isoformat()
        task_id = str(uuid.uuid4())

        execute("""
            INSERT INTO sale_tasks
                (id, opportunity_id, task_type, title, description,
                 from_dept, to_dept, assigned_to,
                 status, priority, created_at, updated_at)
            VALUES (?, ?, 'PROJECT_HANDOFF', ?, ?,
                    'PM', 'SALE', ?,
                    'PENDING', 'HIGH', ?, ?)
        """, [
            task_id, opportunity["id"],
            f"PM: {overdue_count} overdue task(s) — {opportunity.get('project_name', '')}",
            f"The PM team has {overdue_count} overdue task(s) "
            f"on project {opportunity.get('project_code')}.\n"
            f"Please coordinate with PM to resolve delays.",
            opportunity.get("assigned_to", ""),
            now, now,
        ])

        # Log sync
        execute("""
            INSERT INTO sale_pm_sync_log
                (id, direction, source_entity, target_entity, target_id,
                 project_code, sync_type, action,
                 payload, status, triggered_by, created_at)
            VALUES (?, 'PM_TO_SALE', 'WorkflowTask', 'sale_tasks', ?,
                    ?, 'OVERDUE_DETECTION', 'CREATE',
                    ?, 'SYNCED', 'SYSTEM', ?)
        """, [
            str(uuid.uuid4()), task_id,
            opportunity.get("project_code"),
            json.dumps({"overdue_count": overdue_count}),
            now,
        ])

        logger.info("pm_overdue_task_created",
                      task_id=task_id,
                      project=opportunity.get("project_code"),
                      overdue_count=overdue_count)

    except Exception as e:
        logger.error("pm_overdue_handler_error",
                      opp_id=opportunity.get("id"), error=str(e))


async def get_sync_log(
    opportunity_id: Optional[str] = None,
    direction: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Get PM sync log entries.

    Args:
        opportunity_id: Filter by opportunity ID.
        direction: Filter by direction (PM_TO_SALE or SALE_TO_PM).
        limit: Max results (default 100, max 200).

    Returns:
        List of sync log records.
    """
    try:
        limit = min(limit, 200)
        sql = "SELECT * FROM sale_pm_sync_log WHERE 1=1"
        params: list = []

        if opportunity_id:
            sql += " AND project_code IN (SELECT project_code FROM sale_opportunities WHERE id = ?)"
            params.append(opportunity_id)

        if direction:
            sql += " AND direction = ?"
            params.append(direction)

        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        return query(sql, params)
    except Exception:
        return []
