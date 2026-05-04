"""
Configuration module for IBS HI Sale Platform.
Handles environment variables, API keys, and database configuration.
"""

import os
from typing import Dict, Optional

# Server Configuration
SALE_PORT = int(os.getenv("SALE_PORT", "8767"))
API_HOST = os.getenv("API_HOST", "0.0.0.0")

# Database Configuration
DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # sqlite or postgresql
# Built by sql_import/build_db.py — lives at project root
SALE_DB_PATH = os.getenv("SALE_DB_PATH", "./sale.db")
# Pipeline directory for sql_import/build_db.py (32 tables, ~6,700 records)
IMPORT_DIR = os.getenv("IMPORT_DIR", "./sql_import/")

# PostgreSQL Configuration (if DB_TYPE == "postgresql")
PG_DSN = os.getenv(
    "PG_DSN",
    "postgresql://user:password@localhost:5432/ibs_hi_sale"
)

# API Keys Configuration (3-tier system)
# IMPORTANT: Set via environment variables. Do NOT use defaults in production.
#
# Two ways to configure keys:
# 1. Numbered slots (legacy): {TIER}_API_KEY_1, {TIER}_API_KEY_2
# 2. Bulk list (recommended for many testers):
#    {TIER}_API_KEYS_LIST="key1:Alice,key2:Bob,key3:Charlie"
#    Each entry is "uuid:label". Labels surface in /auth/me + audit log.
#
# Both can coexist — numbered slots get a generic label, list entries
# get the explicit label.

_admin_key_1 = os.getenv("ADMIN_API_KEY_1", "")
_admin_key_2 = os.getenv("ADMIN_API_KEY_2", "")
_manager_key_1 = os.getenv("MANAGER_API_KEY_1", "")
_manager_key_2 = os.getenv("MANAGER_API_KEY_2", "")
_viewer_key_1 = os.getenv("VIEWER_API_KEY_1", "")
_viewer_key_2 = os.getenv("VIEWER_API_KEY_2", "")

API_KEYS: Dict[str, str] = {}
API_KEY_LABELS: Dict[str, str] = {}


def _add_key(key: str, tier: str, label: str = "") -> None:
    """Register one key in both API_KEYS (key→tier) and API_KEY_LABELS (key→label)."""
    if not key:
        return
    API_KEYS[key] = tier
    API_KEY_LABELS[key] = label or f"{tier} (slot)"


def _parse_keys_list(env_value: str, tier: str) -> None:
    """Parse '{TIER}_API_KEYS_LIST' env value: comma-separated 'key:label' entries.

    A bare 'key' (no colon) gets the default '<tier> (unlabeled)' label.
    Whitespace around tokens is stripped.
    """
    if not env_value:
        return
    for entry in env_value.split(","):
        entry = entry.strip()
        if not entry:
            continue
        if ":" in entry:
            key, _, label = entry.partition(":")
            _add_key(key.strip(), tier, label.strip())
        else:
            _add_key(entry, tier, f"{tier} (unlabeled)")


# Numbered slots
_add_key(_admin_key_1, "ADMIN", "ADMIN slot 1")
_add_key(_admin_key_2, "ADMIN", "ADMIN slot 2")
_add_key(_manager_key_1, "MANAGER", "MANAGER slot 1")
_add_key(_manager_key_2, "MANAGER", "MANAGER slot 2")
_add_key(_viewer_key_1, "VIEWER", "VIEWER slot 1")
_add_key(_viewer_key_2, "VIEWER", "VIEWER slot 2")

# Bulk lists (recommended for testers)
_parse_keys_list(os.getenv("ADMIN_API_KEYS_LIST", ""), "ADMIN")
_parse_keys_list(os.getenv("MANAGER_API_KEYS_LIST", ""), "MANAGER")
_parse_keys_list(os.getenv("VIEWER_API_KEYS_LIST", ""), "VIEWER")

# Dev mode: if no keys configured, allow a dev key
SALE_ENV = os.getenv("SALE_ENV", "development")
IS_DEV_ENV = SALE_ENV == "development"
if not API_KEYS and IS_DEV_ENV:
    _add_key("dev-key-local-only", "ADMIN", "Dev fallback (local only)")

# IBS HI Layer 1 Integration
IBSHI1_URL = os.getenv("IBSHI1_URL", "http://localhost:3000")
IBSHI1_TOKEN = os.getenv("IBSHI1_TOKEN", "")

# Gmail Integration
GMAIL_CREDENTIALS_PATH = os.getenv(
    "GMAIL_CREDENTIALS_PATH",
    "./credentials/gmail_credentials.json"
)
GMAIL_TOKENS_DIR = os.getenv(
    "GMAIL_TOKENS_DIR",
    "./tokens/"
)

# Feature Flags
ENABLE_EMAIL_SYNC = os.getenv("ENABLE_EMAIL_SYNC", "true").lower() == "true"
ENABLE_PM_INTEGRATION = os.getenv("ENABLE_PM_INTEGRATION", "true").lower() == "true"
ENABLE_TASK_SCHEDULING = os.getenv("ENABLE_TASK_SCHEDULING", "true").lower() == "true"

# Auto-load seed data on startup if the DB is under-populated (sqlite only).
# Runs the sql_import/*.sql pipeline when fewer than 50 customers AND fewer
# than 10 opportunities exist. Tables are cleared first so re-runs don't
# collide on UNIQUE constraints. Set to "false" to disable on environments
# that manage their own data.
AUTO_LOAD_SEED_DATA = os.getenv("AUTO_LOAD_SEED_DATA", "true").lower() == "true"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Departments Enum
DEPARTMENTS = [
    "SALE",    # Sales team
    "KTKH",    # Technical - Design (Kỹ Thuật Thiết Kế)
    "KT",      # Technical - Engineering (Kỹ Thuật)
    "QLDA",    # Project Management (Quản Lý Dự Án)
    "SX",      # Production (Sản Xuất)
    "TCKT",    # Technical Cost (Tính Chi Phí Kỹ Thuật)
    "QAQC",    # QA/QC
    "TM",      # Trade/Commerce (Thương Mại)
]

# Task Types Enum
TASK_TYPES = [
    "COST_ESTIMATE",
    "TECHNICAL_REVIEW",
    "CAPACITY_CHECK",
    "MATERIAL_PRICING",
    "QUOTATION_REVIEW",
    "CUSTOMER_FOLLOW_UP",
    "PROJECT_HANDOFF",
    "INVOICE_REQUEST",
    "QUALITY_REVIEW",
    "CONTRACT_REVIEW",
    "GENERAL",
]

# Opportunity Stages Enum
OPPORTUNITY_STAGES = [
    "PROSPECT",
    "CONTACTED",
    "RFQ_RECEIVED",
    "COSTING",
    "QUOTED",
    "NEGOTIATION",
    "WON",
    "LOST",
    "IN_PROGRESS",
]

# Email Types Enum — Canonical 10 types (unified from CLAUDE.md)
EMAIL_TYPES = [
    "RFQ",           # Request for Quotation
    "TECHNICAL",     # Technical inquiry/discussion
    "NEGOTIATION",   # Price/terms negotiation
    "CONTRACT",      # Contract-related (PO, award)
    "PAYMENT",       # Invoice/payment/remittance
    "FOLLOWUP",      # Follow-up/reminder
    "INTERNAL",      # Internal communication
    "VENDOR",        # Supplier/vendor communication
    "COMPLAINT",     # Complaint/claim
    "GENERAL",       # General/unclassified (fallback)
]

# Task Statuses
TASK_STATUSES = [
    "PENDING",
    "IN_PROGRESS",
    "COMPLETED",
    "OVERDUE",
    "CANCELLED",
]

# Email Activity Actions
EMAIL_ACTIVITY_ACTIONS = [
    "RECEIVED",
    "CLASSIFIED",
    "LINKED_TO_OPP",
    "TASK_CREATED",
    "REPLY_DRAFTED",
    "REPLY_SENT",
    "FLAGGED",
    "ARCHIVED",
]
