"""PM Bridge service for Sale ↔ ibshi1 (L1) platform integration.

Syncs project updates from PM to Sale (milestone completions, overdue tasks)
and sales context to PM (customer communications, change requests).

Two-way sync via HTTP REST API to ibshi1 running on :3000.
All syncs logged to sale_pm_sync_log for audit trail.

HARD RULE: draft_reply_email() creates DRAFT only — never auto-sends.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Optional, Any

import httpx
import structlog

logger = structlog.get_logger(__name__)

# Support both module and direct execution
try:
    from . import config
except ImportError:
    import config


class PMBridge:
    """Bridge between Sale Platform and ibshi1 PM system."""

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_token: Optional[str] = None,
    ):
        """Initialize PM Bridge with ibshi1 connection details.

        Args:
            api_url: ibshi1 API base URL. Defaults to config.IBSHI1_URL.
            api_token: Bearer token. Defaults to config.IBSHI1_TOKEN.
        """
        self.api_url = api_url or config.IBSHI1_URL
        self.api_token = api_token or config.IBSHI1_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    async def get_project_status(self, project_code: str) -> Optional[Dict[str, Any]]:
        """Get consolidated project status from ibshi1.

        Args:
            project_code: Project code to look up (e.g., "V17556").

        Returns:
            Dict with project, milestones, tasks_summary, or None if error.
        """
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{self.api_url}/api/projects?projectCode={project_code}",
                    headers=self.headers,
                )
                if resp.status_code != 200:
                    logger.warning("pm_project_not_found",
                                    project_code=project_code,
                                    status=resp.status_code)
                    return None

                project = resp.json()

                # Get milestones
                ms_resp = await client.get(
                    f"{self.api_url}/api/milestones?projectId={project['id']}",
                    headers=self.headers,
                )
                milestones = ms_resp.json() if ms_resp.status_code == 200 else []

                # Get tasks
                t_resp = await client.get(
                    f"{self.api_url}/api/tasks?projectId={project['id']}",
                    headers=self.headers,
                )
                tasks = t_resp.json() if t_resp.status_code == 200 else []

                return {
                    "project": project,
                    "milestones": milestones,
                    "tasks_summary": {
                        "total": len(tasks),
                        "overdue": len([t for t in tasks if t.get("urgency") == "overdue"]),
                        "completed": len([t for t in tasks if t.get("status") == "COMPLETED"]),
                    },
                    "summary": (
                        f"{project.get('projectName')} - {len(milestones)} milestones, "
                        f"{len([m for m in milestones if m.get('status') == 'COMPLETED'])} completed"
                    ),
                }

        except (httpx.TimeoutException, httpx.ConnectError) as e:
            logger.error("pm_connection_failed",
                          url=self.api_url, error=str(e))
            return None
        except Exception as e:
            logger.error("pm_status_error",
                          project_code=project_code, error=str(e))
            return None

    async def create_pm_task(
        self,
        opportunity_id: str,
        task_type: str,
        title: str,
        description: str,
        assigned_role: str,
    ) -> Optional[Dict[str, Any]]:
        """Create task in ibshi1 from Sale context.

        Args:
            opportunity_id: Sale opportunity ID.
            task_type: Type of task.
            title: Task title.
            description: Task description.
            assigned_role: Role to assign in PM.

        Returns:
            Created task object from ibshi1, or None if error.
        """
        try:
            from .database import query, execute

            opp = query(
                "SELECT * FROM sale_opportunities WHERE id = ?",
                [opportunity_id], one=True
            )

            if not opp or not opp.get("project_code"):
                logger.warning("pm_no_project_link",
                                opp_id=opportunity_id)
                return None

            async with httpx.AsyncClient(timeout=10) as client:
                proj_resp = await client.get(
                    f"{self.api_url}/api/projects?projectCode={opp['project_code']}",
                    headers=self.headers,
                )
                if proj_resp.status_code != 200:
                    return None

                project = proj_resp.json()

                task_resp = await client.post(
                    f"{self.api_url}/api/tasks",
                    headers=self.headers,
                    json={
                        "projectId": project["id"],
                        "stepCode": f"SALE_{task_type}",
                        "stepName": title,
                        "description": description,
                        "assignedRole": assigned_role,
                        "priority": "HIGH",
                        "source": "SALE_PLATFORM",
                    },
                )

                if task_resp.status_code not in (200, 201):
                    logger.warning("pm_task_create_failed",
                                    status=task_resp.status_code)
                    return None

                pm_task = task_resp.json()

                # Log sync
                execute("""
                    INSERT INTO sale_pm_sync_log
                        (id, direction, source_entity, source_id,
                         target_entity, target_id,
                         project_code, sync_type, action,
                         payload, status, triggered_by, created_at)
                    VALUES (?, 'SALE_TO_PM', 'sale_opportunities', ?,
                            'WorkflowTask', ?, ?, ?, 'CREATE', ?, 'SYNCED', 'API', ?)
                """, [
                    str(uuid.uuid4()), opportunity_id,
                    pm_task.get("id"), opp["project_code"],
                    task_type,
                    json.dumps({"title": title, "assigned_role": assigned_role}),
                    datetime.utcnow().isoformat(),
                ])

                logger.info("pm_task_created",
                             pm_task_id=pm_task.get("id"),
                             project=opp["project_code"])
                return pm_task

        except Exception as e:
            logger.error("pm_task_error",
                          opp_id=opportunity_id, error=str(e))
            return None

    async def draft_reply_email(
        self,
        opportunity_id: str,
        context: str,
        template_type: str,
    ) -> Optional[Dict[str, Any]]:
        """Draft email reply based on PM project data.

        CRITICAL: Status=DRAFT, requires_review=True. NEVER auto-send.

        Args:
            opportunity_id: Sale opportunity ID.
            context: Email context (e.g., 'Milestone Update').
            template_type: Email template type.

        Returns:
            Draft email dict with status='DRAFT', or None if error.
        """
        try:
            from .database import query, execute

            opp = query(
                "SELECT * FROM sale_opportunities WHERE id = ?",
                [opportunity_id], one=True
            )
            if not opp:
                return None

            # Get project status from PM
            project_status = await self.get_project_status(
                opp.get("project_code", "")
            )

            # Get email template
            template = query(
                "SELECT * FROM sale_email_templates WHERE template_type = ?",
                [template_type], one=True
            ) or {"body": ""}

            # Build draft with PM data
            body = self._fill_template(template, opp, project_status)
            draft = {
                "to": opp.get("customer_email"),
                "subject": f"Re: {opp.get('project_name')} - {context}",
                "body": body,
                "status": "DRAFT",
                "requires_review": True,
                "reviewer_note": (
                    f"Draft based on PM status: "
                    f"{project_status.get('summary', 'N/A') if project_status else 'N/A'}"
                ),
            }

            # Log as DRAFT
            execute("""
                INSERT INTO sale_pm_sync_log
                    (id, direction, source_entity, source_id,
                     target_entity, project_code,
                     sync_type, action, payload, status,
                     triggered_by, created_at)
                VALUES (?, 'PM_TO_SALE', 'Project', ?,
                        'sale_emails', ?,
                        'DRAFT_REPLY_CREATED', 'DRAFT', ?, 'DRAFT',
                        'SYSTEM', ?)
            """, [
                str(uuid.uuid4()),
                opp.get("project_code"),
                opp.get("project_code"),
                json.dumps(draft),
                datetime.utcnow().isoformat(),
            ])

            logger.info("pm_draft_created",
                         opp_id=opportunity_id,
                         template=template_type)
            return draft

        except Exception as e:
            logger.error("pm_draft_error",
                          opp_id=opportunity_id, error=str(e))
            return None

    async def get_project_timeline(
        self, project_code: str
    ) -> Optional[Dict[str, Any]]:
        """Get project timeline with milestones and tasks.

        Args:
            project_code: Project code to look up.

        Returns:
            Timeline dict with milestones and grouped tasks, or None.
        """
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                proj_resp = await client.get(
                    f"{self.api_url}/api/projects?projectCode={project_code}",
                    headers=self.headers,
                )
                if proj_resp.status_code != 200:
                    return None

                project = proj_resp.json()

                ms_resp = await client.get(
                    f"{self.api_url}/api/milestones?projectId={project['id']}",
                    headers=self.headers,
                )
                milestones = ms_resp.json() if ms_resp.status_code == 200 else []

                t_resp = await client.get(
                    f"{self.api_url}/api/tasks?projectId={project['id']}",
                    headers=self.headers,
                )
                tasks = t_resp.json() if t_resp.status_code == 200 else []

                return {
                    "project": project,
                    "milestones": [
                        {
                            "id": m.get("id"),
                            "name": m.get("name"),
                            "status": m.get("status"),
                            "plannedDate": m.get("plannedDate"),
                            "actualDate": m.get("actualDate"),
                            "tasks": [
                                t for t in tasks
                                if t.get("milestoneId") == m.get("id")
                            ],
                        }
                        for m in milestones
                    ],
                }

        except Exception as e:
            logger.error("pm_timeline_error",
                          project_code=project_code, error=str(e))
            return None

    def _fill_template(
        self,
        template: Dict[str, Any],
        opportunity: Dict[str, Any],
        project_status: Optional[Dict[str, Any]],
    ) -> str:
        """Fill email template with opportunity and project data."""
        body = template.get("body", "") or template.get("body_template", "")

        variables = {
            "customer_name": opportunity.get("customer_name", ""),
            "project_name": opportunity.get("project_name", ""),
            "project_code": opportunity.get("project_code", ""),
            "sales_person": opportunity.get("assigned_to", ""),
            "project_status": (
                project_status.get("summary", "")
                if project_status else "N/A"
            ),
        }

        for key, value in variables.items():
            body = body.replace(f"{{{{{key}}}}}", str(value))

        return body
