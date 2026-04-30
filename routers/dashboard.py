"""Dashboard Router — KPIs, pipeline analysis, task/email statistics.

Provides executive-level view aligned with KHKD targets and product categories.
"""

from fastapi import APIRouter
from datetime import datetime

import structlog

try:
    from ..database import query
except ImportError:
    from database import query

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/pipeline")
async def get_pipeline_kpis():
    """Get pipeline KPIs vs KHKD targets.

    Includes total weighted value, coverage ratio, and breakdown by stage.

    Returns:
        Pipeline KPIs with KHKD target comparisons.
    """
    # Get KHKD targets
    khkd = query(
        "SELECT * FROM sale_khkd_targets ORDER BY fiscal_year DESC LIMIT 1",
        one=True
    ) or {}

    # Get pipeline stats (active deals only)
    pipeline = query("""
        SELECT
            COUNT(*) as total_opps,
            COALESCE(SUM(contract_value_usd * win_probability / 100.0), 0) as weighted_value,
            COALESCE(SUM(contract_value_usd), 0) as total_value,
            COALESCE(SUM(weight_ton), 0) as total_tons,
            COUNT(DISTINCT assigned_to) as num_ams
        FROM sale_opportunities
        WHERE stage NOT IN ('LOST')
    """, one=True) or {}

    # By stage
    by_stage = query("""
        SELECT stage, COUNT(*) as count,
               COALESCE(SUM(contract_value_usd), 0) as total_value
        FROM sale_opportunities
        WHERE stage NOT IN ('LOST')
        GROUP BY stage
        ORDER BY stage
    """)

    weighted = pipeline.get("weighted_value", 0) or 0
    target_revenue = khkd.get("total_revenue_target", 0) or 0

    return {
        "fiscal_year": khkd.get("fiscal_year", "N/A"),
        "pipeline": {
            "total_opportunities": pipeline.get("total_opps", 0),
            "weighted_value_usd": round(weighted, 2),
            "total_value_usd": pipeline.get("total_value", 0),
            "total_tons": pipeline.get("total_tons", 0),
            "num_ams": pipeline.get("num_ams", 0),
        },
        "khkd_target": {
            "total_revenue": target_revenue,
            "total_tons": khkd.get("total_tons_target", 0),
            "total_gm_pct": khkd.get("total_gm_pct_target", 0),
            "total_gm_value": khkd.get("total_gm_value_target", 0),
        },
        "coverage_ratio_pct": round(
            (weighted / target_revenue * 100) if target_revenue > 0 else 0, 1
        ),
        "by_stage": by_stage,
    }


@router.get("/pipeline/by-product")
async def get_pipeline_by_product():
    """Get pipeline breakdown by 7 KHKD product groups with target comparison.

    Returns:
        Product group breakdown with KHKD targets.
    """
    # Get product categories with targets
    categories = query("""
        SELECT code, name_en, name_vn, target_tons, target_unit_price,
               target_revenue, target_gm_pct, target_gm_value
        FROM sale_product_categories
        ORDER BY code
    """)

    breakdown = []
    for cat in categories:
        code = cat.get("code")
        stats = query("""
            SELECT
                COUNT(*) as count,
                COALESCE(SUM(contract_value_usd), 0) as total_value,
                COALESCE(SUM(weight_ton), 0) as total_tons,
                COALESCE(SUM(contract_value_usd * win_probability / 100.0), 0) as weighted_value
            FROM sale_opportunities
            WHERE product_group = ? AND stage NOT IN ('LOST')
        """, [code], one=True) or {}

        breakdown.append({
            "product_group": code,
            "name_en": cat.get("name_en"),
            "name_vn": cat.get("name_vn"),
            "count": stats.get("count", 0),
            "total_value": stats.get("total_value", 0),
            "total_tons": stats.get("total_tons", 0),
            "weighted_value": stats.get("weighted_value", 0),
            "target_revenue": cat.get("target_revenue", 0),
            "target_tons": cat.get("target_tons", 0),
            "target_gm_pct": cat.get("target_gm_pct", 0),
        })

    return {"breakdown": breakdown}


@router.get("/pipeline/by-quarter")
async def get_pipeline_by_quarter():
    """Get revenue by quarter based on estimated_signing date.

    Returns:
        Revenue grouped by quarter.
    """
    quarters = query("""
        SELECT
            CAST(strftime('%Y', estimated_signing) AS TEXT) as year,
            CASE
                WHEN strftime('%m', estimated_signing) IN ('01', '02', '03') THEN 'Q1'
                WHEN strftime('%m', estimated_signing) IN ('04', '05', '06') THEN 'Q2'
                WHEN strftime('%m', estimated_signing) IN ('07', '08', '09') THEN 'Q3'
                ELSE 'Q4'
            END as quarter,
            COUNT(*) as count,
            COALESCE(SUM(contract_value_usd), 0) as total_value,
            COALESCE(SUM(contract_value_usd * win_probability / 100.0), 0) as weighted_value
        FROM sale_opportunities
        WHERE estimated_signing IS NOT NULL AND stage NOT IN ('LOST')
        GROUP BY year, quarter
        ORDER BY year DESC, quarter DESC
    """)

    return {"by_quarter": quarters}


@router.get("/tasks")
async def get_task_stats():
    """Get task statistics: total, overdue, pending, by department.

    Returns:
        Task statistics with department breakdown.
    """
    total_stats = query("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status = 'OVERDUE' THEN 1 ELSE 0 END) as overdue,
            SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN status = 'IN_PROGRESS' THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) as completed
        FROM sale_tasks
    """, one=True) or {}

    by_dept = query("""
        SELECT to_dept, status, COUNT(*) as count
        FROM sale_tasks
        GROUP BY to_dept, status
        ORDER BY to_dept, status
    """)

    return {
        "total": total_stats.get("total", 0),
        "overdue": total_stats.get("overdue", 0),
        "pending": total_stats.get("pending", 0),
        "in_progress": total_stats.get("in_progress", 0),
        "completed": total_stats.get("completed", 0),
        "by_department": by_dept,
    }


@router.get("/emails")
async def get_email_stats():
    """Get email statistics: unread, unactioned, grouped by type.

    Returns:
        Email statistics.
    """
    total_stats = query("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN is_read = 0 THEN 1 ELSE 0 END) as unread,
            SUM(CASE WHEN is_actioned = 0 THEN 1 ELSE 0 END) as unactioned,
            SUM(CASE WHEN is_actioned = 1 THEN 1 ELSE 0 END) as actioned
        FROM sale_emails
    """, one=True) or {}

    by_type = query("""
        SELECT email_type, COUNT(*) as count
        FROM sale_emails
        GROUP BY email_type
        ORDER BY count DESC
    """)

    return {
        "total": total_stats.get("total", 0),
        "unread": total_stats.get("unread", 0),
        "unactioned": total_stats.get("unactioned", 0),
        "actioned": total_stats.get("actioned", 0),
        "by_type": by_type,
    }


@router.get("/executive")
async def get_executive_overview():
    """BD Director executive overview with all combined KPIs.

    Returns:
        Comprehensive executive dashboard with pipeline, tasks, emails, KHKD.
    """
    # Pipeline KPIs
    pipeline = query("""
        SELECT
            COUNT(*) as total_opps,
            COALESCE(SUM(contract_value_usd * win_probability / 100.0), 0) as weighted_value,
            COALESCE(SUM(contract_value_usd), 0) as total_value
        FROM sale_opportunities
        WHERE stage NOT IN ('LOST')
    """, one=True) or {}

    # KHKD Target
    khkd = query("""
        SELECT total_revenue_target, total_gm_value_target
        FROM sale_khkd_targets
        ORDER BY fiscal_year DESC LIMIT 1
    """, one=True) or {}

    # Task Stats
    task_stats = query("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status = 'OVERDUE' THEN 1 ELSE 0 END) as overdue,
            SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) as pending
        FROM sale_tasks
    """, one=True) or {}

    # Email Stats
    email_stats = query("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN is_read = 0 THEN 1 ELSE 0 END) as unread,
            SUM(CASE WHEN is_actioned = 0 THEN 1 ELSE 0 END) as unactioned
        FROM sale_emails
    """, one=True) or {}

    weighted = pipeline.get("weighted_value", 0) or 0
    target = khkd.get("total_revenue_target", 0) or 0

    return {
        "timestamp": datetime.now().isoformat(),
        "pipeline": {
            "total_opportunities": pipeline.get("total_opps", 0),
            "weighted_value_usd": round(weighted, 2),
            "total_value_usd": pipeline.get("total_value", 0),
        },
        "khkd_progress": {
            "target_revenue": target,
            "weighted_pipeline": round(weighted, 2),
            "coverage_pct": round(
                (weighted / target * 100) if target > 0 else 0, 1
            ),
        },
        "tasks": {
            "total": task_stats.get("total", 0),
            "overdue": task_stats.get("overdue", 0),
            "pending": task_stats.get("pending", 0),
        },
        "emails": {
            "total": email_stats.get("total", 0),
            "unread": email_stats.get("unread", 0),
            "unactioned": email_stats.get("unactioned", 0),
        },
    }


# ═══════════════════════════════════════════════════════════════
# /summary — full 32-table aggregate dashboard
# ═══════════════════════════════════════════════════════════════

# Tables surfaced as record counts in /summary. Kept in one place
# so adding/removing tables only touches this list.
_SUMMARY_TABLES = [
    "sale_customers",
    "sale_customer_contacts",
    "sale_customer_interactions",
    "sale_product_categories",
    "sale_opportunities",
    "sale_quotation_revisions",
    "sale_quotation_history",
    "sale_active_contracts",
    "sale_contract_milestones",
    "sale_change_orders",
    "sale_settlements",
    "sale_emails",
    "sale_email_full",
    "sale_email_labels",
    "sale_email_activity_log",
    "sale_tasks",
    "sale_follow_up_schedules",
    "sale_nas_file_links",
    "sale_market_signals",
    "sale_product_opportunities",
    "sale_digital_content",
    "sale_khkd_targets",
    "sale_audit_log",
    "sale_import_log",
    "sale_pm_sync_log",
]


@router.get("/summary")
async def get_summary():
    """Full 32-table aggregate dashboard.

    Combines pipeline coverage, milestone health, settlement status, follow-ups,
    market signals, and table-level record counts. Designed for the BD Director
    landing page.
    """
    now = datetime.now().isoformat()

    # ── Pipeline ─────────────────────────────────────────────────
    pipeline = query(
        """
        SELECT
            COUNT(*) AS total_opps,
            COALESCE(SUM(contract_value_usd * win_probability / 100.0), 0) AS weighted_value,
            COALESCE(SUM(contract_value_usd), 0) AS total_value,
            COALESCE(SUM(weight_ton), 0) AS total_tons,
            SUM(CASE WHEN stage = 'WON' THEN 1 ELSE 0 END) AS won_count,
            SUM(CASE WHEN stage = 'LOST' THEN 1 ELSE 0 END) AS lost_count,
            SUM(CASE WHEN stale_flag = 1 THEN 1 ELSE 0 END) AS stale_count
        FROM sale_opportunities
        """,
        one=True,
    ) or {}

    by_stage = query(
        """
        SELECT stage, COUNT(*) AS count,
               COALESCE(SUM(contract_value_usd), 0) AS total_value
        FROM sale_opportunities
        WHERE stage NOT IN ('LOST')
        GROUP BY stage
        """
    )

    # ── KHKD ────────────────────────────────────────────────────
    khkd = query(
        "SELECT * FROM sale_khkd_targets ORDER BY fiscal_year DESC LIMIT 1",
        one=True,
    ) or {}

    # ── Milestones / Settlements ────────────────────────────────
    milestones = query(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN invoice_status = 'NOT_INVOICED' THEN 1 ELSE 0 END) AS not_invoiced,
            SUM(CASE WHEN invoice_status = 'INVOICED' THEN 1 ELSE 0 END) AS invoiced,
            SUM(CASE WHEN invoice_status = 'PAID' THEN 1 ELSE 0 END) AS paid,
            SUM(CASE WHEN overdue_days > 0 THEN 1 ELSE 0 END) AS overdue
        FROM sale_contract_milestones
        """,
        one=True,
    ) or {}

    settlements = query(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN settlement_status = 'OPEN' THEN 1 ELSE 0 END) AS open_count,
            SUM(CASE WHEN settlement_status = 'CLOSED' THEN 1 ELSE 0 END) AS closed_count,
            COALESCE(SUM(actual_revenue_usd), 0) AS total_actual_revenue,
            COALESCE(SUM(actual_gm_value), 0) AS total_actual_gm
        FROM sale_settlements
        """,
        one=True,
    ) or {}

    # ── Tasks / Emails / Signals ────────────────────────────────
    tasks = query(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'OVERDUE' THEN 1 ELSE 0 END) AS overdue,
            SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) AS pending,
            SUM(CASE WHEN status = 'IN_PROGRESS' THEN 1 ELSE 0 END) AS in_progress
        FROM sale_tasks
        """,
        one=True,
    ) or {}

    emails = query(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN is_read = 0 THEN 1 ELSE 0 END) AS unread,
            SUM(CASE WHEN is_actioned = 0 THEN 1 ELSE 0 END) AS unactioned
        FROM sale_emails
        """,
        one=True,
    ) or {}

    signals = query(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN impact_level = 'HIGH' THEN 1 ELSE 0 END) AS high_impact,
            SUM(CASE WHEN is_actionable = 1 THEN 1 ELSE 0 END) AS actionable
        FROM sale_market_signals
        """,
        one=True,
    ) or {}

    # ── Record counts (32 tables) ───────────────────────────────
    record_counts = {}
    for table in _SUMMARY_TABLES:
        try:
            row = query(f"SELECT COUNT(*) AS cnt FROM {table}", one=True) or {}
            record_counts[table] = row.get("cnt", 0)
        except Exception as exc:
            logger.warning("summary_count_failed", table=table, error=str(exc))
            record_counts[table] = None

    weighted = pipeline.get("weighted_value", 0) or 0
    target_revenue = khkd.get("total_revenue_target", 0) or 0

    return {
        "timestamp": now,
        "fiscal_year": khkd.get("fiscal_year", "N/A"),
        "pipeline": {
            "total_opportunities": pipeline.get("total_opps", 0),
            "weighted_value_usd": round(weighted, 2),
            "total_value_usd": pipeline.get("total_value", 0),
            "total_tons": pipeline.get("total_tons", 0),
            "won_count": pipeline.get("won_count", 0),
            "lost_count": pipeline.get("lost_count", 0),
            "stale_count": pipeline.get("stale_count", 0),
            "by_stage": by_stage,
        },
        "khkd_target": {
            "total_revenue": target_revenue,
            "total_tons": khkd.get("total_tons_target", 0),
            "total_gm_pct": khkd.get("total_gm_pct_target", 0),
            "total_gm_value": khkd.get("total_gm_value_target", 0),
            "total_po": khkd.get("total_po_target", 0),
            "coverage_pct": round(
                (weighted / target_revenue * 100) if target_revenue > 0 else 0, 1
            ),
        },
        "milestones": dict(milestones),
        "settlements": dict(settlements),
        "tasks": dict(tasks),
        "emails": dict(emails),
        "market_signals": dict(signals),
        "record_counts": record_counts,
    }
