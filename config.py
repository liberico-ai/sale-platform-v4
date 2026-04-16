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
SALE_DB_PATH = os.getenv("SALE_DB_PATH", "./sale_platform.db")

# PostgreSQL Configuration (if DB_TYPE == "postgresql")
PG_DSN = os.getenv(
    "PG_DSN",
    "postgresql://user:password@localhost:5432/ibs_hi_sale"
)

# API Keys Configuration (3-tier system)
# IMPORTANT: Set via environment variables. Do NOT use defaults in production.
_admin_key_1 = os.getenv("ADMIN_API_KEY_1", "")
_admin_key_2 = os.getenv("ADMIN_API_KEY_2", "")
_manager_key_1 = os.getenv("MANAGER_API_KEY_1", "")
_manager_key_2 = os.getenv("MANAGER_API_KEY_2", "")
_viewer_key_1 = os.getenv("VIEWER_API_KEY_1", "")
_viewer_key_2 = os.getenv("VIEWER_API_KEY_2", "")

API_KEYS: Dict[str, str] = {}
if _admin_key_1:
    API_KEYS[_admin_key_1] = "ADMIN"
if _admin_key_2:
    API_KEYS[_admin_key_2] = "ADMIN"
if _manager_key_1:
    API_KEYS[_manager_key_1] = "MANAGER"
if _manager_key_2:
    API_KEYS[_manager_key_2] = "MANAGER"
if _viewer_key_1:
    API_KEYS[_viewer_key_1] = "VIEWER"
if _viewer_key_2:
    API_KEYS[_viewer_key_2] = "VIEWER"

# Dev mode: if no keys configured, allow a dev key
if not API_KEYS and os.getenv("SALE_ENV", "development") == "development":
    API_KEYS["dev-key-local-only"] = "ADMIN"

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
