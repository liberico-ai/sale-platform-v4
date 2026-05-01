#!/usr/bin/env python3
"""
IBS HI Sale Platform — Database Builder
========================================
Rebuilds sale.db from the sql_import/ pipeline.
No sqlite3 CLI required — uses Python's built-in sqlite3 module.

Usage:
    python build_db.py                  # Build ../sale.db (default)
    python build_db.py --output sale.db # Build to custom path
    python build_db.py --validate-only  # Check SQL syntax without building
    python build_db.py --no-counts      # Skip record count output

Generated: 2026-04-30
"""

import sqlite3
import os
import sys
import time
from pathlib import Path

# ── Import file order (matches master_import.sql) ──────────────────────
IMPORT_FILES = [
    "schema_all.sql",
    "01_customers.sql",
    "02_opportunities.sql",
    "02b_active_contracts.sql",
    "03_contract_milestones.sql",
    "04_settlements.sql",
    "05_vogt_pipeline.sql",
    "06_nas_file_links.sql",
    "07_quotation_revisions.sql",
    "08_contract_files.sql",
    "09_digital_content.sql",
    "10_product_opportunities.sql",
    "11_emails.sql",
    "12_customer_interactions.sql",
    "13_market_signals.sql",
    "14_mbox_customers.sql",
    "15_customer_contacts.sql",
    "16_email_stats.sql",
    "17_quotation_enrichment.sql",
    "18_qr_customers.sql",
    "19_won_contracts.sql",
    "20_email_2026_quotations.sql",
    "21_email_active_contracts.sql",
    "22_email_customer_labels.sql",
    "23_full_email_mapping.sql",
    "24_client_database.sql",
    "25_client_visits.sql",
    "99_import_log.sql",
]

COUNT_TABLES = [
    "sale_customers",
    "sale_customer_contacts",
    "sale_opportunities",
    "sale_contract_milestones",
    "sale_settlements",
    "sale_nas_file_links",
    "sale_quotation_revisions",
    "sale_digital_content",
    "sale_emails",
    "sale_customer_interactions",
    "sale_market_signals",
    "sale_product_opportunities",
    "sale_import_log",
    "sale_quotation_history",
    "sale_active_contracts",
    "sale_email_labels",
    "sale_email_full",
]

INTEGRITY_CHECKS = [
    ("Orphan opportunities", "SELECT COUNT(*) FROM sale_opportunities WHERE customer_id IS NOT NULL AND customer_id NOT IN (SELECT id FROM sale_customers)"),
    ("Orphan emails", "SELECT COUNT(*) FROM sale_emails WHERE customer_id IS NOT NULL AND customer_id NOT IN (SELECT id FROM sale_customers)"),
    ("Orphan interactions", "SELECT COUNT(*) FROM sale_customer_interactions WHERE customer_id NOT IN (SELECT id FROM sale_customers)"),
    ("Orphan contacts", "SELECT COUNT(*) FROM sale_customer_contacts WHERE customer_id NOT IN (SELECT id FROM sale_customers)"),
]


def load_sql(filepath: Path) -> str:
    """Load SQL file, stripping sqlite3 CLI dot-commands."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return ''.join(l for l in lines if not l.lstrip().startswith('.'))


def validate_only(sql_dir: Path) -> bool:
    """Check that all SQL files exist and parse without errors."""
    print("=== VALIDATE SQL FILES ===")
    all_ok = True
    conn = sqlite3.connect(":memory:")
    for fname in IMPORT_FILES:
        fpath = sql_dir / fname
        if not fpath.exists():
            print(f"  MISSING: {fname}")
            all_ok = False
            continue
        try:
            sql = load_sql(fpath)
            conn.executescript(sql)
            size_kb = fpath.stat().st_size / 1024
            print(f"  OK: {fname} ({size_kb:.0f} KB)")
        except Exception as e:
            print(f"  ERROR: {fname} — {e}")
            all_ok = False
    conn.close()
    print(f"\n{'ALL FILES VALID' if all_ok else 'ERRORS FOUND'}")
    return all_ok


def build_db(sql_dir: Path, db_path: Path, show_counts: bool = True) -> bool:
    """Build sale.db from the sql_import pipeline."""
    print("=== BUILDING DATABASE ===")
    print(f"  Source: {sql_dir}/")
    print(f"  Target: {db_path}")

    if db_path.exists():
        db_path.unlink()
        print(f"  Removed existing {db_path.name}")

    start = time.time()
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=OFF")
    conn.execute("PRAGMA foreign_keys=OFF")

    errors = []
    for fname in IMPORT_FILES:
        fpath = sql_dir / fname
        if not fpath.exists():
            print(f"    SKIP: {fname} (missing)")
            continue
        try:
            sql = load_sql(fpath)
            conn.executescript(sql)
            size_kb = fpath.stat().st_size / 1024
            print(f"    OK: {fname} ({size_kb:.0f} KB)")
        except Exception as e:
            msg = str(e)[:150]
            print(f"    ERR: {fname} — {msg}")
            errors.append((fname, msg))

    elapsed = time.time() - start
    db_size = db_path.stat().st_size / (1024 * 1024)
    print(f"\n  Built in {elapsed:.1f}s — {db_size:.1f} MB")

    if errors:
        print(f"\n  WARNINGS ({len(errors)}):")
        for f, e in errors:
            print(f"    {f}: {e}")

    if show_counts:
        print("\n=== RECORD COUNTS ===")
        total = 0
        for table in COUNT_TABLES:
            try:
                c = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                total += c
                print(f"  {table}: {c:,}")
            except:
                print(f"  {table}: (missing)")
        print(f"  --- TOTAL: {total:,} records ---")

        print("\n=== INTEGRITY CHECKS ===")
        clean = True
        for label, query in INTEGRITY_CHECKS:
            try:
                c = conn.execute(query).fetchone()[0]
                s = "OK" if c == 0 else f"WARN: {c}"
                if c > 0: clean = False
                print(f"  {label}: {s}")
            except Exception as e:
                print(f"  {label}: ERROR — {e}")
        if clean:
            print("  All checks passed.")

    conn.execute("PRAGMA synchronous=NORMAL")
    conn.close()

    print(f"\n{'=' * 50}")
    print(f"  sale.db ready: {db_path}")
    print(f"{'=' * 50}")
    return len(errors) == 0


def main():
    sql_dir = Path(__file__).parent
    default_db = sql_dir.parent / "sale.db"

    args = sys.argv[1:]
    output = default_db
    validate = False
    counts = True

    i = 0
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output = Path(args[i + 1])
            i += 2
        elif args[i] == "--validate-only":
            validate = True
            i += 1
        elif args[i] == "--no-counts":
            counts = False
            i += 1
        elif args[i] in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        else:
            print(f"Unknown arg: {args[i]}")
            sys.exit(1)

    if validate:
        sys.exit(0 if validate_only(sql_dir) else 1)

    sys.exit(0 if build_db(sql_dir, output, counts) else 1)


if __name__ == "__main__":
    main()
