"""KHKD target vs pipeline tracker for IBS HI Sale Platform.

Compares actual sales pipeline values against KHKD 2026-2027 targets.
Data comes from sale_khkd_targets (1 row) + sale_product_categories (7 rows).
"""

from typing import Dict, List, Any

import structlog

logger = structlog.get_logger(__name__)

# 7 product groups aligned with sale_product_categories.code
PRODUCT_GROUPS = ["HRSG", "DIVERTER", "SHIP", "PV", "HANDLING", "DUCT", "OTHER"]


def get_pipeline_vs_khkd() -> Dict[str, Any]:
    """Get consolidated pipeline vs KHKD targets.

    Compares total weighted value of active opportunities against
    KHKD fiscal year targets.

    Returns:
        Dict with target vs actual revenue, tons, GM, coverage ratio.
    """
    try:
        try:
            from ..database import query
        except ImportError:
            from database import query

        # Get KHKD targets (single row per fiscal year)
        khkd = query("""
            SELECT total_revenue_target, total_tons_target,
                   total_gm_pct_target, total_gm_value_target
            FROM sale_khkd_targets
            ORDER BY fiscal_year DESC LIMIT 1
        """, one=True)

        if not khkd:
            return {
                "target_revenue": 0, "actual_revenue": 0,
                "gap": 0, "coverage_ratio": 0.0,
            }

        target_revenue = khkd.get("total_revenue_target", 0) or 0
        target_tons = khkd.get("total_tons_target", 0) or 0
        target_gm_pct = khkd.get("total_gm_pct_target", 0) or 0
        target_gm_value = khkd.get("total_gm_value_target", 0) or 0

        # Get actual pipeline (active stages)
        pipeline = query("""
            SELECT
                COALESCE(SUM(contract_value_usd), 0) as total_value,
                COALESCE(SUM(contract_value_usd * win_probability / 100.0), 0) as weighted_value,
                COALESCE(SUM(weight_ton), 0) as total_tons
            FROM sale_opportunities
            WHERE stage NOT IN ('LOST', 'PROSPECT')
        """, one=True) or {}

        actual_revenue = pipeline.get("weighted_value", 0) or 0
        total_value = pipeline.get("total_value", 0) or 0
        actual_tons = pipeline.get("total_tons", 0) or 0

        gap = target_revenue - actual_revenue

        return {
            "fiscal_year": khkd.get("fiscal_year", "N/A"),
            "target_revenue": float(target_revenue),
            "actual_revenue": round(float(actual_revenue), 2),
            "total_pipeline_value": round(float(total_value), 2),
            "gap": round(float(gap), 2),
            "coverage_ratio": round(
                (actual_revenue / target_revenue * 100) if target_revenue > 0 else 0, 1
            ),
            "target_tons": float(target_tons),
            "actual_tons": float(actual_tons),
            "target_gm_pct": float(target_gm_pct),
            "target_gm_value": float(target_gm_value),
        }

    except Exception as e:
        logger.error("khkd_tracker_error", error=str(e))
        return {}


def get_by_product_group() -> List[Dict[str, Any]]:
    """Get pipeline vs KHKD breakdown by 7 product groups.

    Uses sale_product_categories for targets and sale_opportunities
    for actuals. Groups by product_group column.

    Returns:
        List of dicts with target vs actual per product group.
    """
    try:
        try:
            from ..database import query
        except ImportError:
            from database import query

        # Get product categories with targets
        categories = query("""
            SELECT code, name_en, name_vn,
                   target_tons, target_revenue, target_gm_pct
            FROM sale_product_categories
            ORDER BY code
        """)

        if not categories:
            return []

        results = []
        for cat in categories:
            code = cat.get("code")

            # Get pipeline for this product group
            pipeline = query("""
                SELECT
                    COUNT(*) as count,
                    COALESCE(SUM(contract_value_usd), 0) as total_value,
                    COALESCE(SUM(contract_value_usd * win_probability / 100.0), 0) as weighted_value,
                    COALESCE(SUM(weight_ton), 0) as total_tons
                FROM sale_opportunities
                WHERE product_group = ? AND stage NOT IN ('LOST', 'PROSPECT')
            """, [code], one=True) or {}

            target_rev = cat.get("target_revenue", 0) or 0
            actual_rev = pipeline.get("weighted_value", 0) or 0

            results.append({
                "product_group": code,
                "name_en": cat.get("name_en"),
                "name_vn": cat.get("name_vn"),
                "count": pipeline.get("count", 0),
                "target_revenue": float(target_rev),
                "actual_weighted": round(float(actual_rev), 2),
                "total_pipeline": float(pipeline.get("total_value", 0) or 0),
                "gap": round(float(target_rev) - float(actual_rev), 2),
                "coverage_ratio": round(
                    (actual_rev / target_rev * 100) if target_rev > 0 else 0, 1
                ),
                "target_tons": float(cat.get("target_tons", 0) or 0),
                "actual_tons": float(pipeline.get("total_tons", 0) or 0),
                "target_gm_pct": float(cat.get("target_gm_pct", 0) or 0),
            })

        return results

    except Exception as e:
        logger.error("khkd_by_group_error", error=str(e))
        return []


def check_coverage_status(threshold_pct: float = 80.0) -> Dict[str, Any]:
    """Check if pipeline covers KHKD targets above threshold.

    Args:
        threshold_pct: Minimum coverage percentage (default 80%).

    Returns:
        Dict with overall_coverage, by_group breakdown, and at-risk alerts.
    """
    summary = get_pipeline_vs_khkd()
    by_group = get_by_product_group()

    at_risk = [g for g in by_group if g.get("coverage_ratio", 0) < threshold_pct]

    return {
        "overall_coverage": summary.get("coverage_ratio", 0),
        "by_group": by_group,
        "at_risk_groups": at_risk,
        "is_on_track": summary.get("coverage_ratio", 0) >= threshold_pct,
        "alert_count": len(at_risk),
    }
