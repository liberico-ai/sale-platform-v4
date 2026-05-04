"""Report generation engine (Phase 2 step 12).

Loads a sale_report_configs row, runs the right query for the report
type, and serialises to JSON / CSV / XLSX. The router calls
``generate(config_id, format)`` and gets back a dict + raw bytes.

Report types supported:
    - PIPELINE   — opportunities by stage + product + KHKD comparison
    - SLA        — overdue tasks, breached SLAs, response times
    - QUOTATION  — win rate by product + salesperson + period
    - COMMISSION — by salesperson, by status, totals
    - CUSTOMER   — active/inactive, by region

XLSX support is optional — falls back to CSV with a warning if openpyxl
isn't installed.
"""

import csv
import io
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import structlog

try:
    from ..database import query
except ImportError:
    from database import query

logger = structlog.get_logger(__name__)


# ─────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────

REPORT_TYPES = {"PIPELINE", "SLA", "QUOTATION", "COMMISSION", "CUSTOMER"}
SUPPORTED_FORMATS = {"json", "csv", "xlsx"}


def generate(
    config: Dict[str, Any],
    fmt: str = "json",
    filters: Optional[Dict[str, Any]] = None,
) -> Tuple[Dict[str, Any], Optional[bytes]]:
    """Run a report config and serialise the result.

    Args:
        config: Row from sale_report_configs.
        fmt: 'json' | 'csv' | 'xlsx'.
        filters: Override config.filters JSON when running ad-hoc.

    Returns:
        (metadata, bytes_or_none) — bytes is None when fmt='json'.
    """
    fmt = (fmt or "json").lower()
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {fmt}")

    report_type = (config.get("report_type") or "").upper()
    if report_type not in REPORT_TYPES:
        raise ValueError(
            f"Unknown report type: {report_type}. "
            f"Supported: {sorted(REPORT_TYPES)}"
        )

    # Merge config.filters_json with override. Schema column is
    # filters_json; we also accept "filters" for forward-compat with
    # callers that build the dict in-memory.
    config_filters = (
        _parse_json(config.get("filters_json"))
        or _parse_json(config.get("filters"))
        or {}
    )
    merged = {**config_filters, **(filters or {})}

    rows, headers = _run_query(report_type, merged)

    metadata = {
        "config_id": config.get("id"),
        "config_name": (
            config.get("report_name") or config.get("name") or report_type
        ),
        "report_type": report_type,
        "format": fmt,
        "filters": merged,
        "row_count": len(rows),
        "generated_at": datetime.now().isoformat(),
    }

    if fmt == "json":
        metadata["rows"] = rows
        return metadata, None

    if fmt == "csv":
        return metadata, _to_csv(rows, headers)

    if fmt == "xlsx":
        try:
            return metadata, _to_xlsx(rows, headers, metadata)
        except ImportError:
            logger.warning("xlsx_fallback_to_csv", reason="openpyxl_missing")
            metadata["format"] = "csv"
            metadata["xlsx_fallback"] = True
            return metadata, _to_csv(rows, headers)

    raise ValueError(f"Unhandled format: {fmt}")


def default_configs() -> List[Dict[str, Any]]:
    """Five pre-built report configs the SPA can seed on first run."""
    return [
        {
            "name": "Pipeline by stage + product",
            "report_type": "PIPELINE",
            "description": "Opportunity totals grouped by stage and product group",
            "filters": {},
            "schedule_cron": None,
        },
        {
            "name": "SLA breaches",
            "report_type": "SLA",
            "description": "Overdue and breached tasks",
            "filters": {},
            "schedule_cron": None,
        },
        {
            "name": "Quotation win rate",
            "report_type": "QUOTATION",
            "description": "Win/loss rate by product type and salesperson",
            "filters": {},
            "schedule_cron": None,
        },
        {
            "name": "Commission by salesperson",
            "report_type": "COMMISSION",
            "description": "Commission totals by status and salesperson",
            "filters": {},
            "schedule_cron": None,
        },
        {
            "name": "Customer summary",
            "report_type": "CUSTOMER",
            "description": "Customers grouped by status and region",
            "filters": {},
            "schedule_cron": None,
        },
    ]


# ─────────────────────────────────────────────────────────────────
# Query plans per report type
# ─────────────────────────────────────────────────────────────────

def _run_query(report_type: str, filters: Dict[str, Any]) -> Tuple[List[dict], List[str]]:
    if report_type == "PIPELINE":
        return _pipeline(filters)
    if report_type == "SLA":
        return _sla(filters)
    if report_type == "QUOTATION":
        return _quotation(filters)
    if report_type == "COMMISSION":
        return _commission(filters)
    if report_type == "CUSTOMER":
        return _customer(filters)
    raise ValueError(f"No query plan for: {report_type}")


def _pipeline(filters: Dict[str, Any]) -> Tuple[List[dict], List[str]]:
    where, params = ["(stage IS NULL OR stage != 'DELETED')"], []
    if (pg := filters.get("product_group")):
        where.append("product_group = ?")
        params.append(pg)
    if (af := filters.get("assigned_to")):
        where.append("assigned_to = ?")
        params.append(af)

    rows = query(
        f"""
        SELECT
            stage,
            product_group,
            COUNT(*) AS opportunity_count,
            COALESCE(SUM(contract_value_usd), 0) AS total_value_usd,
            COALESCE(SUM(contract_value_usd * win_probability / 100.0), 0) AS weighted_value_usd,
            COALESCE(SUM(weight_ton), 0) AS total_tons
        FROM sale_opportunities
        WHERE {' AND '.join(where)}
        GROUP BY stage, product_group
        ORDER BY stage, product_group
        """,
        params,
    )
    headers = [
        "stage", "product_group", "opportunity_count",
        "total_value_usd", "weighted_value_usd", "total_tons",
    ]
    return rows, headers


def _sla(filters: Dict[str, Any]) -> Tuple[List[dict], List[str]]:
    rows = query(
        """
        SELECT
            t.id,
            t.task_type,
            t.title,
            t.status,
            t.assigned_to,
            t.from_dept,
            t.to_dept,
            t.priority,
            t.sla_hours,
            t.due_date,
            t.escalation_count,
            o.project_name,
            o.customer_name
        FROM sale_tasks t
        LEFT JOIN sale_opportunities o ON o.id = t.opportunity_id
        WHERE t.status IN ('OVERDUE', 'PENDING', 'IN_PROGRESS')
          AND t.due_date IS NOT NULL
        ORDER BY
            CASE t.status WHEN 'OVERDUE' THEN 0 WHEN 'PENDING' THEN 1 ELSE 2 END,
            t.due_date ASC
        """
    )
    headers = [
        "id", "task_type", "title", "status", "assigned_to",
        "from_dept", "to_dept", "priority", "sla_hours",
        "due_date", "escalation_count", "project_name", "customer_name",
    ]
    return rows, headers


def _quotation(filters: Dict[str, Any]) -> Tuple[List[dict], List[str]]:
    where, params = ["1=1"], []
    if (pt := filters.get("product_type")):
        where.append("product_type = ?")
        params.append(pt)
    if (year := filters.get("year")):
        where.append("strftime('%Y', date_offer) = ?")
        params.append(str(year))

    rows = query(
        f"""
        SELECT
            COALESCE(product_type, '(unspecified)') AS product_type,
            COALESCE(incharge, '(unassigned)') AS incharge,
            COUNT(*) AS total,
            SUM(CASE WHEN UPPER(status) = 'WON' THEN 1 ELSE 0 END) AS won,
            SUM(CASE WHEN UPPER(status) = 'LOST' THEN 1 ELSE 0 END) AS lost,
            COALESCE(SUM(value_usd), 0) AS total_value_usd,
            COALESCE(SUM(CASE WHEN UPPER(status) = 'WON' THEN value_usd END), 0) AS won_value_usd
        FROM sale_quotation_history
        WHERE {' AND '.join(where)}
        GROUP BY product_type, incharge
        ORDER BY total DESC
        """,
        params,
    )
    # Compute win rate per row in Python — clearer than SQL CASE.
    for r in rows:
        total = r.get("total") or 0
        won = r.get("won") or 0
        r["win_rate_pct"] = round((won / total * 100) if total else 0, 1)

    headers = [
        "product_type", "incharge", "total", "won", "lost",
        "win_rate_pct", "total_value_usd", "won_value_usd",
    ]
    return rows, headers


def _commission(filters: Dict[str, Any]) -> Tuple[List[dict], List[str]]:
    where, params = ["1=1"], []
    if (fy := filters.get("fiscal_year")):
        where.append("fiscal_year = ?")
        params.append(str(fy))
    if (status := filters.get("status")):
        where.append("status = ?")
        params.append(status)

    rows = query(
        f"""
        SELECT
            salesperson,
            fiscal_year,
            status,
            COUNT(*) AS deal_count,
            COALESCE(SUM(contract_value_usd), 0) AS total_contract_value,
            COALESCE(SUM(commission_amount_usd), 0) AS total_commission_usd,
            COALESCE(SUM(bonus_amount), 0) AS total_bonus_usd
        FROM sale_commissions
        WHERE {' AND '.join(where)}
        GROUP BY salesperson, fiscal_year, status
        ORDER BY salesperson, fiscal_year, status
        """,
        params,
    )
    headers = [
        "salesperson", "fiscal_year", "status",
        "deal_count", "total_contract_value",
        "total_commission_usd", "total_bonus_usd",
    ]
    return rows, headers


def _customer(filters: Dict[str, Any]) -> Tuple[List[dict], List[str]]:
    where, params = ["1=1"], []
    if (region := filters.get("region")):
        where.append("region = ?")
        params.append(region)
    if (status := filters.get("status")):
        where.append("status = ?")
        params.append(status)
    else:
        where.append("(status IS NULL OR status != 'DELETED')")

    rows = query(
        f"""
        SELECT
            COALESCE(status, 'UNKNOWN') AS status,
            COALESCE(region, '(unspecified)') AS region,
            COALESCE(country, '(unspecified)') AS country,
            COUNT(*) AS customer_count
        FROM sale_customers
        WHERE {' AND '.join(where)}
        GROUP BY status, region, country
        ORDER BY status, region, customer_count DESC
        """,
        params,
    )
    headers = ["status", "region", "country", "customer_count"]
    return rows, headers


# ─────────────────────────────────────────────────────────────────
# Serialisers
# ─────────────────────────────────────────────────────────────────

def _to_csv(rows: List[dict], headers: List[str]) -> bytes:
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=headers, extrasaction="ignore")
    writer.writeheader()
    for r in rows:
        writer.writerow({h: r.get(h, "") for h in headers})
    return out.getvalue().encode("utf-8")


def _to_xlsx(
    rows: List[dict], headers: List[str], metadata: Dict[str, Any]
) -> bytes:
    """Render rows + metadata as a multi-sheet xlsx workbook."""
    from openpyxl import Workbook  # imported lazily — optional dep

    wb = Workbook()
    data_sheet = wb.active
    data_sheet.title = "Data"

    data_sheet.append(headers)
    for r in rows:
        data_sheet.append([r.get(h, "") for h in headers])

    meta_sheet = wb.create_sheet("Report Metadata")
    meta_sheet.append(["Field", "Value"])
    for k in (
        "config_id", "config_name", "report_type",
        "row_count", "generated_at",
    ):
        meta_sheet.append([k, str(metadata.get(k) or "")])

    # Filters as JSON for traceability.
    meta_sheet.append(
        ["filters", json.dumps(metadata.get("filters") or {}, default=str)]
    )

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def _parse_json(value: Any) -> Optional[dict]:
    if not value:
        return None
    if isinstance(value, dict):
        return value
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return None
