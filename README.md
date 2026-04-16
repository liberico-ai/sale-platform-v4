# IBS HI Sale Platform v4 - Phase 1

Sales pipeline & email management platform for IBS HI, with Gmail integration, email classification, SLA monitoring, and PM bridge to ibshi1 L1 platform.

**Status:** Sprint 1-3 Complete (Apr 2026)
**Team:** Builder (Toàn), AH (oversight)
**Users:** Hiệu, Paul, Ngoãn, Hùng (SALE dept)

---

## Project Overview

### What It Does

1. **Gmail Integration** — Auto-sync emails from monitored mailboxes (ibshi@, hieunh@)
2. **Email Classification** — Rule-based 10-type classifier (RFQ, TECHNICAL, NEGOTIATION, CONTRACT, PAYMENT, FOLLOWUP, INTERNAL, VENDOR, COMPLAINT, GENERAL)
3. **Customer Matching** — Link emails to customers by domain
4. **Auto-Actions** — Create tasks for high-confidence RFQs, draft acknowledgments (NEVER auto-send)
5. **SLA Monitoring** — Track task deadlines, escalate overdue items
6. **Stale Deal Detection** — Flag opportunities with >30 days no activity
7. **Pipeline Dashboard** — Compare against KHKD 2026-2027 targets by product group
8. **PM Bridge** — Sync project updates from ibshi1 (milestones, tasks)

### Architecture

```
Mac Mini M2
├── ibshi1 (L1 Platform, Next.js:3000)
├── Sale Platform (L2, FastAPI:8767)
│   ├── 16 database tables (PostgreSQL schema "sale")
│   ├── 40+ API endpoints (v1)
│   ├── Background workers (APScheduler)
│   └── Gmail + PM sync engines
├── PostgreSQL 16
└── External APIs
    ├── Gmail API
    ├── NAS Synology
    └── Telegram (future)
```

### Data

- **Customers:** ~988 from Workflow 2026
- **Pipeline:** ~25 deals from IBSHI Potential (~$61M raw)
- **KHKD Targets:** FY2026-2027 ($19.1M revenue, 7000 tons, 21% GM)
- **Email Volume:** ~1500/month across 2 mailboxes

---

## Setup Instructions

### 1. Prerequisites

```bash
# Python 3.10+
python --version

# Required packages
pip install fastapi uvicorn python-multipart
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
pip install httpx apscheduler
pip install openpyxl  # For Excel imports
pip install psycopg2-binary  # For PostgreSQL (or sqlite3 for dev)
```

### 2. Database Setup

```bash
# SQLite (development)
python
>>> from database import init_db
>>> init_db()

# PostgreSQL (production)
# Create schema "sale" first, then run migrations
psql -h localhost -U postgres -c "CREATE SCHEMA sale;"
python migrate.py  # Runs all migrations from 01_DATABASE/migrations/
```

### 3. Gmail OAuth Setup

```bash
# Place OAuth credentials in repo root
# File: .gmail_credentials.json (from Google Cloud Console)

# First-time users will be prompted to authorize in browser
# Tokens stored in: .gmail_tokens/{email}.json
```

### 4. Data Import (Day 1)

```bash
# Import customers
python scripts/import_customers.py /path/to/workflow_2026.xlsx

# Import pipeline
python scripts/import_pipeline.py /path/to/ibshi_potential.xlsx

# Import KHKD targets
python scripts/import_khkd.py

# Seed email templates
python scripts/seed_templates.py
```

### 5. Environment Variables

```bash
# Copy .env.example → .env  and fill in values
cp .env.example .env

# Key variables:
SALE_ENV=production           # development | production
DB_TYPE=postgresql             # sqlite or postgresql
PG_DSN=postgresql://user:pass@localhost:5432/ibs_hi_sale
PG_POOL_MAX=10                 # PG connection pool size

ADMIN_API_KEY_1=<uuid>         # Generate: python3 -c "import uuid; print(uuid.uuid4().hex)"
MANAGER_API_KEY_1=<uuid>
VIEWER_API_KEY_1=<uuid>

CORS_ORIGINS=http://localhost:3000  # Comma-separated

IBSHI1_URL=http://localhost:3000
IBSHI1_TOKEN=<bearer-token>

GMAIL_CREDENTIALS_PATH=./credentials/gmail_credentials.json
GMAIL_TOKENS_DIR=./tokens/

ENABLE_EMAIL_SYNC=true
ENABLE_PM_INTEGRATION=true
ENABLE_TASK_SCHEDULING=true
LOG_LEVEL=INFO
```

### 6. Start Server

```bash
# Development
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8767

# Production (Mac Mini M2)
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8767 > sale_platform.log 2>&1 &
```

### 7. Start Background Workers

```bash
# All workers auto-start via APScheduler when server boots
# Schedule:
# - gmail_worker: every 5 minutes
# - sla_worker: every 15 minutes
# - stale_worker: daily 8:00 AM
# - pm_sync_worker: every 10 minutes
```

---

## API Documentation

### Base URL

```
http://localhost:8767
```

### Health Check

```bash
GET /health

Response: {"status": "ok", "timestamp": "2026-04-15T12:00:00"}
```

### Core Endpoints

#### Emails

```
GET    /api/v1/emails              # List emails (filter: type, date, read)
GET    /api/v1/emails/{id}         # Email detail + thread
PATCH  /api/v1/emails/{id}         # Update: classify, link opp, mark read
POST   /api/v1/emails/{id}/create-task    # Create task from email
POST   /api/v1/emails/{id}/link-opp       # Link email to opportunity
POST   /api/v1/emails/sync         # Trigger Gmail sync
```

#### Tasks

```
GET    /api/v1/tasks               # List tasks (filter: status, dept, assigned)
POST   /api/v1/tasks               # Create task
PATCH  /api/v1/tasks/{id}          # Update task (status, result)
POST   /api/v1/tasks/{id}/escalate # Escalate task
```

#### Opportunities

```
GET    /api/v1/opportunities           # List pipeline (filter: stage, product, AM)
POST   /api/v1/opportunities           # Create opportunity
PATCH  /api/v1/opportunities/{id}      # Update (stage, win%, notes)
GET    /api/v1/opportunities/{id}      # Detail + emails + tasks
GET    /api/v1/opportunities/stale     # Stale deals (>30d no update)
```

#### Dashboard

```
GET    /api/v1/dashboard/pipeline           # Pipeline KPIs vs. KHKD targets
GET    /api/v1/dashboard/pipeline/by-product # By 7 product groups
GET    /api/v1/dashboard/tasks              # Task stats
GET    /api/v1/dashboard/emails             # Email stats
GET    /api/v1/dashboard/executive          # BD Director overview
```

#### Customers

```
GET    /api/v1/customers           # List customers (filter: region, status)
GET    /api/v1/customers/{id}      # Customer + contacts + opportunities
GET    /api/v1/customers/search    # Search by name/code/email
```

#### PM Bridge (Phase 3)

```
GET    /api/v1/pm/project/{code}/status        # Get project status from ibshi1
POST   /api/v1/pm/tasks                        # Create task in ibshi1
GET    /api/v1/pm/project/{code}/timeline      # Get milestones + tasks
POST   /api/v1/pm/draft-reply                  # Draft email from PM data
PATCH  /api/v1/pm/draft-reply/{id}/approve     # Approve draft → send
GET    /api/v1/pm/sync-log                     # View sync history
```

### Full API Docs

Swagger UI: `http://localhost:8767/docs`

---

## Service Modules

### `services/gmail_service.py`

Gmail API wrapper with OAuth 2.0 authentication.

```python
from services import GmailService

gmail = GmailService()
creds = gmail.authenticate("ibshi@ibs.com.vn")
service = build("gmail", "v1", credentials=creds)

messages = gmail.list_messages(service, after_date="2026-04-15")
for msg in messages:
    parsed = gmail.parse_message(gmail.get_message(service, msg['id']))
    print(parsed['from_address'], parsed['subject'])
```

### `services/classifier.py`

Rule-based email classifier.

```python
from services import classify_email, match_customer

email_type, confidence = classify_email(parsed_email)
# Returns: ("RFQ", 0.92)

customer_id = match_customer("john@acme.com", customers_list)
# Returns: customer UUID or None
```

### `services/sla_engine.py`

SLA tracking and escalation.

```python
from services import get_sla_hours, calculate_due_date, ESCALATION_CHAIN

hours = get_sla_hours("COST_ESTIMATE")  # Returns: 48
due = calculate_due_date("COST_ESTIMATE")  # Returns: ISO string
chain = ESCALATION_CHAIN  # {"MEMBER": "MANAGER", "MANAGER": "BD_DIRECTOR", ...}
```

### `services/khkd_tracker.py`

KHKD target vs pipeline comparison.

```python
from services import get_pipeline_vs_khkd, get_by_product_group

summary = get_pipeline_vs_khkd()
# Returns: target_revenue, actual_revenue, coverage_ratio, etc.

by_group = get_by_product_group()
# Returns list of 7 product groups with breakdowns
```

### `services/pm_bridge.py`

PM ↔ Sale synchronization via ibshi1 API.

```python
from services import PMBridge

bridge = PMBridge()
status = await bridge.get_project_status("PRJ-001")
# Returns: project, milestones, tasks_summary

task = await bridge.create_pm_task(opp_id, "PROGRESS_REPORT", title, desc, "ENGINEERING")
# Creates task in ibshi1, logs to sale_pm_sync_log

draft = await bridge.draft_reply_email(opp_id, "Milestone Update", "MILESTONE_UPDATE")
# Returns: {to, subject, body, status="DRAFT", requires_review=True}
```

---

## Worker Processes

All workers run automatically via APScheduler on schedule:

### `workers/gmail_worker.py` (every 5 minutes)

- Fetches new emails from monitored mailboxes
- Classifies each email
- Matches to customer by domain
- Auto-creates COST_ESTIMATE task for RFQ (confidence > 0.8)
- Creates DRAFT acknowledgment for RFQs (NEVER auto-sends)

### `workers/sla_worker.py` (every 15 minutes)

- Checks all active tasks for overdue status
- Escalates overdue tasks through chain: assigned_to → manager → BD Director
- Logs escalations

### `workers/stale_worker.py` (daily 8:00 AM)

- Finds opportunities with >30 days no activity
- Sets stale_flag=1
- Creates CUSTOMER_FOLLOW_UP task for assigned sales person

### `workers/pm_sync_worker.py` (every 10 minutes)

- Polls ibshi1 for changes on active projects
- Detects milestone completions → drafts customer email
- Detects overdue PM tasks → creates Sale follow-up task
- Logs all syncs to sale_pm_sync_log

---

## Import Scripts

All scripts in `scripts/` are one-time data population utilities.

### `import_customers.py`

Import customer master from Workflow 2026 Excel.

```bash
python scripts/import_customers.py /path/to/workflow_2026.xlsx

# Expected: ~988 customer records
# Output: sale_customers + sale_customer_contacts, logged in sale_import_log
```

### `import_pipeline.py`

Import sales pipeline from IBSHI Potential Excel.

```bash
python scripts/import_pipeline.py /path/to/ibshi_potential.xlsx

# Expected: ~25 deals, $61M raw value
# Output: sale_opportunities, logged in sale_import_log
```

### `import_khkd.py`

Import KHKD 2026-2027 targets.

```bash
python scripts/import_khkd.py

# Expected: 1 consolidated + 7 product group records
# Values: $19.1M revenue, 7000 tons, 21% GM
# Output: sale_khkd_targets, logged in sale_import_log
```

### `seed_templates.py`

Seed 6 email templates.

```bash
python scripts/seed_templates.py

# Templates: RFQ_ACK, FOLLOWUP_3D, FOLLOWUP_7D, FOLLOWUP_14D, FOLLOWUP_30D, QUOTATION_COVER
# Output: sale_email_templates, logged in sale_import_log
```

---

## For Toàn (v5.x Production)

When building v5.x production version, consider:

1. **Database Migration** — Switch from SQLite to PostgreSQL on Mac Mini M2
   - Ensure schema "sale" exists
   - Run all migrations: `python migrate.py`
   - Test connection: `psql -h localhost -U postgres -d ibs_sale_v5`

2. **Gmail Scaling** — Current limit ~100 messages per sync
   - Consider batch processing for >1000 emails/day
   - Token refresh strategy for long-lived process

3. **PM Bridge Error Handling** — Add circuit breaker for ibshi1 API
   - Timeout handling (currently 10s)
   - Retry logic with backoff

4. **NAS File Integration** — Phase 3 feature
   - Link drawing files from NAS Synology
   - Store paths in sale_attachments table
   - UI: click file path → open in Finder

5. **Telegram Bot** — Phase 3 feature
   - Alert on overdue tasks, stale deals
   - Quick task status updates

6. **Authentication** — Currently basic role-based
   - Consider JWT tokens for API security
   - RBAC per-department (SALE, DESIGN, QA, etc.)

7. **Audit Logging** — All changes logged
   - sale_import_log, sale_pm_sync_log already in place
   - Consider additional audit_log table for API calls

8. **Performance** — Monitor slow queries
   - Add indexes on frequently queried columns: project_code, customer_code, status, stage
   - Cache KHKD targets (rarely change)

9. **Testing** — Phase 3 deliverable
   - Unit tests for classifiers (email type accuracy)
   - Integration tests for PM bridge
   - End-to-end: RFQ → Task → Follow-up email

10. **Go-Live Checklist** — Before May 2026
    - ✓ All 16 tables created (inc. sale_audit_log)
    - ✓ Data imported (988 customers, 25 deals, KHKD targets)
    - ✓ Gmail sync stable
    - ✓ SLA escalation tested
    - ✓ Email templates finalized
    - ✓ UI screens approved
    - ✓ User training completed
    - ✓ Production deployment on Mac Mini M2

---

## Support & Troubleshooting

### Gmail Sync Not Working

1. Check token file exists: `.gmail_tokens/{email}.json`
2. Re-authenticate: Delete token file, restart server
3. Check credentials: `.gmail_credentials.json` valid format?
4. Check scope permissions in Google Cloud Console

### Classifier Confidence Too Low

- Rule weights in `services/classifier.py` lines 20-50
- Add/remove patterns to match your email style
- Manual review: POST `/api/v1/emails/{id}` to override classification

### PM Bridge Timeouts

- Check ibshi1 running: `curl http://localhost:3000/health`
- Increase timeout in `pm_bridge.py` line 33: `timeout=10`
- Check network: `ping localhost`

### Database Connection Error

- SQLite: file exists at DB_PATH?
- PostgreSQL: `psql -h localhost -U postgres -c "\l"` shows ibs_sale_v5?
- Check credentials in `.env`

### Workers Not Running

- Check APScheduler started: look for "[apscheduler]" in logs
- Check sys.modules has apscheduler: `python -c "import apscheduler"`
- Check schedule times: `python -c "from workers import sync_gmail; print(sync_gmail.__doc__)"`

---

## Project Structure

```
sale_platform_v4/
├── README.md                        # This file
├── main.py                          # FastAPI app entry point (to be created)
├── config.py                        # Configuration (to be created)
├── database.py                      # Database connection (to be created)
├── auth.py                          # Authentication (to be created)
├── services/
│   ├── __init__.py
│   ├── gmail_service.py             # Gmail API wrapper
│   ├── classifier.py                # Email classifier (9 types)
│   ├── sla_engine.py                # SLA monitoring + escalation
│   ├── khkd_tracker.py              # KHKD vs pipeline comparison
│   └── pm_bridge.py                 # PM ↔ Sale synchronization
├── workers/
│   ├── __init__.py
│   ├── gmail_worker.py              # Email sync (every 5 min)
│   ├── sla_worker.py                # SLA check (every 15 min)
│   ├── stale_worker.py              # Stale deal detection (daily 8am)
│   └── pm_sync_worker.py            # PM sync (every 10 min)
├── routers/                         # API routers (to be created)
│   ├── __init__.py
│   ├── emails.py
│   ├── tasks.py
│   ├── opportunities.py
│   ├── customers.py
│   ├── dashboard.py
│   ├── mailboxes.py
│   ├── users.py
│   └── pm_bridge.py
└── scripts/
    ├── __init__.py
    ├── import_customers.py          # Import ~988 customers
    ├── import_pipeline.py           # Import ~25 deals
    ├── import_khkd.py               # Import KHKD targets
    └── seed_templates.py            # Seed 6 email templates
```

---

## References

- **System Design:** `/Users/huyenleduy/Documents/Claude/Projects/IBS HI/IBS HI/Sale_Phase1_System_Design_and_Dev_Plan.md`
- **Database Schema:** `01_DATABASE/ibs_sale_v5.db` or `ibs_sale_v5.sql`
- **Admin Platform:** `project_admin_platform.md`
- **QA/QC Platform:** `project_qaqc_platform.md`

---

**Last Updated:** 2026-04-16
**Version:** v4.0 (Sprint 1-3 Complete)
**Status:** Ready for production deployment
