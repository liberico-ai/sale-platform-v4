# IBS HI Sale Platform Phase 1 - Router Files Manifest

## Overview
Complete API router implementation for IBS HI Sale Platform Phase 1, following FastAPI patterns and design specifications from System Design document.

**Created**: 2026-04-15  
**Target**: /Users/huyenleduy/Library/CloudStorage/GoogleDrive-leduyhuyen@gmail.com/My Drive/IBS HI/Sale/sale_platform_v4/routers/

---

## Router Files (10 total)

### 1. `__init__.py`
Package initialization file. Exports all router modules for use in main.py.

---

### 2. `health.py`
**Prefix**: `/health`  
**Endpoints**: 1

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | System health check with version and db_type |

**Features**:
- Returns status, version (1.0.0), and database type
- No authentication required

---

### 3. `customers.py`
**Prefix**: `/customers`  
**Endpoints**: 3

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `` | GET | List customers with region/status filtering, limit/offset pagination |
| `/search` | GET | Search customers by name, code, or email (LIKE query) |
| `/{customer_id}` | GET | Get customer detail with contacts + opportunities |

**Features**:
- Dynamic WHERE clause building
- Full-text search across name, code, email
- Nested related data (contacts, opportunities)
- Pagination support (limit 1-200, offset)

---

### 4. `opportunities.py`
**Prefix**: `/opportunities`  
**Endpoints**: 5

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `` | GET | List pipeline opportunities with stage/product/AM filtering |
| `` | POST | Create opportunity |
| `/{opp_id}` | PATCH | Update stage/win%/notes/assigned_to (auto updated_at) |
| `/{opp_id}` | GET | Detail with related emails + tasks |
| `/stale` | GET | Stale deals (>30 days no activity, stale_flag=1) |

**Features**:
- Pipeline stage filtering
- Auto-timestamp on updates
- Stale deal detection via last_activity_date
- Nested email and task lists

**Models**:
- `OpportunityCreate`: customer_id, project_name, product_group, expected_value, etc.
- `OpportunityUpdate`: stage, win_percentage, notes, assigned_to

---

### 5. `emails.py`
**Prefix**: `/emails`  
**Endpoints**: 5

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `` | GET | List emails with type/read/actioned/dept/date filtering |
| `/{email_id}` | GET | Email detail with complete thread |
| `/sync` | POST | Trigger Gmail sync |
| `/{email_id}` | PATCH | Update classification, link opp, mark read/actioned |
| `/{email_id}/create-task` | POST | Create task from email context (auto link email_id + opp_id) |

**Features**:
- Thread grouping by thread_id
- Multi-criteria filtering
- Task auto-creation with activity logging
- Email activity audit trail

**Models**:
- `EmailUpdate`: classification, opportunity_id, is_read, is_actioned
- `TaskFromEmailCreate`: task_type, title, to_dept, assigned_to, priority, etc.

---

### 6. `tasks.py`
**Prefix**: `/tasks`  
**Endpoints**: 6

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `` | GET | List tasks with status/dept/assigned filtering, priority ordering |
| `` | POST | Create task (auto log activity if email_id present) |
| `/{task_id}` | PATCH | Update status/result/assigned_to (auto timestamps) |
| `/{task_id}/escalate` | POST | Escalate task (increment count, set escalated_to) |
| `/board` | GET | Kanban board data grouped by status |
| `/my` | GET | My tasks (filter by assigned_to from auth context) |

**Features**:
- Auto timestamp management (started_at on IN_PROGRESS, completed_at on COMPLETED)
- Kanban board grouping (PENDING, IN_PROGRESS, COMPLETED, OVERDUE)
- Escalation tracking
- Personal task list endpoint

**Models**:
- `TaskCreate`: task_type, title, from_dept, to_dept, priority, sla_hours, etc.
- `TaskUpdate`: status, result, assigned_to, notes
- `TaskEscalate`: escalated_to

---

### 7. `dashboard.py`
**Prefix**: `/dashboard`  
**Endpoints**: 6

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/pipeline` | GET | Pipeline KPIs vs KHKD targets (weighted value, coverage ratio, by stage) |
| `/pipeline/by-product` | GET | Breakdown by 7 product groups with target comparison |
| `/pipeline/by-quarter` | GET | Revenue by quarter (estimated_signing date grouping) |
| `/tasks` | GET | Task stats (total, overdue, pending, by dept) |
| `/emails` | GET | Email stats (unread, unactioned, by type, by dept) |
| `/executive` | GET | BD Director overview (all KPIs combined) |

**Features**:
- Comprehensive KPI aggregations
- KHKD target comparison
- Product group breakdown (INFRASTRUCTURE, NETWORK, CLOUD, SECURITY, DATABASE, MIDDLEWARE, STORAGE)
- Quarter-based revenue projection
- Multi-metric executive summary

---

### 8. `mailboxes.py`
**Prefix**: `/mailboxes`  
**Endpoints**: 4

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `` | GET | List monitored mailboxes with active/inactive status |
| `` | POST | Add new mailbox (token_valid=0 initially) |
| `/{mailbox_id}` | PATCH | Update enable/disable sync, deactivate |
| `/{mailbox_id}/oauth` | POST | Complete OAuth flow (receive token, token_valid=1) |

**Features**:
- Gmail mailbox management
- OAuth flow completion
- Sync status tracking
- Duplicate prevention

**Models**:
- `MailboxCreate`: email_address, mailbox_type, department
- `MailboxUpdate`: is_active, sync_enabled, deactivated_at
- `OAuthCallback`: code, state

---

### 9. `users.py`
**Prefix**: `/users`  
**Endpoints**: 3

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `` | GET | List platform users with roles (filter by dept/active) |
| `` | POST | Add new user (onboard) |
| `/{user_id}` | PATCH | Update role/dept or deactivate (set deactivated_at) |

**Features**:
- User onboarding/offboarding
- Department and role management
- Deactivation tracking
- Permission JSON storage

**Models**:
- `UserCreate`: user_name, email, department, role, permissions
- `UserUpdate`: role, department, is_active, deactivated_at

---

### 10. `pm_integration.py`
**Prefix**: `/pm-integration`  
**Endpoints**: 6

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/project/{project_code}/status` | GET | Proxy to ibshi1 GET /api/projects?projectCode=xxx |
| `/tasks` | POST | Create WorkflowTask in ibshi1 (log to sync_log) |
| `/project/{project_code}/timeline` | GET | Get milestones + tasks from ibshi1 |
| `/draft-reply` | POST | Draft customer email based on PM data (status=DRAFT, requires_review=true) |
| `/draft-reply/{draft_id}/approve` | PATCH | Approve draft and send via Gmail API |
| `/sync-log` | GET | View sync history (filter by direction/project/status) |

**Features**:
- Async httpx calls to ibshi1 API
- Bearer token authentication
- Connection error handling (503 on ibshi1 unavailable)
- Draft email workflow (never auto-send)
- Bidirectional sync audit logging

**Models**:
- `WorkflowTaskCreate`: project_code, task_title, assigned_to, priority
- `DraftReplyCreate`: email_id, project_code, draft_content, recipient_email
- `DraftReplyApprove`: approved_by

---

## Shared Patterns

### Authentication Dependencies
- Most routers: `auth_dep = [Depends(require_auth)]`
- Mailboxes, Users: `write_dep = [Depends(require_write)]` (admin-only)

### ID Generation
```python
import uuid
id = str(uuid.uuid4())
```

### Timestamps
```python
from datetime import datetime
now = datetime.now().isoformat()
```

### Database Operations
```python
from ..database import query, execute

# Read
result = query("SELECT ... WHERE id = ?", [id], one=True)
results = query("SELECT ...", params)

# Write
execute("INSERT INTO ...", params)
execute("UPDATE ... WHERE id = ?", params + [id])
```

### Response Format (Lists)
```python
{
    "total": N,
    "items": [...],
    "limit": L,
    "offset": O
}
```

### Error Handling
```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Resource not found")
```

---

## Integration with main.py

Include routers in FastAPI app:
```python
from .routers import health, customers, opportunities, emails, tasks, dashboard, mailboxes, users, pm_integration

app.include_router(health.router)
app.include_router(emails.router,        prefix="/api/v1", dependencies=auth_dep)
app.include_router(tasks.router,         prefix="/api/v1", dependencies=auth_dep)
app.include_router(opportunities.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(customers.router,     prefix="/api/v1", dependencies=auth_dep)
app.include_router(dashboard.router,     prefix="/api/v1", dependencies=auth_dep)
app.include_router(mailboxes.router,     prefix="/api/v1", dependencies=write_dep)
app.include_router(users.router,         prefix="/api/v1", dependencies=write_dep)
app.include_router(pm_integration.router, prefix="/api/v1", dependencies=auth_dep)
```

---

## Total Endpoints

- **Health**: 1
- **Customers**: 3
- **Opportunities**: 5
- **Emails**: 5
- **Tasks**: 6
- **Dashboard**: 6
- **Mailboxes**: 4
- **Users**: 3
- **PM Integration**: 6

**Total: 39 endpoints** (40 including stale opportunities endpoint variations)

---

## Notes

- All routers use parameterized queries for SQLite/PostgreSQL compatibility
- Pydantic models for request/response validation
- Type hints throughout for IDE support
- Comprehensive docstrings with Args/Returns/Raises
- Async-ready endpoint definitions
- RESTful design with proper HTTP methods
