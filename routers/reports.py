"""Reports Router — sale_report_configs (CRUD) + sale_audit_log (read).

Three surfaces in one file:
- /reports/configs — manage scheduled / on-demand report definitions
- /reports/configs/{id}/run — generate a report (Phase 2 step 12)
- /reports/audit-log — surface the audit trail with filters
"""

import json
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel

import structlog

try:
    from ..database import query, execute
    from ..auth import (
        UserContext, require_write, get_current_writer, get_current_admin,
    )
    from ..errors import EntityNotFoundError
    from ..services import report_engine
except ImportError:
    from database import query, execute
    from auth import (
        UserContext, require_write, get_current_writer, get_current_admin,
    )
    from errors import EntityNotFoundError
    from services import report_engine

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/reports", tags=["Reports"])


# ═══════════════════════════════════════════════════════════════
# Report configs
# ═══════════════════════════════════════════════════════════════

class ReportConfigCreate(BaseModel):
    """Required: report_name, report_type. Everything else optional."""
    report_name: str
    report_type: str             # PIPELINE | SLA | KHKD | COMMISSION | CUSTOM
    description: Optional[str] = None
    schedule_cron: Optional[str] = None
    schedule_type: Optional[str] = "MANUAL"   # MANUAL | DAILY | WEEKLY | MONTHLY | CRON
    template_format: Optional[str] = "XLSX"   # XLSX | PDF | CSV | HTML
    template_config: Optional[str] = None     # JSON
    filters_json: Optional[str] = None        # JSON
    recipients: Optional[str] = None          # comma-separated emails
    cc_recipients: Optional[str] = None
    delivery_method: Optional[str] = "EMAIL"  # EMAIL | NAS | API_DOWNLOAD
    nas_output_path: Optional[str] = None
    is_active: Optional[bool] = True


class ReportConfigUpdate(BaseModel):
    report_name: Optional[str] = None
    report_type: Optional[str] = None
    description: Optional[str] = None
    schedule_cron: Optional[str] = None
    schedule_type: Optional[str] = None
    template_format: Optional[str] = None
    template_config: Optional[str] = None
    filters_json: Optional[str] = None
    recipients: Optional[str] = None
    cc_recipients: Optional[str] = None
    delivery_method: Optional[str] = None
    nas_output_path: Optional[str] = None
    is_active: Optional[bool] = None


@router.get("/configs")
async def list_report_configs(
    report_type: Optional[str] = Query(None),
    schedule_type: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List report configurations."""
    where = []
    params: list = []
    if report_type:
        where.append("report_type = ?")
        params.append(report_type)
    if schedule_type:
        where.append("schedule_type = ?")
        params.append(schedule_type)
    if is_active is not None:
        where.append("is_active = ?")
        params.append(1 if is_active else 0)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_report_configs WHERE {where_sql}",
        params,
    )[0]["cnt"]
    items = query(
        f"""
        SELECT * FROM sale_report_configs WHERE {where_sql}
        ORDER BY is_active DESC, last_run_at DESC, created_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/configs/{config_id}")
async def get_report_config(config_id: str):
    item = query(
        "SELECT * FROM sale_report_configs WHERE id = ?",
        [config_id], one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Report config not found")
    return {"config": dict(item)}


@router.post("/configs", dependencies=[Depends(require_write)])
async def create_report_config(payload: ReportConfigCreate):
    config_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute(
        """
        INSERT INTO sale_report_configs
            (id, report_name, report_type, description,
             schedule_cron, schedule_type, template_format, template_config,
             filters_json, recipients, cc_recipients, delivery_method,
             nas_output_path, run_count, is_active,
             created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
        """,
        [
            config_id, payload.report_name, payload.report_type,
            payload.description, payload.schedule_cron,
            payload.schedule_type or "MANUAL",
            payload.template_format or "XLSX", payload.template_config,
            payload.filters_json, payload.recipients, payload.cc_recipients,
            payload.delivery_method or "EMAIL", payload.nas_output_path,
            1 if payload.is_active else 0, now, now,
        ],
    )
    return {"id": config_id, "status": "ok"}


@router.patch("/configs/{config_id}", dependencies=[Depends(require_write)])
async def update_report_config(config_id: str, payload: ReportConfigUpdate):
    existing = query(
        "SELECT id FROM sale_report_configs WHERE id = ?",
        [config_id], one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Report config not found")

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    if "is_active" in data and isinstance(data["is_active"], bool):
        data["is_active"] = 1 if data["is_active"] else 0

    sets = [f"{k} = ?" for k in data.keys()]
    sets.append("updated_at = ?")
    params = list(data.values()) + [datetime.now().isoformat(), config_id]
    execute(
        f"UPDATE sale_report_configs SET {', '.join(sets)} WHERE id = ?",
        params,
    )
    return {"id": config_id, "status": "ok"}


@router.delete("/configs/{config_id}")
async def delete_report_config(
    config_id: str,
    user: UserContext = Depends(get_current_admin),
):
    """Hard-delete a report config. Admin only.

    Report configs have no audit-log dependencies, so we drop the row
    rather than soft-deleting.
    """
    existing = query(
        "SELECT id FROM sale_report_configs WHERE id = ?",
        [config_id], one=True,
    )
    if not existing:
        raise EntityNotFoundError("ReportConfig", config_id)
    execute("DELETE FROM sale_report_configs WHERE id = ?", [config_id])
    return {"id": config_id, "status": "deleted"}


@router.post("/configs/{config_id}/run")
async def run_report(
    config_id: str,
    fmt: str = Query("json", description="json | csv | xlsx"),
    user: UserContext = Depends(get_current_writer),
):
    """Generate a report from a config (Phase 2 step 12).

    JSON returns the rows inline. CSV / XLSX return file responses
    with a Content-Disposition header so the browser triggers a
    download.

    Filters can be defined in ``sale_report_configs.filters_json``;
    ad-hoc overrides are not yet exposed here — that's a Phase 3
    polish (POST body filters).
    """
    existing = query(
        "SELECT * FROM sale_report_configs WHERE id = ?",
        [config_id], one=True,
    )
    if not existing:
        raise EntityNotFoundError("ReportConfig", config_id)

    now = datetime.now().isoformat()
    try:
        metadata, payload = report_engine.generate(dict(existing), fmt=fmt)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        # Record the failure on the config so the UI shows it.
        execute(
            """
            UPDATE sale_report_configs
            SET last_run_at = ?, last_run_status = 'ERROR',
                last_run_error = ?, run_count = COALESCE(run_count, 0) + 1,
                updated_at = ?
            WHERE id = ?
            """,
            [now, str(exc)[:500], now, config_id],
        )
        logger.exception("report_generation_failed", config_id=config_id)
        raise HTTPException(status_code=500, detail=str(exc))

    new_count = (existing.get("run_count") or 0) + 1
    execute(
        """
        UPDATE sale_report_configs
        SET last_run_at = ?, last_run_status = 'OK',
            last_run_error = NULL, run_count = ?, updated_at = ?
        WHERE id = ?
        """,
        [now, new_count, now, config_id],
    )

    if metadata.get("format") == "json":
        return metadata

    # CSV / XLSX: return file response.
    actual_fmt = metadata.get("format")
    media = (
        "text/csv" if actual_fmt == "csv"
        else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    fname = (
        f"{(existing.get('report_name') or 'report').replace(' ', '_')}"
        f"_{now[:10]}.{actual_fmt}"
    )
    return Response(
        content=payload,
        media_type=media,
        headers={
            "Content-Disposition": f'attachment; filename="{fname}"',
            "X-Report-Type": metadata.get("report_type") or "",
            "X-Report-Row-Count": str(metadata.get("row_count") or 0),
        },
    )


@router.post("/configs/seed-defaults")
async def seed_default_report_configs(
    user: UserContext = Depends(get_current_writer),
):
    """Seed the 5 standard report configs (Phase 2 step 12).

    Skips configs that already exist — idempotent.
    """
    inserted = []
    skipped = []
    now = datetime.now().isoformat()

    for cfg in report_engine.default_configs():
        existing = query(
            "SELECT id FROM sale_report_configs WHERE report_name = ?",
            [cfg["name"]], one=True,
        )
        if existing:
            skipped.append(cfg["name"])
            continue

        config_id = str(uuid.uuid4())
        execute(
            """
            INSERT INTO sale_report_configs
                (id, report_name, report_type, description,
                 schedule_cron, schedule_type, template_format,
                 filters_json, is_active, created_by,
                 created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'MANUAL', 'XLSX', ?, 1, ?, ?, ?)
            """,
            [
                config_id, cfg["name"], cfg["report_type"], cfg["description"],
                cfg.get("schedule_cron"),
                json.dumps(cfg.get("filters") or {}),
                user.actor, now, now,
            ],
        )
        inserted.append({
            "id": config_id,
            "report_name": cfg["name"],
            "report_type": cfg["report_type"],
        })

    return {
        "inserted": inserted,
        "skipped": skipped,
        "summary": f"{len(inserted)} created, {len(skipped)} already existed",
    }


# ═══════════════════════════════════════════════════════════════
# Audit log read surface
# ═══════════════════════════════════════════════════════════════

@router.get("/audit-log")
async def list_audit_log(
    entity_type: Optional[str] = Query(None, description="opportunity | task | customer | quotation | etc."),
    entity_id: Optional[str] = Query(None),
    action: Optional[str] = Query(None, description="STATUS_CHANGE | UPDATE | CREATE | DELETE"),
    field_name: Optional[str] = Query(None),
    changed_by: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Paginated read of sale_audit_log with filters."""
    where = []
    params: list = []
    for col, val in [
        ("entity_type", entity_type), ("entity_id", entity_id),
        ("action", action), ("field_name", field_name),
        ("changed_by", changed_by),
    ]:
        if val is not None:
            where.append(f"{col} = ?")
            params.append(val)
    if date_from:
        where.append("created_at >= ?"); params.append(date_from)
    if date_to:
        where.append("created_at <= ?"); params.append(date_to)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_audit_log WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT * FROM sale_audit_log WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/audit-log/{entity_type}/{entity_id}")
async def entity_audit_history(entity_type: str, entity_id: str):
    """Full audit history for a single entity (most useful for /entity-detail UI)."""
    items = query(
        """
        SELECT * FROM sale_audit_log
        WHERE entity_type = ? AND entity_id = ?
        ORDER BY created_at DESC
        """,
        [entity_type, entity_id],
    )
    return {
        "entity_type": entity_type,
        "entity_id": entity_id,
        "items": items,
        "count": len(items),
    }


@router.get("/audit-log/summary")
async def audit_log_summary(
    days: int = Query(7, ge=1, le=365, description="Window — last N days"),
):
    """Counts grouped by entity_type + action over the last N days."""
    rows = query(
        f"""
        SELECT entity_type, action, COUNT(*) AS count
        FROM sale_audit_log
        WHERE created_at >= datetime('now', '-{int(days)} days')
        GROUP BY entity_type, action
        ORDER BY count DESC
        """
    )
    return {"window_days": days, "rows": rows, "count": len(rows)}
