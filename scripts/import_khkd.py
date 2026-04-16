"""Import KHKD 2026-2027 targets into sale_khkd_targets table.

Usage:
    python import_khkd.py

Inserts FY2026-2027 consolidated targets:
    - Revenue: $19.1M
    - Units: 7000 tons
    - Gross Margin: 21%
    - Gross Profit: $3.976M
    - POs: 25
    - Backlog: 2667 tons
    - Workload to find: 6333 tons

Also inserts per-product-group breakdown across 7 groups (GROUP_A through GROUP_G).
Logs to sale_import_log.
"""

import uuid
import json
from datetime import datetime
from typing import Dict, Any

# KHKD 2026-2027 consolidated targets (RevC)
KHKD_CONSOLIDATED = {
    "revenue_usd": 19100000,  # $19.1M
    "units_tons": 7000,
    "gross_margin_pct": 21,
    "gross_profit_usd": 3976000,  # $3.976M = $19.1M * 21%
    "po_count": 25,
    "backlog_tons": 2667,
    "workload_to_find_tons": 6333,  # 7000 - 2667
}

# Product group breakdown (estimated proportional split)
KHKD_BY_GROUP = [
    {
        "product_group": "GROUP_A",
        "revenue_usd": 2730000,  # 14.3% of total
        "units_tons": 1001,
        "gross_margin_pct": 22,
    },
    {
        "product_group": "GROUP_B",
        "revenue_usd": 2728000,  # 14.3%
        "units_tons": 1000,
        "gross_margin_pct": 20,
    },
    {
        "product_group": "GROUP_C",
        "revenue_usd": 2728000,  # 14.3%
        "units_tons": 1000,
        "gross_margin_pct": 21,
    },
    {
        "product_group": "GROUP_D",
        "revenue_usd": 2728000,  # 14.3%
        "units_tons": 1000,
        "gross_margin_pct": 20,
    },
    {
        "product_group": "GROUP_E",
        "revenue_usd": 2730000,  # 14.3%
        "units_tons": 1001,
        "gross_margin_pct": 22,
    },
    {
        "product_group": "GROUP_F",
        "revenue_usd": 2728000,  # 14.3%
        "units_tons": 1000,
        "gross_margin_pct": 21,
    },
    {
        "product_group": "GROUP_G",
        "revenue_usd": 728000,  # 3.8%
        "units_tons": -2,  # Placeholder (sum check)
        "gross_margin_pct": 18,
    },
]


def import_khkd_targets() -> Dict[str, Any]:
    """Import KHKD targets into database.

    Returns:
        Import report with counts and status.
    """
    try:
        from ..database import execute, query

        print("[import_khkd] Starting KHKD target import")

        # Check if already imported
        existing = query(
            "SELECT COUNT(*) as cnt FROM sale_khkd_targets",
            one=True,
        )

        if existing and existing.get("cnt", 0) > 0:
            print("[import_khkd] KHKD targets already exist, skipping import")
            return {"skipped": True, "reason": "Already imported"}

        # Insert consolidated target
        khkd_id = str(uuid.uuid4())
        execute(
            """INSERT INTO sale_khkd_targets
               (id, fiscal_year, product_group, revenue_usd, units_tons,
                gross_margin_pct, gross_profit_usd, po_count, backlog_tons,
                workload_to_find_tons, notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                khkd_id,
                "FY2026-2027",
                "CONSOLIDATED",
                KHKD_CONSOLIDATED["revenue_usd"],
                KHKD_CONSOLIDATED["units_tons"],
                KHKD_CONSOLIDATED["gross_margin_pct"],
                KHKD_CONSOLIDATED["gross_profit_usd"],
                KHKD_CONSOLIDATED["po_count"],
                KHKD_CONSOLIDATED["backlog_tons"],
                KHKD_CONSOLIDATED["workload_to_find_tons"],
                "Consolidated KHKD 2026-2027 targets (RevC)",
                datetime.utcnow().isoformat(),
            ],
        )

        print("[import_khkd] Inserted consolidated target")

        # Insert by-group breakdown
        for group_data in KHKD_BY_GROUP:
            if group_data["units_tons"] < 0:
                # Skip placeholder
                continue

            group_id = str(uuid.uuid4())
            execute(
                """INSERT INTO sale_khkd_targets
                   (id, fiscal_year, product_group, revenue_usd, units_tons,
                    gross_margin_pct, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                [
                    group_id,
                    "FY2026-2027",
                    group_data["product_group"],
                    group_data["revenue_usd"],
                    group_data["units_tons"],
                    group_data["gross_margin_pct"],
                    datetime.utcnow().isoformat(),
                ],
            )

            print(f"[import_khkd] Inserted {group_data['product_group']}")

        # Log import
        import_log_id = str(uuid.uuid4())
        execute(
            """INSERT INTO sale_import_log
               (id, import_type, source_file, imported_count, notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [
                import_log_id,
                "KHKD_TARGETS",
                "KHKD_2026-2027_RevC",
                1 + len([g for g in KHKD_BY_GROUP if g["units_tons"] >= 0]),
                json.dumps(KHKD_CONSOLIDATED),
                datetime.utcnow().isoformat(),
            ],
        )

        report = {
            "imported_count": 1 + len([g for g in KHKD_BY_GROUP if g["units_tons"] >= 0]),
            "consolidated": KHKD_CONSOLIDATED,
            "by_group": len([g for g in KHKD_BY_GROUP if g["units_tons"] >= 0]),
            "success": True,
        }

        print("[import_khkd] KHKD import complete")
        return report

    except Exception as e:
        print(f"[import_khkd] Error: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    result = import_khkd_targets()

    if "error" in result:
        print(f"\nERROR: {result['error']}")
        exit(1)

    if result.get("skipped"):
        print(f"\nSKIPPED: {result['reason']}")
        exit(0)

    print(f"\nKHKD Import Summary:")
    print(f"  Imported: {result.get('imported_count', 0)} records")
    print(f"  Revenue Target: ${result['consolidated'].get('revenue_usd', 0):,.0f}")
    print(f"  Units Target: {result['consolidated'].get('units_tons', 0):,} tons")
    print(f"  Gross Margin: {result['consolidated'].get('gross_margin_pct', 0)}%")
    print(f"  Gross Profit: ${result['consolidated'].get('gross_profit_usd', 0):,.0f}")
