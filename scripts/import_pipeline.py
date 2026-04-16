"""Import sales pipeline from IBSHI Potential Excel into sale_opportunities table.

Usage:
    python import_pipeline.py <ibshi_potential.xlsx>

Expected: ~25 deals with 2025/2026 revenue splits.
Maps columns: PL/HD, product_group, customer, values, dates, win probability.
Logs all imports to sale_import_log.
"""

import sys
import uuid
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Expected columns from IBSHI Potential
EXPECTED_COLUMNS = [
    "opportunity_code",
    "project_name",
    "customer_code",
    "customer_name",
    "product_group",
    "stage",
    "estimated_value_usd",
    "estimated_units",
    "gross_margin_pct",
    "win_probability",
    "expected_close_date",
    "assigned_to",
    "notes",
]


def import_pipeline_from_file(source_file: str) -> Dict[str, Any]:
    """Import pipeline from Excel file.

    Args:
        source_file: Path to Excel file (IBSHI Potential).

    Returns:
        Import report dict with counts, errors, etc.
    """
    source_path = Path(source_file)
    if not source_path.exists():
        return {"error": f"File not found: {source_file}"}

    print(f"[import_pipeline] Loading {source_file}")

    # Read Excel
    try:
        import openpyxl
        wb = openpyxl.load_workbook(source_file)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
    except ImportError:
        return {"error": "openpyxl not installed. Install with: pip install openpyxl"}
    except Exception as e:
        return {"error": f"Failed to read Excel: {e}"}

    if not rows:
        return {"error": "File is empty"}

    # Parse header
    header = rows[0]
    data_rows = rows[1:]

    print(f"[import_pipeline] Found {len(data_rows)} opportunity records")

    # Import
    try:
        from ..database import execute, query

        imported_count = 0
        skipped_count = 0
        error_count = 0
        seen_codes = set()
        total_value = 0.0

        for idx, row in enumerate(data_rows, start=2):
            try:
                # Parse row
                record = {}
                for col_idx, col_name in enumerate(header):
                    if col_idx < len(row):
                        record[col_name.lower().strip()] = row[col_idx]

                # Validate required fields
                code = record.get("opportunity_code", "").strip()
                name = record.get("project_name", "").strip()
                customer_name = record.get("customer_name", "").strip()

                if not code or not name:
                    print(f"[import_pipeline] Row {idx}: Missing code or name, skipping")
                    skipped_count += 1
                    continue

                # Dedup by code
                if code in seen_codes:
                    print(f"[import_pipeline] Row {idx}: Duplicate {code}, skipping")
                    skipped_count += 1
                    continue

                seen_codes.add(code)

                # Check if already in DB
                existing = query(
                    "SELECT id FROM sale_opportunities WHERE opportunity_code = ?",
                    [code],
                    one=True,
                )

                if existing:
                    print(f"[import_pipeline] Row {idx}: Code {code} already exists, skipping")
                    skipped_count += 1
                    continue

                # Parse values
                est_value = _parse_float(record.get("estimated_value_usd", 0))
                est_units = _parse_float(record.get("estimated_units", 0))
                gm_pct = _parse_float(record.get("gross_margin_pct", 0))
                win_prob = _parse_float(record.get("win_probability", 50)) / 100.0

                # Find customer by name or code
                customer_code = record.get("customer_code", "").strip()
                customer = query(
                    """SELECT id FROM sale_customers
                       WHERE customer_name = ? OR customer_code = ?""",
                    [customer_name, customer_code],
                    one=True,
                )

                customer_id = customer["id"] if customer else None

                # Parse close date
                close_date = record.get("expected_close_date")
                if close_date and isinstance(close_date, str):
                    try:
                        close_date = datetime.fromisoformat(close_date.split("T")[0])
                    except Exception:
                        close_date = datetime.utcnow()
                else:
                    close_date = datetime.utcnow()

                # Insert opportunity
                opp_id = str(uuid.uuid4())
                execute(
                    """INSERT INTO sale_opportunities
                       (id, opportunity_code, project_name, customer_id, customer_name,
                        product_group, stage, estimated_value_usd, estimated_units,
                        gross_margin_pct, win_probability, expected_close_date,
                        assigned_to, notes, created_at, last_activity_date)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    [
                        opp_id,
                        code,
                        name,
                        customer_id,
                        customer_name,
                        record.get("product_group", "GROUP_A").strip(),
                        record.get("stage", "QUALIFIED").strip(),
                        est_value,
                        est_units,
                        gm_pct,
                        win_prob,
                        close_date.isoformat(),
                        record.get("assigned_to", "SALES_STAFF").strip(),
                        record.get("notes", "").strip(),
                        datetime.utcnow().isoformat(),
                        datetime.utcnow().isoformat(),
                    ],
                )

                imported_count += 1
                total_value += est_value
                print(f"[import_pipeline] Row {idx}: {name} (${est_value:,.0f})")

            except Exception as e:
                print(f"[import_pipeline] Row {idx} error: {e}")
                error_count += 1
                continue

        # Log import
        try:
            import_log_id = str(uuid.uuid4())
            execute(
                """INSERT INTO sale_import_log
                   (id, import_type, source_file, imported_count, skipped_count,
                    error_count, notes, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    import_log_id,
                    "PIPELINE",
                    source_file,
                    imported_count,
                    skipped_count,
                    error_count,
                    json.dumps({"total_value_usd": total_value}),
                    datetime.utcnow().isoformat(),
                ],
            )
        except Exception:
            pass

        report = {
            "imported_count": imported_count,
            "skipped_count": skipped_count,
            "error_count": error_count,
            "total_rows": len(data_rows),
            "total_value_usd": total_value,
            "success": error_count == 0,
        }

        print(
            f"[import_pipeline] Complete: {imported_count} imported, "
            f"${total_value:,.0f} total value"
        )

        return report

    except Exception as e:
        return {"error": str(e)}


def _parse_float(value: Any) -> float:
    """Parse value to float.

    Args:
        value: Value to parse.

    Returns:
        Float value or 0.0 if unparseable.
    """
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            # Remove currency symbols and commas
            clean = value.replace("$", "").replace(",", "").strip()
            return float(clean)
        except ValueError:
            return 0.0
    return 0.0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_pipeline.py <ibshi_potential.xlsx>")
        sys.exit(1)

    result = import_pipeline_from_file(sys.argv[1])

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    print(f"\nImport Summary:")
    print(f"  Imported: {result.get('imported_count', 0)}")
    print(f"  Skipped: {result.get('skipped_count', 0)}")
    print(f"  Errors: {result.get('error_count', 0)}")
    print(f"  Total Value: ${result.get('total_value_usd', 0):,.0f}")
