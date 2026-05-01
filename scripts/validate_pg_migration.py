"""Validate PostgreSQL migration for IBS HI Sale Platform.

Connects to PostgreSQL and verifies:
- All 16 tables exist in schema 'sale'
- At least 20 indexes exist
- Seed data loaded (7 categories, 6 templates, 2 mailboxes, 5 users, >=1 KHKD target)
- Query compatibility with router patterns
- UUID generation via gen_random_uuid()

Usage:
    python scripts/validate_pg_migration.py [--dsn <PG_DSN>]

Environment:
    PG_DSN: PostgreSQL connection string (default: from config.py)

Exit codes:
    0: All validations passed
    1: One or more validations failed or connection error
"""

import sys
import argparse
from typing import List, Tuple

import structlog

logger = structlog.get_logger(__name__)

# All 16 tables expected in the 'sale' schema (from schema_pg.sql)
EXPECTED_TABLES = [
    "customers",
    "customer_contacts",
    "product_categories",
    "opportunities",
    "emails",
    "tasks",
    "follow_up_schedules",
    "email_templates",
    "email_activity_log",
    "khkd_targets",
    "nas_file_links",
    "monitored_mailboxes",
    "user_roles",
    "pm_sync_log",
    "import_log",
    "audit_log",
]

MIN_INDEX_COUNT = 20

# Seed data expectations
SEED_EXPECTATIONS = {
    "product_categories": 7,
    "email_templates": 6,
    "monitored_mailboxes": 2,
    "user_roles": 5,
}

# Sample queries that mirror what routers actually use
COMPATIBILITY_QUERIES = [
    (
        "opportunities by stage",
        "SELECT id, project_name, stage, customer_name FROM sale.opportunities WHERE stage = 'PROSPECT' LIMIT 1",
    ),
    (
        "tasks by status with join",
        "SELECT t.id, t.title, t.status, t.to_dept FROM sale.tasks t LEFT JOIN sale.opportunities o ON t.opportunity_id = o.id WHERE t.status = 'PENDING' LIMIT 1",
    ),
    (
        "emails by type with date filter",
        "SELECT id, subject, email_type, received_at FROM sale.emails WHERE email_type = 'RFQ' AND received_at IS NOT NULL LIMIT 1",
    ),
    (
        "dashboard aggregate",
        "SELECT stage, COUNT(*) as cnt FROM sale.opportunities GROUP BY stage",
    ),
    (
        "customer search",
        "SELECT id, code, name, region FROM sale.customers WHERE name ILIKE '%test%' OR code ILIKE '%test%' LIMIT 1",
    ),
    (
        "audit log query",
        "SELECT id, entity_type, entity_id, action, created_at FROM sale.audit_log ORDER BY created_at DESC LIMIT 1",
    ),
    (
        "JSONB field access",
        "SELECT id, milestones FROM sale.opportunities WHERE milestones IS NOT NULL LIMIT 1",
    ),
    (
        "pm_sync_log filter",
        "SELECT id, direction, sync_type, status FROM sale.pm_sync_log WHERE direction = 'SALE_TO_PM' LIMIT 1",
    ),
]


def get_pg_dsn(cli_dsn: str = None) -> str:
    """Resolve PG_DSN from CLI arg, env var, or config.py."""
    import os

    if cli_dsn:
        return cli_dsn

    env_dsn = os.getenv("PG_DSN")
    if env_dsn:
        return env_dsn

    try:
        # Add parent directory to path so we can import config
        parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent not in sys.path:
            sys.path.insert(0, parent)
        from config import PG_DSN
        return PG_DSN
    except ImportError:
        return "postgresql://user:password@localhost:5432/ibs_hi_sale"


def connect(dsn: str):
    """Connect to PostgreSQL via psycopg2.

    Args:
        dsn: PostgreSQL connection string.

    Returns:
        psycopg2 connection object.

    Raises:
        SystemExit: If connection fails.
    """
    try:
        import psycopg2
    except ImportError:
        print("\n\u2717 psycopg2 not installed. Install with: pip install psycopg2-binary")
        logger.error("psycopg2 not installed")
        sys.exit(1)

    try:
        conn = psycopg2.connect(dsn)
        conn.autocommit = True
        logger.info("pg_connected", dsn=dsn.split("@")[-1])
        return conn
    except Exception as e:
        print(f"\n\u2717 Cannot connect to PostgreSQL: {e}")
        logger.error("pg_connection_failed", error=str(e))
        sys.exit(1)


def validate_tables(cur) -> Tuple[bool, str]:
    """Check all 16 tables exist in sale schema."""
    cur.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'sale' AND table_type = 'BASE TABLE'"
    )
    existing = {row[0] for row in cur.fetchall()}
    missing = [t for t in EXPECTED_TABLES if t not in existing]

    if missing:
        return False, f"Missing tables: {', '.join(missing)}"
    return True, f"All {len(EXPECTED_TABLES)} tables present"


def validate_indexes(cur) -> Tuple[bool, str]:
    """Check at least 20 indexes exist in sale schema."""
    cur.execute(
        "SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'sale'"
    )
    count = cur.fetchone()[0]

    if count < MIN_INDEX_COUNT:
        return False, f"Only {count} indexes found (need >= {MIN_INDEX_COUNT})"
    return True, f"{count} indexes created"


def validate_seed_data(cur) -> Tuple[bool, str]:
    """Check seed data counts match expectations."""
    failures: List[str] = []
    counts = {}

    for table, expected in SEED_EXPECTATIONS.items():
        cur.execute(f"SELECT COUNT(*) FROM sale.{table}")
        actual = cur.fetchone()[0]
        counts[table] = actual
        if actual < expected:
            failures.append(f"{table}: {actual} (need >= {expected})")

    # KHKD targets: at least 1
    cur.execute("SELECT COUNT(*) FROM sale.khkd_targets")
    khkd_count = cur.fetchone()[0]
    counts["khkd_targets"] = khkd_count
    if khkd_count < 1:
        failures.append(f"khkd_targets: {khkd_count} (need >= 1)")

    if failures:
        return False, f"Seed data mismatch: {'; '.join(failures)}"

    summary = (
        f"{counts['product_categories']} categories, "
        f"{counts['email_templates']} templates, "
        f"{counts['monitored_mailboxes']} mailboxes, "
        f"{counts['user_roles']} users"
    )
    return True, f"Seed data loaded ({summary})"


def validate_query_compatibility(cur) -> Tuple[bool, str]:
    """Run sample SELECT queries that routers use."""
    failures: List[str] = []

    for name, sql in COMPATIBILITY_QUERIES:
        try:
            cur.execute(sql)
            # Success if query runs without error, even with 0 rows
            cur.fetchall()
        except Exception as e:
            failures.append(f"{name}: {e}")

    if failures:
        return False, f"Query failures: {'; '.join(failures)}"
    return True, "Query compatibility OK"


def validate_uuid_generation(cur) -> Tuple[bool, str]:
    """Check gen_random_uuid() works."""
    try:
        cur.execute("SELECT gen_random_uuid()::text")
        result = cur.fetchone()[0]
        if result and len(result) == 36 and result.count("-") == 4:
            return True, "UUID generation works"
        return False, f"Unexpected UUID format: {result}"
    except Exception as e:
        return False, f"UUID generation failed: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Validate PostgreSQL migration for IBS HI Sale Platform"
    )
    parser.add_argument(
        "--dsn",
        type=str,
        default=None,
        help="PostgreSQL DSN (overrides PG_DSN env var and config.py)",
    )
    args = parser.parse_args()

    dsn = get_pg_dsn(args.dsn)
    print(f"Connecting to PostgreSQL ({dsn.split('@')[-1]})...")

    conn = connect(dsn)
    cur = conn.cursor()

    # Set search path
    cur.execute("SET search_path TO sale, public")

    validators = [
        ("Tables", validate_tables),
        ("Indexes", validate_indexes),
        ("Seed Data", validate_seed_data),
        ("Query Compatibility", validate_query_compatibility),
        ("UUID Generation", validate_uuid_generation),
    ]

    all_passed = True
    print()

    for label, func in validators:
        try:
            passed, detail = func(cur)
        except Exception as e:
            passed = False
            detail = f"Unexpected error: {e}"

        if passed:
            print(f"\u2713 {detail}")
            logger.info("validation_passed", check=label, detail=detail)
        else:
            print(f"\u2717 {detail}")
            logger.error("validation_failed", check=label, detail=detail)
            all_passed = False

    print()
    if all_passed:
        print("MIGRATION VALIDATION: PASSED")
        logger.info("migration_validation_complete", result="PASSED")
    else:
        print("MIGRATION VALIDATION: FAILED")
        logger.error("migration_validation_complete", result="FAILED")

    cur.close()
    conn.close()

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
