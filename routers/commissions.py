"""Commissions Router — sale_commissions.

Tracks commission earned per won opportunity per salesperson. Includes
auto-calc helper that takes opportunity_id + tier + rate and computes
the commission amount in USD/VND.

Status flow: CALCULATED → APPROVED → PAID. CALCULATED can be edited
freely; APPROVED requires admin to roll back to CALCULATED. PAID is
terminal except for `payment_ref` corrections.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

import structlog

try:
    from ..database import query, execute
    from ..auth import UserContext, get_current_writer, get_current_admin
    from ..services.audit import log_status_change, log_financial_change
except ImportError:
    from database import query, execute
    from auth import UserContext, get_current_writer, get_current_admin
    from services.audit import log_status_change, log_financial_change

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/commissions", tags=["Commissions"])


# Default commission tiers (used by /calculate when caller doesn't override)
_DEFAULT_TIERS = {
    "STANDARD":  0.005,   # 0.5% — baseline
    "PREMIUM":   0.010,   # 1.0% — strategic deals
    "STRETCH":   0.015,   # 1.5% — over-quota / high GM
    "OVERRIDE":  0.020,   # 2.0% — director-only
}

_TRANSITIONS = {
    "CALCULATED": {"APPROVED", "VOID"},
    "APPROVED":   {"PAID", "CALCULATED"},     # CALCULATED for adjustments
    "PAID":       set(),                       # terminal except payment_ref
    "VOID":       set(),                       # terminal
}


class CommissionCreate(BaseModel):
    """Manual commission entry. For automatic calc, use POST /calculate."""
    opportunity_id: str
    salesperson: str
    fiscal_year: str
    salesperson_role: Optional[str] = None
    fiscal_quarter: Optional[str] = None
    contract_value_usd: Optional[float] = None
    gm_value_usd: Optional[float] = None
    gm_percent: Optional[float] = None
    commission_tier: Optional[str] = "STANDARD"
    commission_rate: Optional[float] = None
    commission_amount_usd: Optional[float] = None
    commission_amount_vnd: Optional[float] = None
    bonus_amount: Optional[float] = None
    adjustment: Optional[float] = None
    adjustment_reason: Optional[str] = None
    notes: Optional[str] = None


class CommissionCalculate(BaseModel):
    """Auto-calc from a won opportunity."""
    opportunity_id: str
    salesperson: Optional[str] = None        # falls back to opp.assigned_to
    fiscal_year: Optional[str] = None        # falls back to current year
    fiscal_quarter: Optional[str] = None
    commission_tier: Optional[str] = "STANDARD"
    commission_rate: Optional[float] = None  # overrides tier when set
    bonus_amount: Optional[float] = None
    adjustment: Optional[float] = None
    adjustment_reason: Optional[str] = None
    fx_rate_vnd: Optional[float] = None      # USD→VND multiplier; default 24500


class CommissionUpdate(BaseModel):
    status: Optional[str] = None
    commission_tier: Optional[str] = None
    commission_rate: Optional[float] = None
    commission_amount_usd: Optional[float] = None
    commission_amount_vnd: Optional[float] = None
    bonus_amount: Optional[float] = None
    adjustment: Optional[float] = None
    adjustment_reason: Optional[str] = None
    approved_by: Optional[str] = None
    paid_at: Optional[str] = None
    payment_ref: Optional[str] = None
    notes: Optional[str] = None


_AUDITED_FIELDS = {
    "commission_amount_usd", "commission_amount_vnd",
    "commission_rate", "bonus_amount", "adjustment",
}


def _validate(current: str, new: str):
    cur = (current or "CALCULATED").upper()
    nxt = (new or "").upper()
    allowed = _TRANSITIONS.get(cur, set())
    if nxt not in allowed:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid commission transition: {cur} → {nxt}. "
                   f"Allowed: {sorted(allowed) or 'terminal'}",
        )


@router.get("")
async def list_commissions(
    salesperson: Optional[str] = Query(None),
    fiscal_year: Optional[str] = Query(None),
    fiscal_quarter: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    opportunity_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List commission records."""
    where = []
    params: list = []
    for k, v in [
        ("salesperson", salesperson), ("fiscal_year", fiscal_year),
        ("fiscal_quarter", fiscal_quarter), ("status", status),
        ("opportunity_id", opportunity_id),
    ]:
        if v is not None:
            where.append(f"c.{k} = ?")
            params.append(v)
    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_commissions c WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT c.*, o.project_name, o.customer_name
        FROM sale_commissions c
        LEFT JOIN sale_opportunities o ON o.id = c.opportunity_id
        WHERE {where_sql}
        ORDER BY c.fiscal_year DESC, c.fiscal_quarter DESC, c.created_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/by-salesperson")
async def commissions_by_salesperson(
    fiscal_year: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Aggregate commissions per salesperson for a given FY (or all-time)."""
    where = ["1=1"]
    params: list = []
    if fiscal_year:
        where.append("fiscal_year = ?")
        params.append(fiscal_year)

    where_sql = " AND ".join(where)

    total = query(
        f"""
        SELECT COUNT(DISTINCT salesperson) AS cnt
        FROM sale_commissions
        WHERE {where_sql}
        """,
        params,
    )[0]["cnt"]

    rows = query(
        f"""
        SELECT
            salesperson,
            COUNT(*) AS deal_count,
            COALESCE(SUM(contract_value_usd), 0) AS total_contract_value,
            COALESCE(SUM(commission_amount_usd), 0) AS total_commission_usd,
            COALESCE(SUM(bonus_amount), 0) AS total_bonus_usd,
            COALESCE(SUM(adjustment), 0) AS total_adjustment_usd,
            SUM(CASE WHEN status = 'PAID' THEN 1 ELSE 0 END) AS paid_count,
            SUM(CASE WHEN status IN ('CALCULATED', 'APPROVED') THEN 1 ELSE 0 END) AS pending_count
        FROM sale_commissions
        WHERE {where_sql}
        GROUP BY salesperson
        ORDER BY total_commission_usd DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )
    return {
        "fiscal_year": fiscal_year,
        "total": total,
        "items": rows,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{commission_id}")
async def get_commission(commission_id: str):
    item = query(
        """
        SELECT c.*, o.project_name, o.customer_name
        FROM sale_commissions c
        LEFT JOIN sale_opportunities o ON o.id = c.opportunity_id
        WHERE c.id = ?
        """,
        [commission_id], one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Commission not found")
    return {"commission": dict(item)}


@router.post("/calculate")
async def calculate_commission(
    payload: CommissionCalculate,
    user: UserContext = Depends(get_current_writer),
):
    """Compute + insert a commission row from an opportunity.

    Pulls contract_value_usd, gm_value_usd, gm_percent from the opportunity.
    commission_amount_usd = contract_value * (rate or default tier rate)
                          + bonus_amount + adjustment.
    """
    opp = query(
        "SELECT * FROM sale_opportunities WHERE id = ?",
        [payload.opportunity_id], one=True,
    )
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    salesperson = payload.salesperson or opp.get("assigned_to")
    if not salesperson:
        raise HTTPException(
            status_code=400,
            detail="Salesperson not specified and opportunity has no assigned_to",
        )

    fy = payload.fiscal_year or str(datetime.now().year)
    tier = payload.commission_tier or "STANDARD"
    rate = payload.commission_rate
    if rate is None:
        rate = _DEFAULT_TIERS.get(tier, _DEFAULT_TIERS["STANDARD"])

    contract_value = opp.get("contract_value_usd") or 0
    base_commission = contract_value * rate
    bonus = payload.bonus_amount or 0
    adjustment = payload.adjustment or 0
    total_usd = base_commission + bonus + adjustment

    fx = payload.fx_rate_vnd or 24500
    total_vnd = total_usd * fx if total_usd else 0

    commission_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    execute(
        """
        INSERT INTO sale_commissions
            (id, opportunity_id, salesperson, salesperson_role,
             fiscal_year, fiscal_quarter,
             contract_value_usd, gm_value_usd, gm_percent,
             commission_tier, commission_rate,
             commission_amount_usd, commission_amount_vnd,
             bonus_amount, adjustment, adjustment_reason,
             status, calculation_date,
             created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                'CALCULATED', ?, ?, ?)
        """,
        [
            commission_id, payload.opportunity_id, salesperson, None,
            fy, payload.fiscal_quarter,
            contract_value, opp.get("gm_value_usd"), opp.get("gm_percent"),
            tier, rate,
            total_usd, total_vnd,
            bonus, adjustment, payload.adjustment_reason,
            now, now, now,
        ],
    )

    logger.info(
        "commission_calculated",
        commission_id=commission_id, opp_id=payload.opportunity_id,
        salesperson=salesperson, total_usd=total_usd,
    )

    return {
        "id": commission_id,
        "salesperson": salesperson,
        "fiscal_year": fy,
        "tier": tier,
        "rate": rate,
        "contract_value_usd": contract_value,
        "base_commission_usd": base_commission,
        "bonus": bonus,
        "adjustment": adjustment,
        "total_usd": total_usd,
        "total_vnd": total_vnd,
        "status": "CALCULATED",
    }


@router.post("")
async def create_commission(
    payload: CommissionCreate,
    user: UserContext = Depends(get_current_writer),
):
    """Manual commission entry. Use /calculate for auto-derived rows."""
    commission_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    cols = list(data.keys()) + ["id", "status", "calculation_date",
                                 "created_at", "updated_at"]
    values = list(data.values()) + [commission_id, "CALCULATED", now, now, now]
    placeholders = ",".join("?" * len(cols))

    execute(
        f"INSERT INTO sale_commissions ({','.join(cols)}) VALUES ({placeholders})",
        values,
    )
    return {"id": commission_id, "status": "CALCULATED"}


@router.patch("/{commission_id}")
async def update_commission(
    commission_id: str,
    payload: CommissionUpdate,
    user: UserContext = Depends(get_current_writer),
):
    """Update commission. status changes go through state machine, financial
    diffs go to audit log.
    """
    existing = query(
        "SELECT * FROM sale_commissions WHERE id = ?",
        [commission_id], one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Commission not found")

    data = (
        payload.model_dump(exclude_unset=True)
        if hasattr(payload, "model_dump")
        else payload.dict(exclude_unset=True)
    )
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    new_status = data.get("status")
    if new_status and new_status != existing.get("status"):
        _validate(existing.get("status") or "CALCULATED", new_status)
        log_status_change(
            "commission", commission_id,
            existing.get("status") or "", new_status,
            changed_by=user.actor,
        )
        if new_status == "APPROVED" and not existing.get("approved_at"):
            data["approved_at"] = datetime.now().isoformat()
        if new_status == "PAID" and not existing.get("paid_at"):
            data["paid_at"] = datetime.now().isoformat()

    diffs = {}
    for f in _AUDITED_FIELDS:
        if f in data and data[f] != existing.get(f):
            diffs[f] = (existing.get(f), data[f])
    if diffs:
        log_financial_change(
            "commission", commission_id, diffs,
            changed_by=user.actor,
        )

    sets = [f"{k} = ?" for k in data.keys()]
    sets.append("updated_at = ?")
    params = list(data.values()) + [datetime.now().isoformat(), commission_id]
    execute(
        f"UPDATE sale_commissions SET {', '.join(sets)} WHERE id = ?",
        params,
    )

    return {"id": commission_id, "status": "ok",
            "updated_fields": list(data.keys())}
