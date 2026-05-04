"""Intelligence Router — Market Signals & Product-Customer Fit Scores.

Read-only access to AI-derived signal *content* (Z4 in the 4-zone data
model). Phase 2 added human-acknowledgement/dismissal/conversion
actions on top — those mutate operational metadata only (status,
acknowledged_at) and never the AI-generated payload itself.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel

import structlog

try:
    from ..database import query, execute
    from ..auth import UserContext, get_current_writer
    from ..errors import EntityNotFoundError
    from ..services.audit import log_status_change
except ImportError:
    from database import query, execute
    from auth import UserContext, get_current_writer
    from errors import EntityNotFoundError
    from services.audit import log_status_change

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/intelligence", tags=["Intelligence"])


# ═══════════════════════════════════════════════════════════════
# sale_market_signals — external signals (12 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/signals")
@router.get("/market-signals")
async def list_market_signals(
    signal_type: Optional[str] = Query(None),
    impact_level: Optional[str] = Query(None, description="HIGH, MEDIUM, LOW"),
    region: Optional[str] = Query(None),
    related_product_group: Optional[str] = Query(None),
    actionable_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List market signals (Z4 read-only — AI-curated)."""
    where = []
    params: list = []
    if signal_type:
        where.append("ms.signal_type = ?")
        params.append(signal_type)
    if impact_level:
        where.append("ms.impact_level = ?")
        params.append(impact_level)
    if region:
        where.append("ms.region = ?")
        params.append(region)
    if related_product_group:
        where.append("ms.related_product_group = ?")
        params.append(related_product_group)
    if actionable_only:
        where.append("ms.is_actionable = 1")
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_market_signals ms WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT ms.*, c.name AS related_customer_name
        FROM sale_market_signals ms
        LEFT JOIN sale_customers c ON c.id = ms.related_customer_id
        WHERE {where_sql}
        ORDER BY
            CASE ms.impact_level WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END,
            ms.relevance_score DESC,
            ms.created_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/market-signals/{signal_id}")
async def get_market_signal(signal_id: str):
    """Get a single market signal."""
    item = query(
        """
        SELECT ms.*, c.name AS related_customer_name
        FROM sale_market_signals ms
        LEFT JOIN sale_customers c ON c.id = ms.related_customer_id
        WHERE ms.id = ?
        """,
        [signal_id],
        one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Market signal not found")
    return {"signal": dict(item)}


# ═══════════════════════════════════════════════════════════════
# sale_product_opportunities — fit-score matrix (51 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/products")
@router.get("/product-opportunities")
async def list_product_opportunities(
    customer_id: Optional[str] = Query(None),
    product_category_id: Optional[str] = Query(None),
    capability_status: Optional[str] = Query(None, description="FULL, PARTIAL, GAP"),
    strategic_only: bool = Query(False),
    min_fit_score: Optional[float] = Query(None, ge=0, le=1),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Cross-sell / upsell fit scores between customers and product categories."""
    where = []
    params: list = []
    if customer_id:
        where.append("po.customer_id = ?")
        params.append(customer_id)
    if product_category_id:
        where.append("po.product_category_id = ?")
        params.append(product_category_id)
    if capability_status:
        where.append("po.capability_status = ?")
        params.append(capability_status)
    if strategic_only:
        where.append("po.is_strategic = 1")
    if min_fit_score is not None:
        where.append("po.fit_score >= ?")
        params.append(min_fit_score)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_product_opportunities po WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT po.*,
               c.name AS customer_name,
               pc.code AS product_code,
               pc.name_en AS product_name_en
        FROM sale_product_opportunities po
        LEFT JOIN sale_customers c ON c.id = po.customer_id
        LEFT JOIN sale_product_categories pc ON pc.id = po.product_category_id
        WHERE {where_sql}
        ORDER BY po.is_strategic DESC, po.fit_score DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


# ═══════════════════════════════════════════════════════════════
# sale_digital_content — collateral / case studies (12 records)
# ═══════════════════════════════════════════════════════════════

@router.get("/digital-content")
async def list_digital_content(
    content_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List digital sales collateral indexed for use in customer outreach."""
    where = []
    params: list = []
    if content_type:
        where.append("content_type = ?")
        params.append(content_type)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_digital_content WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT * FROM sale_digital_content
        WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


# ═══════════════════════════════════════════════════════════════
# sale_product_categories — 7 KHKD product groups
# ═══════════════════════════════════════════════════════════════

@router.get("/product-categories")
async def list_product_categories():
    """7 KHKD product groups (HRSG, Diverter, Shipbuilding, PV, Handling, Duct, Other)."""
    items = query(
        "SELECT * FROM sale_product_categories ORDER BY code"
    )
    return {"items": items, "count": len(items)}


# ═══════════════════════════════════════════════════════════════
# Signal lifecycle actions (Phase 2 step 10)
# ═══════════════════════════════════════════════════════════════
#
# A signal is born NEW. The salesperson reviews it and:
#   - acknowledges (seen, not actioned) → ACKNOWLEDGED
#   - dismisses (irrelevant) → DISMISSED + dismiss_reason
#   - converts to opportunity → CONVERTED + converted_opportunity_id


def _load_signal_or_404(signal_id: str) -> dict:
    sig = query(
        "SELECT * FROM sale_market_signals WHERE id = ?",
        [signal_id], one=True,
    )
    if not sig:
        raise EntityNotFoundError("MarketSignal", signal_id)
    return dict(sig)


@router.post("/signals/{signal_id}/acknowledge")
async def acknowledge_signal(
    signal_id: str,
    user: UserContext = Depends(get_current_writer),
):
    """Mark a signal as ACKNOWLEDGED — seen but not yet actioned."""
    sig = _load_signal_or_404(signal_id)
    current = (sig.get("status") or "NEW").upper()
    if current not in ("NEW", "DISMISSED"):
        return {"id": signal_id, "status": current, "no_change": True}

    now = datetime.now().isoformat()
    execute(
        """
        UPDATE sale_market_signals
        SET status = 'ACKNOWLEDGED', acknowledged_by = ?, acknowledged_at = ?,
            updated_at = ?
        WHERE id = ?
        """,
        [user.actor, now, now, signal_id],
    )
    log_status_change(
        "market_signal", signal_id, current, "ACKNOWLEDGED",
        changed_by=user.actor,
    )
    return {"id": signal_id, "status": "ACKNOWLEDGED",
            "acknowledged_by": user.actor, "acknowledged_at": now}


class _SignalDismiss(BaseModel):
    reason: str


@router.post("/signals/{signal_id}/dismiss")
async def dismiss_signal(
    signal_id: str,
    payload: _SignalDismiss,
    user: UserContext = Depends(get_current_writer),
):
    """Dismiss a signal as not actionable. Reason is required for audit."""
    sig = _load_signal_or_404(signal_id)
    current = (sig.get("status") or "NEW").upper()
    if current == "CONVERTED":
        raise HTTPException(
            status_code=422,
            detail="Cannot dismiss a signal already converted to an opportunity",
        )
    if current == "DISMISSED":
        return {"id": signal_id, "status": "DISMISSED", "no_change": True}

    now = datetime.now().isoformat()
    execute(
        """
        UPDATE sale_market_signals
        SET status = 'DISMISSED', dismiss_reason = ?, is_actionable = 0,
            updated_at = ?
        WHERE id = ?
        """,
        [payload.reason, now, signal_id],
    )
    log_status_change(
        "market_signal", signal_id, current, "DISMISSED",
        changed_by=user.actor,
    )
    return {"id": signal_id, "status": "DISMISSED", "reason": payload.reason}


class _SignalConvert(BaseModel):
    project_name: Optional[str] = None
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    product_group: Optional[str] = None
    contract_value_usd: Optional[float] = None
    win_probability: Optional[int] = 25
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


@router.post("/signals/{signal_id}/convert-to-opportunity")
async def convert_signal_to_opportunity(
    signal_id: str,
    payload: _SignalConvert,
    user: UserContext = Depends(get_current_writer),
):
    """Promote a market signal into a PROSPECT opportunity.

    Idempotent — if the signal is already CONVERTED, returns the
    existing opportunity_id.
    """
    sig = _load_signal_or_404(signal_id)
    current = (sig.get("status") or "NEW").upper()
    if current == "CONVERTED" and sig.get("converted_opportunity_id"):
        return {
            "id": signal_id,
            "status": "CONVERTED",
            "opportunity_id": sig["converted_opportunity_id"],
            "no_change": True,
        }

    customer_id = payload.customer_id or sig.get("related_customer_id")
    customer_name = payload.customer_name
    if customer_id and not customer_name:
        cust = query(
            "SELECT name FROM sale_customers WHERE id = ?",
            [customer_id], one=True,
        )
        if cust:
            customer_name = cust.get("name")
    if not customer_name:
        customer_name = sig.get("competitor_name") or "Unknown"

    project_name = payload.project_name or sig.get("title") or "Opportunity from signal"

    opp_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute(
        """
        INSERT INTO sale_opportunities
            (id, customer_id, customer_name, project_name, product_group,
             stage, contract_value_usd, win_probability,
             assigned_to, notes, last_activity_date, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 'PROSPECT', ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            opp_id, customer_id, customer_name, project_name,
            payload.product_group or sig.get("related_product_group") or "Other",
            payload.contract_value_usd, payload.win_probability or 25,
            payload.assigned_to,
            payload.notes or f"Converted from market signal: {sig.get('title')}",
            now, now, now,
        ],
    )

    execute(
        """
        UPDATE sale_market_signals
        SET status = 'CONVERTED', converted_opportunity_id = ?,
            actioned_by = ?, actioned_at = ?, updated_at = ?
        WHERE id = ?
        """,
        [opp_id, user.actor, now, now, signal_id],
    )
    log_status_change(
        "market_signal", signal_id, current, "CONVERTED",
        changed_by=user.actor,
    )

    return {
        "id": signal_id,
        "status": "CONVERTED",
        "opportunity_id": opp_id,
        "project_name": project_name,
    }
