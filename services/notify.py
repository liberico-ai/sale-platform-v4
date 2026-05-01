"""Notification helper — append rows to sale_notifications.

Workers call write_notification() when they detect events worth
surfacing in the in-app feed. The router only reads; writes happen
exclusively from this helper.
"""

import uuid
from datetime import datetime
from typing import Optional

import structlog

try:
    from ..database import execute, query
except ImportError:
    from database import execute, query

logger = structlog.get_logger(__name__)


def write_notification(
    notification_type: str,
    title: str,
    message: Optional[str] = None,
    user_id: Optional[str] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    severity: str = "INFO",
    dedupe_window_hours: int = 24,
) -> Optional[str]:
    """Insert a notification.

    Returns the new notification id, or None when a near-identical
    notification already exists in the last `dedupe_window_hours`
    (prevents the SLA worker from spamming the same task every 15 min).

    Dedupe key: (user_id, type, entity_type, entity_id).
    """
    if dedupe_window_hours > 0 and entity_id:
        existing = query(
            f"""
            SELECT id FROM sale_notifications
            WHERE type = ?
              AND COALESCE(entity_type, '') = COALESCE(?, '')
              AND COALESCE(entity_id, '') = COALESCE(?, '')
              AND COALESCE(user_id, '') = COALESCE(?, '')
              AND created_at > datetime('now', '-{int(dedupe_window_hours)} hours')
            LIMIT 1
            """,
            [notification_type, entity_type, entity_id, user_id],
            one=True,
        )
        if existing:
            return None

    notification_id = str(uuid.uuid4())
    execute(
        """
        INSERT INTO sale_notifications
            (id, user_id, type, title, message,
             entity_type, entity_id, is_read, severity, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
        """,
        [
            notification_id, user_id, notification_type, title, message,
            entity_type, entity_id, severity,
            datetime.now().isoformat(),
        ],
    )

    logger.info(
        "notification_written",
        notification_id=notification_id,
        type=notification_type,
        user_id=user_id,
        entity_id=entity_id,
    )
    return notification_id
