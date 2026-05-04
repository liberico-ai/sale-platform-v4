"""Database module for IBS HI Sale Platform.

Supports both SQLite and PostgreSQL with thread-local connections.
Auto-initializes schema on first run (SQLite only).
"""

import asyncio
import os
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, List, Dict, Optional
from contextlib import contextmanager

import structlog

logger = structlog.get_logger(__name__)

# Support both module and direct execution
try:
    from . import config
except ImportError:
    import config

# Thread-local storage for database connections
_thread_local = threading.local()

# PostgreSQL connection pool (initialized lazily)
_pg_pool = None

# Schema file paths (relative to project root)
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
_SQLITE_SCHEMA = os.path.join(_PROJECT_ROOT, "sql_import", "schema_all.sql")
_PG_SCHEMA = os.path.join(_PROJECT_ROOT, "schema_pg.sql")
_SEED_SQL_DIR = os.path.join(_PROJECT_ROOT, "sql_import")

# Seed data import order — mirrors sql_import/build_db.py IMPORT_FILES,
# excluding schema_all.sql (run separately) and 99_import_log.sql.
_SEED_DATA_FILES = [
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


def _get_pg_pool():
    """Get or create PostgreSQL connection pool (lazy init).

    Uses ``ThreadedConnectionPool`` so getconn/putconn are safe to call
    from FastAPI's threadpool workers and APScheduler background jobs
    concurrently. ``SimpleConnectionPool`` (single-thread only) raises
    ``PoolError`` under concurrent access — see psycopg2 docs.
    """
    global _pg_pool
    if _pg_pool is None:
        from psycopg2 import pool as pg_pool
        _pg_pool = pg_pool.ThreadedConnectionPool(
            minconn=2,
            maxconn=int(os.getenv("PG_POOL_MAX", "10")),
            dsn=config.PG_DSN,
        )
        logger.info("pg_pool_created",
                     min=2,
                     max=int(os.getenv("PG_POOL_MAX", "10")),
                     pool_type="ThreadedConnectionPool")
    return _pg_pool


def get_db_connection():
    """Get or create a database connection for the current thread.

    For PostgreSQL: uses connection pool.
    For SQLite: uses thread-local connections with WAL mode.
    """
    if not hasattr(_thread_local, 'connection') or _thread_local.connection is None:
        if config.DB_TYPE == "postgresql":
            pool = _get_pg_pool()
            _thread_local.connection = pool.getconn()
            logger.debug("pg_connection_acquired",
                         thread=threading.current_thread().name)
        else:  # sqlite
            _thread_local.connection = sqlite3.connect(config.SALE_DB_PATH)
            _thread_local.connection.execute("PRAGMA foreign_keys = ON")
            _thread_local.connection.execute("PRAGMA journal_mode = WAL")
            _thread_local.connection.row_factory = sqlite3.Row
            logger.debug("sqlite_connection_created",
                         path=config.SALE_DB_PATH,
                         thread=threading.current_thread().name)
    return _thread_local.connection


def close_db_connection():
    """Close or return the database connection for the current thread.

    For PostgreSQL: returns connection to pool.
    For SQLite: closes the connection.
    """
    if hasattr(_thread_local, 'connection') and _thread_local.connection is not None:
        if config.DB_TYPE == "postgresql" and _pg_pool:
            _pg_pool.putconn(_thread_local.connection)
            logger.debug("pg_connection_returned",
                         thread=threading.current_thread().name)
        else:
            _thread_local.connection.close()
            logger.debug("sqlite_connection_closed",
                         thread=threading.current_thread().name)
        _thread_local.connection = None


def close_all_connections():
    """Close all connections and shut down pool. Called on app shutdown."""
    global _pg_pool
    close_db_connection()
    if _pg_pool:
        _pg_pool.closeall()
        _pg_pool = None
        logger.info("pg_pool_closed")
    # Drain the async-wrapper executor so the process can exit cleanly.
    try:
        _db_executor.shutdown(wait=False)
    except Exception:
        pass



@contextmanager
def get_cursor():
    """Context manager for database cursor."""
    conn = get_db_connection()
    if config.DB_TYPE == "postgresql":
        from psycopg2.extras import RealDictCursor
        cursor = conn.cursor(cursor_factory=RealDictCursor)
    else:  # sqlite
        cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def _convert_placeholders(sql: str, db_type: str) -> str:
    """Convert ? placeholders to %s for PostgreSQL."""
    if db_type == "postgresql":
        sql = sql.replace("?", "%s")
    return sql


# ═══════════════════════════════════════════════════════════════
# Dialect helpers — dates / now / today (UNIFIED step 7)
# ═══════════════════════════════════════════════════════════════
# Workers and routers should call these instead of hardcoding
# ``datetime('now')`` (SQLite) or ``NOW()`` (PostgreSQL). The helpers
# read ``config.DB_TYPE`` at call time so a single codebase runs on
# both engines.


def now_expr() -> str:
    """SQL expression for the current timestamp.

    Use in SQL strings: ``UPDATE foo SET updated_at = {now_expr()}``.
    """
    return "NOW()" if config.DB_TYPE == "postgresql" else "datetime('now')"


def date_today_expr() -> str:
    """SQL expression for today's date (no time component)."""
    return "CURRENT_DATE" if config.DB_TYPE == "postgresql" else "date('now')"


def date_diff_expr(column: str, days: int) -> str:
    """SQL boolean expression: ``column`` is older than ``days`` days.

    Returns a complete predicate that goes inside a WHERE clause:
        ``WHERE {date_diff_expr('last_activity_date', 30)}``
    """
    if config.DB_TYPE == "postgresql":
        return f"{column} < NOW() - INTERVAL '{int(days)} days'"
    return f"{column} < datetime('now', '-{int(days)} days')"


def query(
    sql: str,
    params: List[Any] = None,
    one: bool = False
) -> Any:
    """Execute a SELECT query and return results.

    Args:
        sql: SQL query string (use ? for placeholders).
        params: Query parameters.
        one: If True, return single row; if False, return list of rows.

    Returns:
        Single row dict (if one=True), list of row dicts, or None.
    """
    if params is None:
        params = []

    sql = _convert_placeholders(sql, config.DB_TYPE)

    with get_cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]

        if one:
            return result[0] if result else None
        return result


def execute(sql: str, params: List[Any] = None) -> int:
    """Execute an INSERT, UPDATE, or DELETE query.

    Args:
        sql: SQL query string (use ? for placeholders).
        params: Query parameters.

    Returns:
        Number of affected rows.
    """
    if params is None:
        params = []

    sql = _convert_placeholders(sql, config.DB_TYPE)

    conn = get_db_connection()
    with get_cursor() as cursor:
        cursor.execute(sql, params)
        conn.commit()
        return cursor.rowcount


# ═══════════════════════════════════════════════════════════════
# Async wrappers (UNIFIED step 8)
# ═══════════════════════════════════════════════════════════════
# The sync ``query``/``execute`` functions block the event loop. Routers
# under heavy concurrent load should call the async variants which run
# on a dedicated thread pool. New code prefers these; existing routers
# stay sync and keep working unchanged.

_db_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="db")


async def async_query(
    sql: str,
    params: List[Any] = None,
    one: bool = False,
) -> Any:
    """Async-friendly wrapper around :func:`query`. Runs on a worker thread."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_db_executor, _run_query, sql, params, one)


async def async_execute(sql: str, params: List[Any] = None) -> int:
    """Async-friendly wrapper around :func:`execute`."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_db_executor, _run_execute, sql, params)


def _run_query(sql, params, one):
    return query(sql, params, one)


def _run_execute(sql, params):
    return execute(sql, params)


def execute_many(sql: str, params_list: List[List[Any]]) -> int:
    """Execute multiple INSERT, UPDATE, or DELETE queries.

    Args:
        sql: SQL query string (use ? for placeholders).
        params_list: List of parameter lists.

    Returns:
        Total number of affected rows.
    """
    sql = _convert_placeholders(sql, config.DB_TYPE)

    conn = get_db_connection()
    with get_cursor() as cursor:
        total_rows = 0
        for params in params_list:
            cursor.execute(sql, params)
            total_rows += cursor.rowcount
        conn.commit()
        return total_rows


def _create_audit_table_sqlite(conn):
    """Create audit_log table for SQLite (not in original schema)."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sale_audit_log (
            id              TEXT PRIMARY KEY,
            entity_type     TEXT NOT NULL,
            entity_id       TEXT NOT NULL,
            action          TEXT NOT NULL,
            field_name      TEXT,
            old_value       TEXT,
            new_value       TEXT,
            changed_by      TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_sal_entity
            ON sale_audit_log(entity_type, entity_id);
        CREATE INDEX IF NOT EXISTS idx_sal_created
            ON sale_audit_log(created_at);
    """)


def _create_audit_table_pg(cursor):
    """Create audit_log table for PostgreSQL."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale.audit_log (
            id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            entity_type     TEXT NOT NULL,
            entity_id       UUID NOT NULL,
            action          TEXT NOT NULL,
            field_name      TEXT,
            old_value       TEXT,
            new_value       TEXT,
            changed_by      TEXT,
            created_at      TIMESTAMPTZ DEFAULT now()
        );
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sal_entity
            ON sale.audit_log(entity_type, entity_id);
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sal_created
            ON sale.audit_log(created_at);
    """)


def _load_seed_data_sqlite(conn) -> None:
    """Wipe sale_* tables, then run sql_import/*.sql to populate the DB.

    Only invoked from init_db() after the gate check confirms the DB is
    under-populated. Wiping first guarantees a clean slate so re-runs don't
    fail on UNIQUE-constraint conflicts with stale rows (e.g. a partially
    seeded DB from an earlier broken deploy).

    FK enforcement is disabled during the wipe + load (mirrors
    sql_import/build_db.py) because the bulk-insert files don't strictly
    maintain insertion order across FK boundaries.

    Errors are logged per-file and do not abort the rest.
    """
    # Toggling foreign_keys requires no open transaction
    conn.commit()
    conn.execute("PRAGMA foreign_keys = OFF")
    cleared = 0
    loaded = 0
    failed = []
    try:
        # Wipe all sale_* tables (including audit_log — fresh seed = fresh audit)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'sale_%'"
        )
        tables = [r[0] for r in cursor.fetchall()]
        cursor.close()
        for t in tables:
            try:
                conn.execute(f"DELETE FROM {t}")
                cleared += 1
            except Exception as e:
                logger.warning("seed_table_clear_failed",
                               table=t, error=str(e)[:200])
        conn.commit()
        logger.info("seed_tables_cleared", count=cleared, total=len(tables))

        # Load seed files in order
        for fname in _SEED_DATA_FILES:
            fpath = os.path.join(_SEED_SQL_DIR, fname)
            if not os.path.exists(fpath):
                logger.warning("seed_file_missing", file=fname)
                continue
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    sql = "".join(
                        line for line in f if not line.lstrip().startswith(".")
                    )
                conn.executescript(sql)
                loaded += 1
            except Exception as e:
                failed.append((fname, str(e)[:200]))
                logger.error("seed_file_failed", file=fname, error=str(e)[:200])
        conn.commit()
    finally:
        conn.execute("PRAGMA foreign_keys = ON")
    logger.info(
        "seed_data_load_complete",
        files_loaded=loaded,
        files_failed=len(failed),
    )


def init_db() -> bool:
    """Initialize database: apply schema, optionally load seed data.

    For SQLite:
      - Always runs schema_all.sql (CREATE TABLE IF NOT EXISTS is idempotent),
        so new tables added to the schema appear in existing DBs on restart.
      - If AUTO_LOAD_SEED_DATA=true and sale_opportunities is empty, runs the
        sql_import/*.sql data pipeline once.
    For PostgreSQL: Verifies connectivity (schema must be created manually).

    Returns:
        True if database is ready, False if initialization failed.
    """
    try:
        conn = get_db_connection()

        if config.DB_TYPE == "sqlite":
            # Always apply schema. CREATE TABLE/INDEX/VIEW use IF NOT EXISTS
            # so they're idempotent. ALTER TABLE ADD COLUMN doesn't support
            # IF NOT EXISTS in older SQLite — on re-run it raises 'duplicate
            # column name'. We split the schema into individual statements
            # using sqlite3.complete_statement (handles strings, comments,
            # multi-line SQL correctly) so we can swallow that one benign
            # error per-ALTER without aborting the rest.
            if os.path.exists(_SQLITE_SCHEMA):
                with open(_SQLITE_SCHEMA, "r") as f:
                    schema_sql = f.read()
                statements = []
                buf = ""
                for line in schema_sql.splitlines():
                    buf += line + "\n"
                    if sqlite3.complete_statement(buf):
                        stmt = buf.strip()
                        if stmt:
                            statements.append(stmt)
                        buf = ""
                if buf.strip():
                    statements.append(buf.strip())
                applied = 0
                skipped = 0
                for stmt in statements:
                    try:
                        conn.execute(stmt)
                        applied += 1
                    except sqlite3.OperationalError as e:
                        if "duplicate column name" in str(e).lower():
                            skipped += 1
                            continue
                        raise
                conn.commit()
                logger.info("sqlite_schema_applied",
                            schema_file=_SQLITE_SCHEMA,
                            applied=applied, skipped=skipped)
            else:
                logger.warning("sqlite_schema_missing",
                               expected_path=_SQLITE_SCHEMA)

            # Always ensure audit_log table exists
            _create_audit_table_sqlite(conn)
            conn.commit()

            # Auto-load seed data if enabled AND the DB is under-populated.
            # Two-marker gate (customers AND opportunities) so it passes for
            # fresh/broken deploys but fails for any meaningfully populated DB.
            if config.AUTO_LOAD_SEED_DATA:
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT COUNT(*) FROM sale_customers")
                    customer_count = cursor.fetchone()[0]
                    cursor.execute("SELECT COUNT(*) FROM sale_opportunities")
                    opp_count = cursor.fetchone()[0]
                finally:
                    cursor.close()
                needs_seed = customer_count < 50 and opp_count < 10
                if needs_seed:
                    logger.info("seed_data_loading",
                                reason="db_under_populated",
                                customers=customer_count,
                                opportunities=opp_count)
                    _load_seed_data_sqlite(conn)
                else:
                    logger.info("seed_data_skipped",
                                reason="db_populated",
                                customers=customer_count,
                                opportunities=opp_count)

        else:  # postgresql
            with get_cursor() as cursor:
                cursor.execute("SELECT 1")
                # Ensure audit_log table exists
                _create_audit_table_pg(cursor)
                conn.commit()

        logger.info("database_ready", db_type=config.DB_TYPE)
        return True

    except Exception as e:
        logger.error("database_init_failed", error=str(e), db_type=config.DB_TYPE)
        return False
