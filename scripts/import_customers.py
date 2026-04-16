"""Import customers from Workflow 2026 Excel/CSV into sale_customers table.

Usage:
    python import_customers.py <source_file.xlsx or .csv>

Expected: ~988 customer records with dedup by customer_code.
Inserts into sale_customers + sale_customer_contacts tables.
Logs all imports to sale_import_log.
"""

import sys
import uuid
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Expected columns from Workflow 2026
EXPECTED_COLUMNS = [
    "customer_code",
    "customer_name",
    "industry",
    "region",
    "country",
    "address",
    "contact_name",
    "contact_title",
    "contact_email",
    "contact_phone",
    "payment_terms",
    "status",
]


def import_customers_from_file(source_file: str) -> Dict[str, Any]:
    """Import customers from Excel or CSV file.

    Args:
        source_file: Path to Excel (.xlsx) or CSV file.

    Returns:
        Import report dict with counts, errors, etc.
    """
    source_path = Path(source_file)
    if not source_path.exists():
        return {"error": f"File not found: {source_file}"}

    print(f"[import_customers] Loading {source_file}")

    # Read file
    if source_path.suffix.lower() in [".xlsx", ".xls"]:
        try:
            import openpyxl
            wb = openpyxl.load_workbook(source_file)
            ws = wb.active
            rows = list(ws.iter_rows(values_only=True))
        except ImportError:
            return {"error": "openpyxl not installed. Install with: pip install openpyxl"}
    elif source_path.suffix.lower() == ".csv":
        import csv
        with open(source_file, encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
    else:
        return {"error": "File must be .xlsx, .xls, or .csv"}

    if not rows:
        return {"error": "File is empty"}

    # Parse header
    header = rows[0]
    data_rows = rows[1:]

    print(f"[import_customers] Found {len(data_rows)} records")

    # Import
    try:
        from ..database import execute, query

        imported_count = 0
        skipped_count = 0
        error_count = 0
        seen_codes = set()

        for idx, row in enumerate(data_rows, start=2):
            try:
                # Parse row into dict
                record = {}
                for col_idx, col_name in enumerate(header):
                    if col_idx < len(row):
                        record[col_name.lower().strip()] = row[col_idx]

                # Validate required fields
                code = record.get("customer_code", "").strip()
                name = record.get("customer_name", "").strip()

                if not code or not name:
                    print(f"[import_customers] Row {idx}: Missing code or name, skipping")
                    skipped_count += 1
                    continue

                # Dedup by code
                if code in seen_codes:
                    print(f"[import_customers] Row {idx}: Duplicate code {code}, skipping")
                    skipped_count += 1
                    continue

                seen_codes.add(code)

                # Check if already in DB
                existing = query(
                    "SELECT id FROM sale_customers WHERE customer_code = ?",
                    [code],
                    one=True,
                )

                if existing:
                    print(f"[import_customers] Row {idx}: Code {code} already exists, skipping")
                    skipped_count += 1
                    continue

                # Insert customer
                customer_id = str(uuid.uuid4())
                execute(
                    """INSERT INTO sale_customers
                       (id, customer_code, customer_name, industry, region, country,
                        address, payment_terms, status, email_domain, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    [
                        customer_id,
                        code,
                        name,
                        record.get("industry", "").strip(),
                        record.get("region", "").strip(),
                        record.get("country", "").strip(),
                        record.get("address", "").strip(),
                        record.get("payment_terms", "").strip(),
                        record.get("status", "ACTIVE").strip(),
                        _extract_domain(record.get("contact_email", "")),
                        datetime.utcnow().isoformat(),
                    ],
                )

                # Insert contact if present
                contact_name = record.get("contact_name", "").strip()
                contact_email = record.get("contact_email", "").strip()

                if contact_name or contact_email:
                    contact_id = str(uuid.uuid4())
                    execute(
                        """INSERT INTO sale_customer_contacts
                           (id, customer_id, contact_name, contact_title, contact_email,
                            contact_phone, is_primary, created_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        [
                            contact_id,
                            customer_id,
                            contact_name,
                            record.get("contact_title", "").strip(),
                            contact_email,
                            record.get("contact_phone", "").strip(),
                            True,
                            datetime.utcnow().isoformat(),
                        ],
                    )

                imported_count += 1
                if imported_count % 100 == 0:
                    print(f"[import_customers] Imported {imported_count}...")

            except Exception as e:
                print(f"[import_customers] Row {idx} error: {e}")
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
                    "CUSTOMERS",
                    source_file,
                    imported_count,
                    skipped_count,
                    error_count,
                    json.dumps({"total_rows": len(data_rows)}),
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
            "success": error_count == 0,
        }

        print(
            f"[import_customers] Complete: {imported_count} imported, "
            f"{skipped_count} skipped, {error_count} errors"
        )

        return report

    except Exception as e:
        return {"error": str(e)}


def _extract_domain(email: str) -> Optional[str]:
    """Extract domain from email address.

    Args:
        email: Email address.

    Returns:
        Domain (e.g., 'acme.com') or None.
    """
    if not email or "@" not in email:
        return None
    return email.split("@")[1].lower().strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_customers.py <file.xlsx|file.csv>")
        sys.exit(1)

    result = import_customers_from_file(sys.argv[1])

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    print(f"\nImport Summary:")
    print(f"  Imported: {result.get('imported_count', 0)}")
    print(f"  Skipped: {result.get('skipped_count', 0)}")
    print(f"  Errors: {result.get('error_count', 0)}")
    print(f"  Total: {result.get('total_rows', 0)}")
