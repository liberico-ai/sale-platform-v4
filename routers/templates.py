"""Templates Router — sale_quote_templates + sale_email_templates.

Quote templates feed the auto-quote engine (Sprint 2 Phase 2).
Email templates feed the DRAFT-email engine (sale → review → send).
"""

import json
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

import structlog

try:
    from ..database import query, execute
    from ..auth import require_write, get_current_admin, UserContext
    from ..errors import EntityNotFoundError
except ImportError:
    from database import query, execute
    from auth import require_write, get_current_admin, UserContext
    from errors import EntityNotFoundError

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/templates", tags=["Templates"])


# ═══════════════════════════════════════════════════════════════
# Quote templates — sale_quote_templates
# ═══════════════════════════════════════════════════════════════

class QuoteTemplateCreate(BaseModel):
    template_name: str
    product_category_id: Optional[str] = None
    product_type: Optional[str] = None
    weight_range_min: Optional[float] = None
    weight_range_max: Optional[float] = None
    base_unit_price: Optional[float] = None
    material_pct: Optional[float] = None
    labor_pct: Optional[float] = None
    overhead_pct: Optional[float] = None
    subcontract_pct: Optional[float] = None
    target_gm_pct: Optional[float] = None
    complexity_factor: Optional[float] = 1.0
    lead_time_weeks: Optional[int] = None
    cost_breakdown_json: Optional[str] = None
    assumptions: Optional[str] = None
    currency: Optional[str] = "USD"
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None


class QuoteTemplateUpdate(BaseModel):
    template_name: Optional[str] = None
    product_category_id: Optional[str] = None
    product_type: Optional[str] = None
    weight_range_min: Optional[float] = None
    weight_range_max: Optional[float] = None
    base_unit_price: Optional[float] = None
    material_pct: Optional[float] = None
    labor_pct: Optional[float] = None
    overhead_pct: Optional[float] = None
    subcontract_pct: Optional[float] = None
    target_gm_pct: Optional[float] = None
    complexity_factor: Optional[float] = None
    lead_time_weeks: Optional[int] = None
    cost_breakdown_json: Optional[str] = None
    assumptions: Optional[str] = None
    currency: Optional[str] = None
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    is_active: Optional[bool] = None


@router.get("/quote")
async def list_quote_templates(
    product_type: Optional[str] = Query(None),
    product_category_id: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List quote templates."""
    where = []
    params: list = []
    if product_type:
        where.append("product_type = ?"); params.append(product_type)
    if product_category_id:
        where.append("product_category_id = ?"); params.append(product_category_id)
    if is_active is not None:
        where.append("is_active = ?"); params.append(1 if is_active else 0)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_quote_templates WHERE {where_sql}",
        params,
    )[0]["cnt"]
    items = query(
        f"""
        SELECT qt.*, pc.code AS product_code, pc.name_en AS product_name
        FROM sale_quote_templates qt
        LEFT JOIN sale_product_categories pc ON pc.id = qt.product_category_id
        WHERE {where_sql}
        ORDER BY qt.is_active DESC, qt.template_name ASC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/quote/{template_id}")
async def get_quote_template(template_id: str):
    item = query(
        """
        SELECT qt.*, pc.code AS product_code, pc.name_en AS product_name
        FROM sale_quote_templates qt
        LEFT JOIN sale_product_categories pc ON pc.id = qt.product_category_id
        WHERE qt.id = ?
        """,
        [template_id], one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Quote template not found")
    return {"template": dict(item)}


@router.post("/quote", dependencies=[Depends(require_write)])
async def create_quote_template(payload: QuoteTemplateCreate):
    template_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    cols = list(data.keys()) + [
        "id", "is_active", "version", "created_at", "updated_at",
    ]
    values = list(data.values()) + [template_id, 1, 1, now, now]
    placeholders = ",".join("?" * len(cols))
    execute(
        f"INSERT INTO sale_quote_templates ({','.join(cols)}) "
        f"VALUES ({placeholders})",
        values,
    )
    return {"id": template_id, "status": "ok"}


@router.patch("/quote/{template_id}", dependencies=[Depends(require_write)])
async def update_quote_template(template_id: str, payload: QuoteTemplateUpdate):
    existing = query(
        "SELECT version FROM sale_quote_templates WHERE id = ?",
        [template_id], one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Quote template not found")

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    if "is_active" in data and isinstance(data["is_active"], bool):
        data["is_active"] = 1 if data["is_active"] else 0

    new_version = (existing.get("version") or 1) + 1
    sets = [f"{k} = ?" for k in data.keys()]
    sets.extend(["version = ?", "updated_at = ?"])
    params = list(data.values()) + [
        new_version, datetime.now().isoformat(), template_id,
    ]
    execute(
        f"UPDATE sale_quote_templates SET {', '.join(sets)} WHERE id = ?",
        params,
    )
    return {"id": template_id, "status": "ok", "version": new_version}


# ═══════════════════════════════════════════════════════════════
# Email templates — sale_email_templates
# ═══════════════════════════════════════════════════════════════

class EmailTemplateCreate(BaseModel):
    """sale_email_templates.template_type is UNIQUE."""
    template_type: str       # RFQ_REPLY | FOLLOWUP | THANK_YOU | QUOTE_SENT | etc.
    subject: Optional[str] = None
    body: Optional[str] = None
    language: Optional[str] = "en"
    variables: Optional[list[str]] = None


class EmailTemplateUpdate(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    language: Optional[str] = None
    variables: Optional[list[str]] = None
    is_active: Optional[bool] = None


@router.get("/email")
async def list_email_templates(
    language: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    where = []
    params: list = []
    if language:
        where.append("language = ?"); params.append(language)
    if is_active is not None:
        where.append("is_active = ?"); params.append(1 if is_active else 0)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) AS cnt FROM sale_email_templates WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"SELECT * FROM sale_email_templates WHERE {where_sql} "
        f"ORDER BY template_type ASC LIMIT ? OFFSET ?",
        params + [limit, offset],
    )
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/email/{template_type}")
async def get_email_template(template_type: str):
    item = query(
        "SELECT * FROM sale_email_templates WHERE template_type = ?",
        [template_type], one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Email template not found")
    return {"template": dict(item)}


@router.post("/email", dependencies=[Depends(require_write)])
async def create_email_template(payload: EmailTemplateCreate):
    """Insert (or 409) a new email template. template_type is UNIQUE."""
    existing = query(
        "SELECT id FROM sale_email_templates WHERE template_type = ?",
        [payload.template_type], one=True,
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Template type already exists: {payload.template_type}",
        )

    template_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    variables_json = (
        json.dumps(payload.variables) if payload.variables else None
    )
    execute(
        """
        INSERT INTO sale_email_templates
            (id, template_type, subject, body, language, variables, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 1, ?)
        """,
        [
            template_id, payload.template_type, payload.subject, payload.body,
            payload.language or "en", variables_json, now,
        ],
    )
    return {"id": template_id, "template_type": payload.template_type, "status": "ok"}


@router.patch("/email/{template_type}", dependencies=[Depends(require_write)])
async def update_email_template(template_type: str, payload: EmailTemplateUpdate):
    existing = query(
        "SELECT id FROM sale_email_templates WHERE template_type = ?",
        [template_type], one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Email template not found")

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    if "variables" in data and isinstance(data["variables"], list):
        data["variables"] = json.dumps(data["variables"])
    if "is_active" in data and isinstance(data["is_active"], bool):
        data["is_active"] = 1 if data["is_active"] else 0

    sets = [f"{k} = ?" for k in data.keys()]
    params = list(data.values()) + [template_type]
    execute(
        f"UPDATE sale_email_templates SET {', '.join(sets)} WHERE template_type = ?",
        params,
    )
    return {"template_type": template_type, "status": "ok"}


@router.post("/email/seed-defaults", dependencies=[Depends(require_write)])
async def seed_email_templates():
    """Idempotently seed canonical email templates for the Sale workflow."""
    defaults = [
        {
            "template_type": "RFQ_ACK",
            "subject": "RFQ received — {{project_name}}",
            "body": (
                "Dear {{contact_name}},\n\n"
                "Thank you for your RFQ on {{project_name}}. We have received "
                "your request and will respond with a quotation within "
                "{{response_days}} business days.\n\n"
                "Best regards,\n{{sender_name}}\nIBS Heat Industry"
            ),
            "variables": ["project_name", "contact_name", "response_days", "sender_name"],
        },
        {
            "template_type": "QUOTE_SENT",
            "subject": "Quotation #{{quotation_no}} — {{project_name}}",
            "body": (
                "Dear {{contact_name}},\n\n"
                "Please find attached our quotation #{{quotation_no}} for "
                "{{project_name}} (USD {{value_usd}}). Validity: {{valid_until}}.\n\n"
                "Happy to discuss any clarification needed.\n\n"
                "Best regards,\n{{sender_name}}"
            ),
            "variables": ["quotation_no", "project_name", "contact_name",
                          "value_usd", "valid_until", "sender_name"],
        },
        {
            "template_type": "FOLLOWUP",
            "subject": "Following up — {{project_name}}",
            "body": (
                "Dear {{contact_name}},\n\n"
                "I'm following up on our quotation for {{project_name}} sent on "
                "{{sent_date}}. Could you share an update on your evaluation "
                "timeline?\n\nBest regards,\n{{sender_name}}"
            ),
            "variables": ["project_name", "contact_name", "sent_date", "sender_name"],
        },
        {
            "template_type": "WON_THANK_YOU",
            "subject": "Thank you — {{project_name}}",
            "body": (
                "Dear {{contact_name}},\n\n"
                "Thank you for awarding the {{project_name}} contract to IBS. "
                "Our project manager {{pm_name}} will be your primary contact "
                "from here.\n\nBest regards,\n{{sender_name}}"
            ),
            "variables": ["project_name", "contact_name", "pm_name", "sender_name"],
        },
        {
            "template_type": "PAYMENT_REMINDER",
            "subject": "Payment reminder — Invoice {{invoice_number}}",
            "body": (
                "Dear {{contact_name}},\n\n"
                "This is a friendly reminder that invoice {{invoice_number}} "
                "for {{project_name}} (USD {{amount}}) was due on {{due_date}}.\n\n"
                "Please confirm payment status at your earliest convenience.\n\n"
                "Best regards,\n{{sender_name}}"
            ),
            "variables": ["invoice_number", "project_name", "contact_name",
                          "amount", "due_date", "sender_name"],
        },
    ]

    inserted = []
    skipped = []
    now = datetime.now().isoformat()
    for tpl in defaults:
        existing = query(
            "SELECT id FROM sale_email_templates WHERE template_type = ?",
            [tpl["template_type"]], one=True,
        )
        if existing:
            skipped.append(tpl["template_type"])
            continue

        template_id = str(uuid.uuid4())
        execute(
            """
            INSERT INTO sale_email_templates
                (id, template_type, subject, body, language, variables,
                 is_active, created_at)
            VALUES (?, ?, ?, ?, 'en', ?, 1, ?)
            """,
            [
                template_id, tpl["template_type"], tpl["subject"], tpl["body"],
                json.dumps(tpl["variables"]), now,
            ],
        )
        inserted.append({"id": template_id, "template_type": tpl["template_type"]})

    return {
        "inserted": inserted,
        "skipped": skipped,
        "summary": f"{len(inserted)} created, {len(skipped)} already existed",
    }


# ═══════════════════════════════════════════════════════════════
# Hard DELETE — templates have no audit trail dependency, so we can
# remove them outright. Admin-only because deleted templates affect
# every future quotation cover that referenced them.
# ═══════════════════════════════════════════════════════════════

@router.delete("/quote/{template_id}")
async def delete_quote_template(
    template_id: str,
    user: UserContext = Depends(get_current_admin),
):
    existing = query(
        "SELECT id FROM sale_quote_templates WHERE id = ?",
        [template_id], one=True,
    )
    if not existing:
        raise EntityNotFoundError("QuoteTemplate", template_id)
    execute("DELETE FROM sale_quote_templates WHERE id = ?", [template_id])
    return {"id": template_id, "status": "deleted"}


@router.delete("/email/{template_type}")
async def delete_email_template(
    template_type: str,
    user: UserContext = Depends(get_current_admin),
):
    existing = query(
        "SELECT id FROM sale_email_templates WHERE template_type = ?",
        [template_type], one=True,
    )
    if not existing:
        raise EntityNotFoundError("EmailTemplate", template_type)
    execute(
        "DELETE FROM sale_email_templates WHERE template_type = ?",
        [template_type],
    )
    return {"template_type": template_type, "status": "deleted"}
