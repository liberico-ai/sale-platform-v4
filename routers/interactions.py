"""Interactions Router — sale_customer_interactions (175 records).

Captures meetings, calls, client visits, and emails outside of the
Gmail-synced sale_emails feed.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

import structlog

try:
    from ..database import query, execute
    from ..auth import require_write
except ImportError:
    from database import query, execute
    from auth import require_write

try:
    from ..models.interaction import (
        CustomerInteractionCreate,
        CustomerInteractionUpdate,
    )
except ImportError:
    from models.interaction import (
        CustomerInteractionCreate,
        CustomerInteractionUpdate,
    )

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/interactions", tags=["Interactions"])


@router.get("")
async def list_interactions(
    customer_id: Optional[str] = Query(None),
    type: Optional[str] = Query(None, description="MEETING, CALL, CLIENT_VISIT, EMAIL, etc."),
    outcome: Optional[str] = Query(None),
    opportunity_id: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List customer interactions with optional filters."""
    where = []
    params: list = []
    if customer_id:
        where.append("ci.customer_id = ?")
        params.append(customer_id)
    if type:
        where.append("ci.interaction_type = ?")
        params.append(type)
    if outcome:
        where.append("ci.outcome = ?")
        params.append(outcome)
    if opportunity_id:
        where.append("ci.opportunity_id = ?")
        params.append(opportunity_id)
    if date_from:
        where.append("ci.interaction_date >= ?")
        params.append(date_from)
    if date_to:
        where.append("ci.interaction_date <= ?")
        params.append(date_to)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_customer_interactions ci WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT ci.*, c.name AS customer_name, o.project_name
        FROM sale_customer_interactions ci
        LEFT JOIN sale_customers c ON c.id = ci.customer_id
        LEFT JOIN sale_opportunities o ON o.id = ci.opportunity_id
        WHERE {where_sql}
        ORDER BY ci.interaction_date DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/{interaction_id}")
async def get_interaction(interaction_id: str):
    """Get a single interaction with customer + opportunity context."""
    item = query(
        """
        SELECT ci.*,
               c.name AS customer_name, c.country AS customer_country,
               o.project_name, o.product_group, o.stage AS opp_stage
        FROM sale_customer_interactions ci
        LEFT JOIN sale_customers c ON c.id = ci.customer_id
        LEFT JOIN sale_opportunities o ON o.id = ci.opportunity_id
        WHERE ci.id = ?
        """,
        [interaction_id],
        one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return {"interaction": dict(item)}


@router.post("", dependencies=[Depends(require_write)])
async def create_interaction(interaction: CustomerInteractionCreate):
    """Create a new customer interaction."""
    customer = query(
        "SELECT id FROM sale_customers WHERE id = ?",
        [interaction.customer_id],
        one=True,
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    interaction_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute(
        """
        INSERT INTO sale_customer_interactions
            (id, customer_id, contact_id, opportunity_id, interaction_type,
             interaction_date, duration_minutes, location,
             attendees_ibs, attendees_customer, subject, summary, outcome,
             next_action, next_action_due, sentiment_score,
             nas_file_path, attachments, recorded_by,
             created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            interaction_id, interaction.customer_id, interaction.contact_id,
            interaction.opportunity_id, interaction.interaction_type,
            interaction.interaction_date, interaction.duration_minutes,
            interaction.location, interaction.attendees_ibs,
            interaction.attendees_customer, interaction.subject,
            interaction.summary, interaction.outcome,
            interaction.next_action, interaction.next_action_due,
            interaction.sentiment_score, interaction.nas_file_path,
            interaction.attachments, interaction.recorded_by, now, now,
        ],
    )

    logger.info(
        "interaction_created",
        interaction_id=interaction_id,
        customer_id=interaction.customer_id,
        type=interaction.interaction_type,
    )

    return {"id": interaction_id, "status": "ok",
            "message": f"Interaction created: {interaction.subject}"}


@router.patch("/{interaction_id}", dependencies=[Depends(require_write)])
async def update_interaction(interaction_id: str, update: CustomerInteractionUpdate):
    """Update an existing interaction."""
    existing = query(
        "SELECT id FROM sale_customer_interactions WHERE id = ?",
        [interaction_id],
        one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Interaction not found")

    data = update.model_dump(exclude_unset=True) if hasattr(update, "model_dump") else update.dict(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    sets = [f"{k} = ?" for k in data.keys()]
    params = list(data.values()) + [datetime.now().isoformat(), interaction_id]
    sets.append("updated_at = ?")

    execute(
        f"UPDATE sale_customer_interactions SET {', '.join(sets)} WHERE id = ?",
        params,
    )

    return {"id": interaction_id, "status": "ok"}
