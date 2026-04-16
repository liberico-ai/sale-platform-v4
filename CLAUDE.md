# SALE PLATFORM PHASE 1 — CLAUDE CODE INSTRUCTIONS

## Context
Sale Platform v4.x prototype (AI-generated). Builder (Toàn) sẽ adapt thành v5.x production.
Tuân thủ TEAM_RULES v2.0, IBS One Architecture (AD-007/AD-008).

## Architecture
- **FastAPI** on port **8767** (standalone, shared PostgreSQL with ibshi1)
- **SQLite** (dev): `sale_platform.db` | **PostgreSQL** (prod): schema `sale`
- **16 tables** prefixed `sale_`, **40+ API endpoints**, **3 sprints**
- Gmail API OAuth 2.0 for dynamic mailboxes
- 2-way sync with ibshi1 (Next.js:3000) via HTTP
- **State Machine**: opportunity stages + task statuses with validated transitions
- **Audit Log**: all financial/status changes tracked in `sale_audit_log`
- **structlog**: structured JSON logging (no print() in core code)
- **APScheduler**: 3 background workers (Gmail 5min, SLA 15min, Stale daily)
- **PG Connection Pool**: `SimpleConnectionPool(min=2, max=10)` via psycopg2

## Folder Structure
```
sale_platform_v4/
├── CLAUDE.md                 ← THIS FILE
├── README.md                 ← Setup instructions for Builder
├── requirements.txt          ← Python dependencies (inc. structlog)
├── schema.sql                ← Full 16-table schema (SQLite)
├── schema_pg.sql             ← PostgreSQL version with "sale" schema
├── main.py                   ← FastAPI app entry point + scheduler
├── config.py                 ← Configuration (env vars, paths)
├── database.py               ← DB connection (SQLite/PG pool, auto-init)
├── auth.py                   ← X-API-Key 3-tier auth
├── routers/
│   ├── __init__.py
│   ├── health.py             ← GET /health (public)
│   ├── customers.py          ← 3 endpoints (auth)
│   ├── opportunities.py      ← 5 endpoints (auth) + state machine
│   ├── emails.py             ← 5 endpoints (auth)
│   ├── tasks.py              ← 6 endpoints (auth) + state machine
│   ├── dashboard.py          ← 6 endpoints (auth)
│   ├── mailboxes.py          ← 4 endpoints (write)
│   ├── users.py              ← 3 endpoints (write)
│   └── pm_integration.py     ← 6 endpoints (auth)
├── services/
│   ├── __init__.py
│   ├── gmail_service.py      ← Gmail API wrapper (DRAFT only, no auto-send)
│   ├── classifier.py         ← Email classification (10-type rule-based)
│   ├── sla_engine.py         ← SLA targets + escalation chain definition
│   ├── state_machine.py      ← Opportunity + Task state transitions [NEW]
│   ├── audit.py              ← Audit log for financial/status changes [NEW]
│   ├── khkd_tracker.py       ← KHKD target comparison
│   └── pm_bridge.py          ← Sale↔PM integration service
├── workers/
│   ├── __init__.py
│   ├── gmail_worker.py       ← Periodic Gmail sync (5 min interval)
│   ├── sla_worker.py         ← SLA check + auto-escalation (15 min)
│   ├── stale_worker.py       ← Stale deal detection (daily 8:00 AM)
│   └── pm_sync_worker.py     ← PM sync polling (10 min, Sprint 3)
└── scripts/
    ├── import_customers.py   ← Import Workflow 2026 → sale_customers
    ├── import_pipeline.py    ← Import IBSHI Potential → sale_opportunities
    ├── import_khkd.py        ← Import KHKD RevC targets
    └── seed_templates.py     ← Seed email templates
```

## State Machine Rules
### Opportunity Stages
```
PROSPECT → CONTACTED → RFQ_RECEIVED → COSTING → QUOTED → NEGOTIATION → WON → IN_PROGRESS
                                                                          ↘ LOST → PROSPECT
```
### Task Statuses
```
PENDING → IN_PROGRESS → COMPLETED
    ↓         ↓    ↑
CANCELLED  OVERDUE ─┘
```
**Enforcement**: Invalid transitions return HTTP 422 with allowed transitions list.

## Rules for Claude Code
1. **NEVER modify existing tables** — only CREATE TABLE / ADD COLUMN
2. **All imports MUST log to sale_import_log** — no exceptions
3. **SQLite-compatible types**: TEXT for UUID/datetime/JSON, INTEGER for boolean
4. **Query helper**: use `query()` for reads, `execute()` for writes
5. **Auth**: `Depends(require_auth)` for read, `Depends(require_write)` for write
6. **Naming**: tables `sale_*`, indexes `idx_{short}_{col}`, UUID primary keys
7. **Gmail tokens**: stored per-mailbox, NOT hardcoded
8. **PM integration**: NEVER auto-send email to customer — always DRAFT for review
9. **Logging**: use `structlog.get_logger()` — NO print() in services/workers
10. **State transitions**: MUST call `validate_*_transition()` before status changes
11. **Financial changes**: MUST audit-log via `services/audit.py`

## Key Business Data
- KHKD 2026: $19.1M revenue, 7,000 tons, 21% GM, 25 POs
- Pipeline: 25 projects from IBSHI Potential, weighted ~$43M
- 7 product groups: HRSG, Diverter, Shipbuilding, PV, Handling, Duct, Other
- 988 customers from Workflow 2026
- Gmail: ibshi@ibs.com.vn + hieunh@ibs.com.vn (initial)
- 10 email types: RFQ, TECHNICAL, NEGOTIATION, CONTRACT, PAYMENT, FOLLOWUP, INTERNAL, VENDOR, COMPLAINT, GENERAL

## Running
```bash
pip install -r requirements.txt
python main.py
# → http://localhost:8767/docs (Swagger)
# → http://localhost:8767/health
```

## Compliance Notes (ADR)
- ADR-001: Python/FastAPI accepted for Sale Platform L2 (exception to Hard Rule #4)
- Monetary columns: NUMERIC(15,2) in PostgreSQL, REAL with annotation in SQLite
- API Keys: MUST be set via environment variables (no hardcoded defaults)
- CORS: production MUST set CORS_ORIGINS env var (no wildcard)
- Email types: canonical 10 types — see config.py EMAIL_TYPES
- State machine: see services/state_machine.py — all transitions validated
- Audit: financial field changes logged to sale_audit_log automatically

