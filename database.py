"""Database module for IBS HI Sale Platform.

Supports both SQLite and PostgreSQL with thread-local connections.
Auto-initializes schema on first run (SQLite only).
"""

import os
import sqlite3
import threading
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


def _get_pg_pool():
    """Get or create PostgreSQL connection pool (lazy init)."""
    global _pg_pool
    if _pg_pool is None:
        from psycopg2 import pool as pg_pool
        _pg_pool = pg_pool.SimpleConnectionPool(
            minconn=2,
            maxconn=int(os.getenv("PG_POOL_MAX", "10")),
            dsn=config.PG_DSN,
        )
        logger.info("pg_pool_created",
                     min=2,
                     max=int(os.getenv("PG_POOL_MAX", "10")))
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


def init_db() -> bool:
    """Initialize database: connect, verify, and auto-create schema if needed.

    For SQLite: Runs schema.sql if database file is empty/new.
    For PostgreSQL: Verifies connectivity (schema must be created manually).

    Returns:
        True if database is ready, False if initialization failed.
    """
    try:
        conn = get_db_connection()

        if config.DB_TYPE == "sqlite":
            # Check if tables exist
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='sale_customers'"
            )
            tables_exist = cursor.fetchone() is not None
            cursor.close()

            if not tables_exist:
                # Auto-create schema from schema.sql
                if os.path.exists(_SQLITE_SCHEMA):
                    with open(_SQLITE_SCHEMA, "r") as f:
                        schema_sql = f.read()
                    conn.executescript(schema_sql)
                    conn.commit()
                    logger.info("sqlite_schema_created", schema_file=_SQLITE_SCHEMA)
                else:
                    logger.warning("sqlite_schema_missing",
                                   expected_path=_SQLITE_SCHEMA)

            # Always ensure audit_log table exists
            _create_audit_table_sqlite(conn)
            conn.commit()

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
