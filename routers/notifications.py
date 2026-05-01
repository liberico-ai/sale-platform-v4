"""Notifications Router — sale_notifications.

Notifications are written by background workers (sla_worker, stale_worker,
followup_worker) and read by the frontend. This router is read-only for
list/count and write for mark-as-read.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Header, Query

import structlog

try:
    from ..database import query, execute
    from ..auth import require_write
    from .. import config
except ImportError:
    from database import query, execute
    from auth import require_write
    import config

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def _resolve_current_user_id(x_api_key: Optional[str], explicit: Optional[str]) -> Optional[str]:
    """Pick the user_id filter for notification queries.

    Priority: explicit ?user_id query param > sale_user_roles row matching
    the API key's tier. Falls back to None (broadcast notifications only).
    """
    if explicit:
        return explicit
    if not x_api_key:
        return None
    tier = config.API_KEYS.get(x_api_key)
    if not tier:
        return None
    role_filter = "ADMIN" if tier == "ADMIN" else (
        "MANAGER" if tier == "MANAGER" else "MEMBER"
    )
    profile = query(
        "SELECT email FROM sale_user_roles "
        "WHERE role = ? AND is_active = 1 "
        "ORDER BY joined_at ASC LIMIT 1",
        [role_filter],
        one=True,
    )
    return profile.get("email") if profile else None


@router.get("")
async def list_notifications(
    is_read: Optional[bool] = Query(None),
    type: Optional[str] = Query(None, description="SLA_OVERDUE, STALE_DEAL, FOLLOWUP_DUE, QUOTATION_EXPIRING"),
    severity: Optional[str] = Query(None, description="INFO, WARN, CRIT"),
    user_id: Optional[str] = Query(None, description="Override; defaults to caller's user"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    x_api_key: Optional[str] = Header(None),
):
    """List notifications for the caller (or for ?user_id when supplied).

    Includes broadcast rows (user_id IS NULL) for everyone.
    """
    target = _resolve_current_user_id(x_api_key, user_id)

    where = []
    params: list = []
    if target:
        where.append("(user_id = ? OR user_id IS NULL)")
        params.append(target)
    else:
        where.append("user_id IS NULL")

    if is_read is not None:
        where.append("is_read = ?")
        params.append(1 if is_read else 0)
    if type:
        where.append("type = ?")
        params.append(type)
    if severity:
        where.append("severity = ?")
        params.append(severity)

    where_sql = " AND ".join(where)

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_notifications WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT * FROM sale_notifications
        WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {
        "total": total,
        "items": items,
        "user_id": target,
        "limit": limit,
        "offset": offset,
    }


@router.get("/count")
async def unread_count(
    user_id: Optional[str] = Query(None),
    x_api_key: Optional[str] = Header(None),
):
    """Unread notification count for the caller (or ?user_id)."""
    target = _resolve_current_user_id(x_api_key, user_id)

    where = ["is_read = 0"]
    params: list = []
    if target:
        where.append("(user_id = ? OR user_id IS NULL)")
        params.append(target)
    else:
        where.append("user_id IS NULL")

    row = query(
        f"SELECT COUNT(*) as cnt FROM sale_notifications WHERE {' AND '.join(where)}",
        params,
    )[0]
    return {"user_id": target, "unread": row["cnt"]}


@router.patch("/{notification_id}/read", dependencies=[Depends(require_write)])
async def mark_as_read(notification_id: str):
    """Mark a single notification as read."""
    existing = query(
        "SELECT id, is_read FROM sale_notifications WHERE id = ?",
        [notification_id],
        one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Notification not found")
    if existing.get("is_read") == 1:
        return {"id": notification_id, "status": "already_read"}

    execute(
        "UPDATE sale_notifications SET is_read = 1, read_at = ? WHERE id = ?",
        [datetime.now().isoformat(), notification_id],
    )
    return {"id": notification_id, "status": "read"}


@router.patch("/read-all", dependencies=[Depends(require_write)])
async def mark_all_as_read(
    user_id: Optional[str] = Query(None),
    x_api_key: Optional[str] = Header(None),
):
    """Mark every unread notification for the caller as read."""
    target = _resolve_current_user_id(x_api_key, user_id)

    now = datetime.now().isoformat()
    if target:
        affected = execute(
            "UPDATE sale_notifications SET is_read = 1, read_at = ? "
            "WHERE is_read = 0 AND (user_id = ? OR user_id IS NULL)",
            [now, target],
        )
    else:
        affected = execute(
            "UPDATE sale_notifications SET is_read = 1, read_at = ? "
            "WHERE is_read = 0 AND user_id IS NULL",
            [now],
        )

    return {"user_id": target, "affected": affected}
