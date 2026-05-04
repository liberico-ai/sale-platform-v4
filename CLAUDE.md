# SALE PLATFORM PHASE 1 — CLAUDE CODE INSTRUCTIONS

## Context
Sale Platform v4.x prototype (AI-generated). Builder (Toàn) sẽ adapt thành v5.x production.
Tuân thủ TEAM_RULES v2.0, IBS One Architecture (AD-007/AD-008).

## Architecture
- **FastAPI** on port **8767** (standalone, shared PostgreSQL with ibshi1)
- **SQLite** (dev): `sale.db` | **PostgreSQL** (prod): schema `sale`
- **32 tables + 2 views** prefixed `sale_`, **92 indexes**, **40+ API endpoints**, **3 sprints**
- Gmail API OAuth 2.0 for dynamic mailboxes
- 2-way sync with ibshi1 (Next.js:3000) via HTTP
- **State Machine**: opportunity stages + task statuses with validated transitions
- **Audit Log**: all financial/status changes tracked in `sale_audit_log`
- **structlog**: structured JSON logging (no print() in core code)
- **APScheduler**: 3 background workers (Gmail 5min, SLA 15min, Stale daily)
- **PG Connection Pool**: `SimpleConnectionPool(min=2, max=10)` via psycopg2

## Database Build (IMPORTANT — read first)
The SQLite dev database is built from the `sql_import/` pipeline. **Always rebuild before coding.**

```bash
cd sql_import/
python build_db.py          # → produces ../sale.db (~6,700+ records)
# OR with sqlite3 CLI:
sqlite3 ../sale.db < master_import.sql
```

**Pipeline structure:**
1. `schema_all.sql` — 32 tables + 2 views + 92 indexes + seed data
2. `01_customers.sql` → `25_client_visits.sql` — 27 data import files (idempotent, INSERT OR IGNORE)
3. `99_import_log.sql` — import audit trail
4. `master_import.sql` — orchestrator that `.read`s all files in order inside a transaction

**Adding new data:** Create `26_xxx.sql`, add `.read 26_xxx.sql` to `master_import.sql` before `99_import_log.sql`, then rebuild.

## Folder Structure
```
sale_platform_v4/
├── CLAUDE.md                 ← THIS FILE
├── README.md                 ← Setup instructions for Builder
├── requirements.txt          ← Python dependencies (inc. structlog)
├── schema.sql                ← Original 16-table schema (legacy ref)
├── schema_pg.sql             ← PostgreSQL version with "sale" schema
├── sale.db                   ← Built SQLite database (git-ignored, rebuild from sql_import/)
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
│   ├── state_machine.py      ← Opportunity + Task state transitions
│   ├── audit.py              ← Audit log for financial/status changes
│   ├── khkd_tracker.py       ← KHKD target comparison
│   └── pm_bridge.py          ← Sale↔PM integration service
├── workers/
│   ├── __init__.py
│   ├── gmail_worker.py       ← Periodic Gmail sync (5 min interval)
│   ├── sla_worker.py         ← SLA check + auto-escalation (15 min)
│   ├── stale_worker.py       ← Stale deal detection (daily 8:00 AM)
│   └── pm_sync_worker.py     ← PM sync polling (10 min, Sprint 3)
├── scripts/
│   ├── import_customers.py   ← Import Workflow 2026 → sale_customers
│   ├── import_pipeline.py    ← Import IBSHI Potential → sale_opportunities
│   ├── import_khkd.py        ← Import KHKD RevC targets
│   └── seed_templates.py     ← Seed email templates
├── sql_import/               ← ★ DB BUILD PIPELINE (source of truth)
│   ├── build_db.py           ← Python DB builder (no sqlite3 CLI needed)
│   ├── master_import.sql     ← Orchestrator: .read all files in transaction
│   ├── schema_all.sql        ← 32 tables + 2 views + 92 indexes (1,012 lines)
│   ├── 01_customers.sql      ← 109 base customers (Workflow 2026)
│   ├── 02_opportunities.sql  ← 25 pipeline opportunities
│   ├── 02b_active_contracts.sql ← Active contracts with milestones
│   ├── 03-10_*.sql           ← Milestones, settlements, NAS links, quotations, etc.
│   ├── 11-13_*.sql           ← Email scan (ibshi@), interactions, market signals
│   ├── 14-16_*.sql           ← Mbox: 577 customers, 2,807 contacts, email stats
│   ├── 17-19_*.sql           ← Quotation Record: 1,007 quotes, 185 won contracts
│   ├── 20-23_*.sql           ← 2026 emails: quotations, active contracts, labels, mapping
│   ├── 24_client_database.sql ← 172 customers + 164 contacts (Client_Data_Base GSheet)
│   ├── 25_client_visits.sql  ← 142 client visits Oct 2022 – Apr 2026
│   └── 99_import_log.sql     ← Import audit entries
└── docs/
    ├── ADR-001-python-for-sale-platform.md
    └── etl_mapping.md        ← Full ETL source→target mapping
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

## Database Tables (32 tables + 2 views)
### Core CRM (7)
`sale_customers` (992 records), `sale_customer_contacts` (2,990), `sale_product_categories`, `sale_opportunities` (25), `sale_customer_interactions` (175), `sale_commissions`, `sale_digital_content` (11)

### Email & Communication (5)
`sale_emails` (125), `sale_email_templates`, `sale_email_activity_log`, `sale_email_labels` (47), `sale_email_full` (108)

### Pipeline & Quotation (4)
`sale_quotation_revisions` (160), `sale_quotation_history` (1,007), `sale_quote_templates`, `sale_active_contracts` (14)

### Contract & Finance (4)
`sale_contract_milestones` (48), `sale_change_orders`, `sale_settlements` (28), `sale_khkd_targets`

### Operations & System (8)
`sale_tasks`, `sale_follow_up_schedules`, `sale_nas_file_links` (1,112), `sale_monitored_mailboxes`, `sale_user_roles`, `sale_pm_sync_log`, `sale_import_log` (27), `sale_audit_log`

### Intelligence (2)
`sale_market_signals` (18), `sale_product_opportunities` (56)

### Inter-department (2)
`sale_inter_dept_tasks`, `sale_report_configs`

### Views (2)
`v_sale_followups`, `v_project_activity`

## Data Sources (import pipeline order)
| File | Source | Records | Key Data |
|------|--------|---------|----------|
| 01 | Workflow 2026 GSheet | 109 | Base customers |
| 02 | IBSHI Potential GSheet | 25 | Pipeline opportunities |
| 02b-10 | NAS + internal docs | ~1,400 | Contracts, milestones, settlements, NAS links, quotations |
| 11-13 | ibshi@ Gmail scan | ~160 | Emails, interactions, market signals |
| 14-16 | 218MB mbox archive | ~3,400 | Historical customers, contacts, email stats |
| 17-19 | Quotation Record xlsx | ~1,300 | Quote history, new customers, won contracts |
| 20-23 | ibshi@ Chrome 2026 | ~180 | Active quotations, contracts, email labels, full mapping |
| 24-25 | Client_Data_Base GSheet | ~330 | CDB customers, contacts, client visits |
| **TOTAL** | | **~6,700+** | |

## Key Business Data
- KHKD 2026: $19.1M revenue, 7,000 tons, 21% GM, 25 POs
- Pipeline: 25 projects from IBSHI Potential, weighted ~$43M
- 7 product groups: HRSG, Diverter, Shipbuilding, PV, Handling, Duct, Other
- 992 customers (from multiple sources, deduplicated)
- 2,990 customer contacts (from mbox + CDB + manual)
- Gmail: ibshi@ibs.com.vn + hieunh@ibs.com.vn (initial)
- 10 email types: RFQ, TECHNICAL, NEGOTIATION, CONTRACT, PAYMENT, FOLLOWUP, INTERNAL, VENDOR, COMPLAINT, GENERAL

## Running
```bash
# Step 1: Build the database
cd sql_import/ && python build_db.py && cd ..

# Step 2: Start the server
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

## DB Import Conventions
- All SQL files use `INSERT OR IGNORE` for idempotent re-runs
- Customer IDs: deterministic UUID via `MD5(source || '::' || key)` — same input = same ID
- Enrichment pattern: `UPDATE sale_customers SET field = COALESCE(field, new_value)` — never overwrite existing data
- Each import file logs to `sale_import_log` via `99_import_log.sql`
- `schema_all.sql` is the SINGLE source of truth for table definitions (not schema.sql or schema_pg.sql)
- New import files: sequential numbering (next = 26), add to master_import.sql before 99_import_log.sql

## Claude Code Workflow (MUST follow)
### Before any coding:
```bash
cd sql_import/ && python build_db.py && cd ..
```
Verify: 32 tables, ~6,700 records, 0 integrity errors.

### Known gaps to fix:
1. `database.py` line 31: change `schema.sql` → `sql_import/schema_all.sql`
2. Add routers for new tables: contracts, intelligence, interactions
3. Update models/ to match all 32 tables in schema_all.sql
4. Update dashboard.py to query across all populated tables

### ★ UNIFIED COMMAND (ĐỌC FILE NÀY ĐẦU TIÊN):
- **UNIFIED_CLAUDE_CODE_COMMAND.md** — Lệnh DUY NHẤT hợp nhất tất cả fixes. 18 bước, ~65h. **PASTE VÀO CLAUDE CODE.**

### Reference docs (đã merge vào UNIFIED, ĐỌC NẾU CẦN CHI TIẾT):
- CROSS_CUTTING_DESIGN.md — 10 patterns đồng bộ xuyên suốt
- FUNCTIONAL_COMPLETENESS_AUDIT.md — Gap analysis chức năng (updated 03/05/2026)
- SALE_PLATFORM_MASTER_FIX.md — Align code ↔ DB schema + 3 câu hỏi tích hợp

### Cross-cutting rules (bổ sung rules 16-20):
16. KHÔNG define Pydantic model inline trong router — import từ models/
17. TẤT CẢ status/stage/type dùng Enum (models/enums.py)
18. TẤT CẢ list endpoints dùng standard pagination {total, items, limit, offset}
19. TẤT CẢ write endpoints pass user_id vào audit_log changed_by
20. TẤT CẢ date SQL dùng dialect helpers (now_expr, date_diff_expr)

### Thứ tự: Chạy UNIFIED_CLAUDE_CODE_COMMAND.md (18 bước theo thứ tự)

### For detailed sprint plan: see SPRINT1_PLAN.md
### For full NAS gap analysis + module roadmap: see SPRINT1_PLAN.md (NAS Business Process Map section)
### Reference: docs/Sale_Platform_v4_Gap_Analysis_28Apr2026.docx — 13 NAS business functions, 31% coverage, 5-phase roadmap

