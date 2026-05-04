# SALE PLATFORM v4 — UNIFIED CLAUDE CODE COMMAND

> **Date:** 03/05/2026
> **Version:** 1.0 — Hợp nhất từ 3 documents: CROSS_CUTTING_DESIGN + FUNCTIONAL_COMPLETENESS_AUDIT + SALE_PLATFORM_MASTER_FIX
> **Mục đích:** Lệnh DUY NHẤT cho Claude Code sửa Sale Platform v4 từ prototype → team-ready
> **Nguồn audit:** GitHub repo `liberico-ai/sale-platform-v4` (25 routers, 90+ endpoints)
> **Input từ Chairman:** Quotation = Sale tự gửi, Notification = In-app badge, Users = 3-5 người, Documents = Link NAS

---

## HƯỚNG DẪN SỬ DỤNG

**Copy TOÀN BỘ nội dung trong block ``` ở Section LỆNH (cuối document) paste vào Claude Code.**
Phần trên là giải thích chi tiết — đọc để hiểu, KHÔNG cần paste.

---

## 1. HIỆN TRẠNG (GitHub 03/05/2026)

- **25 routers**, **90+ endpoints**, auth applied ở main.py router level
- **6 HTML frontend pages** (index, sale_dashboard, email-hub, task-board, pipeline, project-board)
- **5 workers** (gmail 5min, sla 15min, stale daily, followup daily 7AM, pm_sync 10min)
- **8 services** (classifier, state_machine, audit, sla_engine, gmail_service, khkd_tracker, pm_bridge, notify)
- **32 tables + 2 views**, ~6,700 records (SQLite dev → PostgreSQL prod)
- **10 test flows**, 22 test functions
- **Docker** + GitHub Actions CI/CD

---

## 2. TỔNG HỢP 20 VẤN ĐỀ CẦN FIX — 4 NHÓM

### NHÓM I: Cross-Cutting (fix TRƯỚC — tạo patterns cho code mới)

| # | Vấn đề | Severity | Effort | Mô tả |
|---|--------|----------|--------|-------|
| I-1 | Per-user identity (CC-1) | CRITICAL | 4h | Auth chỉ biết tier, không biết AI là AI → audit_log.changed_by=None |
| I-2 | Global exception handler (CC-3) | HIGH | 3h | Unhandled errors → raw 500, không structured response |
| I-3 | Thread-safe PG pool (CC-9) | HIGH | 0.5h | SimpleConnectionPool → ThreadedConnectionPool |
| I-4 | Enum validation (CC-7) | MEDIUM | 3h | status/stage/type là Optional[str] → bất kỳ string pass |
| I-5 | Models consolidation pilot (CC-6) | MEDIUM | 4h | 2 pilot routers import từ models/ (customers, quotations) |
| I-6 | Pagination consistency (CC-5) | MEDIUM | 2h | 4 routers không đồng nhất pagination format |
| I-7 | DB dialect helpers (CC-8) | MEDIUM | 3h | datetime('now') hardcoded → now_expr() wrapper |
| I-8 | Async DB wrappers (CC-2) | MEDIUM | 2h | Thêm async_query/async_execute, routers mới dùng async |

### NHÓM II: Frontend Fix (team dùng qua browser)

| # | Vấn đề | Severity | Effort | Mô tả |
|---|--------|----------|--------|-------|
| II-1 | Frontend field alignment (CC-4) | HIGH | 3h | customer_code→code, company_name→name, o.title→o.project_name |

### NHÓM III: Functional Gaps (features còn thiếu)

| # | Vấn đề | Priority | Effort | Mô tả |
|---|--------|----------|--------|-------|
| III-1 | Activity timeline per customer | HIGH | 3h | Unified timeline: interactions+emails+quotations sorted by date |
| III-2 | My Dashboard endpoint | HIGH | 2h | GET /dashboard/my → personal tasks, pipeline, follow-ups |
| III-3 | Report export XLSX/PDF | MEDIUM | 6h | GET /reports/{type}?format=xlsx |
| III-4 | Email compose flow | MEDIUM | 6h | Full compose → DRAFT → review → send (Gmail API) |
| III-5 | Duplicate detection | MEDIUM | 3h | Check trùng name/email khi tạo customer/contact |
| III-6 | Dashboard extended filters | MEDIUM | 3h | Date range, assigned_to, product_group trên mọi dashboard |
| III-7 | Soft DELETE | MEDIUM | 2h | SET status=DELETED cho customer, contact, opportunity |

### NHÓM IV: Quality & Safety

| # | Vấn đề | Priority | Effort | Mô tả |
|---|--------|----------|--------|-------|
| IV-1 | Test expansion (CC-10) | MEDIUM | 12h | 5 critical test files (quotations, contracts, contacts, follow_ups, notifications) |
| IV-2 | Schema alignment verify | LOW | 2h | models/ match schema_all.sql columns |
| IV-3 | Dashboard expansion | LOW | 2h | Query across tất cả populated tables |

### TỔNG EFFORT

| Nhóm | Items | Effort |
|-------|-------|--------|
| I: Cross-cutting | 8 | ~21.5h |
| II: Frontend | 1 | ~3h |
| III: Functional | 7 | ~25h |
| IV: Quality | 3 | ~16h |
| **TỔNG** | **19** | **~65.5h** |

---

## 3. CHI TIẾT THIẾT KẾ

### I-1: Per-User Identity

```python
# auth.py — thêm UserContext
@dataclass
class UserContext:
    key_tier: str          # "ADMIN" | "MANAGER" | "VIEWER"
    user_id: Optional[str] # UUID from sale_user_roles
    user_email: Optional[str]
    user_name: Optional[str]
    department: Optional[str]

async def get_current_user(request: Request) -> UserContext:
    key = request.headers.get("X-API-Key", "")
    tier = _resolve_tier(key)
    user_info = _resolve_user(key)  # lookup sale_user_roles WHERE api_key = ?
    return UserContext(key_tier=tier, user_id=user_info.get("user_id"), ...)
```

Migration: thêm cột `api_key TEXT` vào `sale_user_roles`. Seed API keys cho 3-5 users. Grep `changed_by=None` → thay bằng `changed_by=user.user_id`.

### I-2: Global Exception Handler

```python
# errors.py
class SalePlatformError(Exception):
    def __init__(self, status_code: int, code: str, message: str): ...

class EntityNotFoundError(SalePlatformError):
    def __init__(self, entity: str, entity_id: str):
        super().__init__(404, "NOT_FOUND", f"{entity} '{entity_id}' not found")

class InvalidTransitionError(SalePlatformError):
    def __init__(self, entity, current, target, allowed):
        super().__init__(422, "INVALID_TRANSITION", ...)

class DuplicateError(SalePlatformError):
    def __init__(self, entity, field, value):
        super().__init__(409, "DUPLICATE", ...)

# main.py
@app.exception_handler(SalePlatformError)
async def sale_error_handler(request, exc):
    return JSONResponse(status_code=exc.status_code,
        content={"error": True, "code": exc.code, "message": exc.message})

@app.exception_handler(Exception)
async def unhandled_error_handler(request, exc):
    logger.exception("unhandled_error", path=request.url.path)
    return JSONResponse(status_code=500,
        content={"error": True, "code": "INTERNAL_ERROR", "message": "An unexpected error occurred."})
```

### I-4: Enums (models/enums.py)

```python
from enum import Enum

class OpportunityStage(str, Enum):
    PROSPECT = "PROSPECT"; CONTACTED = "CONTACTED"; RFQ_RECEIVED = "RFQ_RECEIVED"
    COSTING = "COSTING"; QUOTED = "QUOTED"; NEGOTIATION = "NEGOTIATION"
    WON = "WON"; LOST = "LOST"; IN_PROGRESS = "IN_PROGRESS"

class TaskStatus(str, Enum):
    PENDING = "PENDING"; IN_PROGRESS = "IN_PROGRESS"; COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"; CANCELLED = "CANCELLED"

class EmailType(str, Enum):
    RFQ = "RFQ"; TECHNICAL = "TECHNICAL"; NEGOTIATION = "NEGOTIATION"
    CONTRACT = "CONTRACT"; PAYMENT = "PAYMENT"; FOLLOWUP = "FOLLOWUP"
    INTERNAL = "INTERNAL"; VENDOR = "VENDOR"; COMPLAINT = "COMPLAINT"; GENERAL = "GENERAL"

class QuotationStatus(str, Enum):
    DRAFT = "DRAFT"; SENT = "SENT"; NEGOTIATION = "NEGOTIATION"
    WON = "WON"; LOST = "LOST"; EXPIRED = "EXPIRED"

class FollowUpType(str, Enum):
    CALL = "CALL"; EMAIL = "EMAIL"; VISIT = "VISIT"; MEETING = "MEETING"

class NotificationType(str, Enum):
    SLA_BREACH = "SLA_BREACH"; STALE_DEAL = "STALE_DEAL"; FOLLOWUP_DUE = "FOLLOWUP_DUE"
    QUOTATION_EXPIRING = "QUOTATION_EXPIRING"; TASK_ASSIGNED = "TASK_ASSIGNED"; ESCALATION = "ESCALATION"

class CommissionStatus(str, Enum):
    CALCULATED = "CALCULATED"; APPROVED = "APPROVED"; PAID = "PAID"
```

### I-7: DB Dialect Helpers

```python
# database.py
def now_expr() -> str:
    return "NOW()" if config.DB_TYPE == "postgresql" else "datetime('now')"

def date_diff_expr(column: str, days: int) -> str:
    if config.DB_TYPE == "postgresql":
        return f"{column} < NOW() - INTERVAL '{days} days'"
    return f"{column} < datetime('now', '-{days} days')"

def date_today_expr() -> str:
    return "CURRENT_DATE" if config.DB_TYPE == "postgresql" else "date('now')"
```

### I-8: Async DB Wrappers

```python
# database.py
from concurrent.futures import ThreadPoolExecutor
_db_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="db")

async def async_query(sql: str, params: tuple = ()) -> list[dict]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_db_executor, query, sql, params)

async def async_execute(sql: str, params: tuple = ()) -> int:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_db_executor, execute, sql, params)
```

### III-1: Activity Timeline

```
GET /api/v1/customers/{id}/timeline?limit=50
  Logic: UNION query across:
    - sale_customer_interactions (type, notes, created_at)
    - sale_emails WHERE customer_id (subject, sent_date)
    - sale_quotation_history WHERE customer_id (project_name, status, created_at)
    - sale_active_contracts WHERE customer_id (contract_no, status, start_date)
  ORDER BY date DESC
  Response: [{ event_type, title, description, date, entity_id }]
```

### III-2: My Dashboard

```
GET /api/v1/dashboard/my    (user resolved from get_current_user)
  Response: {
    my_tasks: { total, overdue, in_progress, completed_this_week },
    my_pipeline: { deals, total_value, stages: [...] },
    my_follow_ups: { today, overdue, this_week },
    my_recent_activities: [ last 10 ],
    my_notifications: { unread_count }
  }
```

---

## 4. QUY TẮC BẮT BUỘC (20 rules — hợp nhất từ 5 nguồn)

### Rules 1-15 (từ CLAUDE.md + TEAM_RULES + SYSTEM_DESIGN + ADR-001)

1. KHÔNG modify existing tables — chỉ CREATE TABLE / ADD COLUMN
2. Mọi import PHẢI log vào sale_import_log
3. SQLite types: TEXT cho UUID/datetime/JSON, INTEGER cho boolean
4. Dùng query() cho reads, execute() cho writes (database.py helper)
5. Auth: Depends(require_auth) read, Depends(require_write) write
6. Naming: tables sale_*, indexes idx_{short}_{col}, UUID primary keys
7. Gmail tokens: stored per-mailbox, KHÔNG hardcode
8. PM integration: KHÔNG auto-send — luôn DRAFT
9. Logging: structlog.get_logger() — KHÔNG print()
10. State transitions: validate_*_transition() trước status changes
11. Financial changes: audit-log qua services/audit.py
12. Giao tiếp ibshi1 CHỈ qua REST API — KHÔNG direct DB
13. Python code PHẢI có type hints, Pydantic validation
14. LUÔN đọc schema_all.sql trước khi query
15. Query bằng Python sqlite3 module — KHÔNG dùng sqlite3 CLI

### Rules 16-20 (từ CROSS_CUTTING_DESIGN)

16. KHÔNG define Pydantic model inline trong router — import từ models/
17. TẤT CẢ status/stage/type dùng Enum (models/enums.py)
18. TẤT CẢ list endpoints dùng standard pagination {total, items, limit, offset}
19. TẤT CẢ write endpoints pass user_id vào audit_log changed_by
20. TẤT CẢ date SQL dùng dialect helpers (now_expr, date_diff_expr)

---

## 5. LỆNH CHO CLAUDE CODE

**Copy block dưới đây paste vào Claude Code:**

```
Đọc CLAUDE.md và UNIFIED_CLAUDE_CODE_COMMAND.md trước khi code.

## CONTEXT
Sale Platform v4 prototype: 25 routers, 90+ endpoints, auth applied ở router level.
Cần fix 19 vấn đề chia 4 nhóm. Fix theo thứ tự dưới đây (cross-cutting TRƯỚC).

## QUY TẮC BẮT BUỘC (tóm tắt — chi tiết xem UNIFIED_CLAUDE_CODE_COMMAND.md Section 4)
1-15: Giữ nguyên rules từ CLAUDE.md
16: KHÔNG define Pydantic model inline — import từ models/
17: Dùng Enum cho status/stage/type (models/enums.py)
18: Standard pagination {total, items, limit, offset}
19: Write endpoints pass user_id vào audit_log changed_by
20: Date SQL dùng dialect helpers

## BƯỚC 0: Rebuild DB + Verify
cd sql_import/ && python build_db.py && cd ..
Verify: 32 tables, ~6,700 records, 0 errors.

## BƯỚC 1: Global Exception Handler (I-2)
Tạo errors.py:
- SalePlatformError(status_code, code, message)
- EntityNotFoundError(entity, entity_id) → 404
- InvalidTransitionError(entity, current, target, allowed) → 422
- DuplicateError(entity, field, value) → 409

Thêm vào main.py:
- @app.exception_handler(SalePlatformError) → JSON {error: true, code, message}
- @app.exception_handler(Exception) → log + JSON {error: true, code: "INTERNAL_ERROR"}

## BƯỚC 2: User Identity (I-1) — CRITICAL
auth.py:
- Tạo UserContext dataclass (key_tier, user_id, user_email, user_name, department)
- Tạo get_current_user(request) → lookup sale_user_roles WHERE api_key = ?
- ALTER TABLE sale_user_roles ADD COLUMN api_key TEXT (trong schema_all.sql, chỉ ADD COLUMN)
- Seed 3 users với API keys:
  admin@ibs.com.vn / ADMIN / api_key=admin-key-xxx
  sale@ibs.com.vn / MANAGER / api_key=sale-key-xxx
  viewer@ibs.com.vn / VIEWER / api_key=viewer-key-xxx

services/audit.py:
- audit_log() nhận user_id parameter
- Grep tất cả changed_by=None → thay bằng changed_by=user.user_id

routers có write operations (POST/PATCH):
- Thêm user: UserContext = Depends(get_current_user)
- Pass user.user_id vào audit_log

## BƯỚC 3: Thread-Safe Pool (I-3)
database.py: SimpleConnectionPool → ThreadedConnectionPool (1 line change)

## BƯỚC 4: Enum Validation (I-4)
Tạo models/enums.py với:
OpportunityStage, TaskStatus, EmailType, QuotationStatus, FollowUpType,
NotificationType, CommissionStatus

Import vào models/*.py. Update Pydantic fields: Optional[str] → Optional[EnumType].

## BƯỚC 5: Models Consolidation Pilot (I-5)
Update models/customer.py: CustomerBase, CustomerCreate, CustomerUpdate, CustomerResponse
Update models/quotation.py: QuotationBase, QuotationCreate, QuotationUpdate, QuotationResponse
Refactor routers/customers.py + routers/quotations.py → import từ models/
Xóa inline Pydantic classes trong 2 routers đó.
Các routers khác: giữ nguyên (Toàn migrate dần v5.x).

## BƯỚC 6: Pagination Fix (I-6)
Fix 4 routers không đồng nhất:
- templates.py /email list → thêm limit/offset, return {total, items, limit, offset}
- follow_ups.py /overdue → thêm offset, return standard format
- commissions.py /by-salesperson → thêm pagination
- reports.py /audit-log → thêm limit/offset
Ngoại lệ OK: search.py (per_type_limit), board endpoints (grouped data).

## BƯỚC 7: DB Dialect Helpers (I-7)
database.py thêm:
- now_expr() → "datetime('now')" / "NOW()"
- date_diff_expr(column, days) → dialect-aware comparison
- date_today_expr() → "date('now')" / "CURRENT_DATE"

Grep datetime('now') và date('now') trong workers/ + routers/ → replace với helpers.

## BƯỚC 8: Async DB Wrappers (I-8)
database.py thêm:
- ThreadPoolExecutor(max_workers=4)
- async_query(sql, params) → run_in_executor
- async_execute(sql, params) → run_in_executor
Routers MỚI (bước sau) dùng async versions. Routers CŨ giữ sync (backward compatible).

## BƯỚC 9: Frontend Field Alignment (II-1)
Chạy API: GET /api/v1/customers?limit=1 → note exact field names.
Grep trong static/*.html và fix:
- customer_code → code
- company_name → name
- o.title → o.project_name
- estimated_value → amount
- Verify tất cả fetch() calls match API response fields
Test: mở browser, verify data hiển thị đúng.

## BƯỚC 10: Functional Gaps — Activity Timeline (III-1)
Thêm endpoint GET /api/v1/customers/{id}/timeline vào routers/customers.py
UNION query: interactions + emails + quotations + contracts ORDER BY date DESC
Response: [{ event_type, title, description, date, entity_id }]

## BƯỚC 11: Functional Gaps — My Dashboard (III-2)
Thêm/verify endpoint GET /api/v1/dashboard/my trong routers/dashboard.py
Dùng get_current_user → filter by user_id
Response: { my_tasks, my_pipeline, my_follow_ups, my_recent_activities, my_notifications }

## BƯỚC 12: Functional Gaps — Soft Delete (III-7)
Thêm DELETE endpoints (require_admin):
- DELETE /api/v1/customers/{id} → SET status='DELETED'
- DELETE /api/v1/contacts/{id} → SET status='DELETED'
- DELETE /api/v1/opportunities/{id} → SET stage='DELETED'
KHÔNG xóa record thật. Audit-log.

## BƯỚC 13: Functional Gaps — Duplicate Detection (III-5)
Trong POST /customers và POST /contacts:
- Trước INSERT, check: SELECT * FROM sale_customers WHERE LOWER(name) = LOWER(?)
- Nếu tìm thấy → raise DuplicateError(...)
- Cho contacts: check email unique per customer

## BƯỚC 14: Schema Alignment Verify (IV-2)
Đọc sql_import/schema_all.sql. Với TỪNG file trong models/:
- So sánh column names + types
- Fix mismatches, thêm Optional[] cho nullable
Verify database.py references schema_all.sql (không schema.sql cũ).

## BƯỚC 15: Dashboard Expansion (IV-3)
GET /api/v1/dashboard/summary mở rộng:
- total_customers, total_contacts, total_opportunities
- pipeline_by_stage, pipeline_value_weighted
- total_quotations, quotation_win_rate (won/total)
- active_contract_value (SUM from sale_active_contracts)
- total_interactions, total_emails, market_signals_count
- total_follow_ups, overdue_follow_ups

## BƯỚC 16: Test Expansion (IV-1)
Thêm 5 test files:
- tests/test_quotations.py (state machine: DRAFT→SENT→WON, invalid transition → 422)
- tests/test_contracts.py (CRUD + milestones + settlements)
- tests/test_contacts.py (CRUD + primary demotion)
- tests/test_follow_ups.py (CRUD + overdue + reschedule)
- tests/test_notifications.py (count + mark-read)
Mỗi file: test_requires_auth, test_list, test_create, test_invalid_body.

## BƯỚC 17: End-to-End Verify
python main.py
Verify trên http://localhost:8767/docs:
- GET /health → 200
- GET /api/v1/customers (no key) → 401
- GET /api/v1/customers (with key) → 200 + ~992 records
- GET /api/v1/auth/me → user info with name + email
- POST /api/v1/customers (duplicate name) → 409 DuplicateError
- GET /api/v1/customers/{id}/timeline → events sorted by date
- GET /api/v1/dashboard/my → personal stats
- GET /api/v1/dashboard/summary → all counts > 0
- Invalid stage transition → 422 InvalidTransitionError
- Mở static/index.html → verify data hiển thị đúng (fields match)

NẾU fail → fix trước khi commit.

## BƯỚC 18: Commit
git add -A
git commit -m "Unified fix: exception handler, user identity, enums, pagination, frontend align, dialect helpers, thread-safe pool, async wrappers, timeline, my-dashboard, soft-delete, duplicate-detection, tests"
```

---

## 6. PHASE 2 — SAU KHI BƯỚC 1-18 XONG

| Feature | Effort | Priority | Ghi chú |
|---------|--------|----------|---------|
| Report export XLSX/PDF (III-3) | 6h | HIGH | openpyxl + weasyprint |
| Email compose flow (III-4) | 6h | MEDIUM | Gmail API DRAFT → review → send |
| Dashboard extended filters (III-6) | 3h | MEDIUM | Date range, assigned_to, product_group |
| Models consolidation full (CC-6 mở rộng) | 4h | LOW | Migrate 23 routers còn lại |
| Test coverage 80%+ | 8h | LOW | 10 router test files còn lại |

---

## 7. REFERENCE — DOCUMENT RELATIONSHIP

```
CLAUDE.md                          → Rules + architecture (ĐỌC ĐẦU TIÊN)
UNIFIED_CLAUDE_CODE_COMMAND.md     → Lệnh hợp nhất DUY NHẤT (ĐÂY LÀ FILE CHÍNH)
├── merges: CROSS_CUTTING_DESIGN.md       (10 patterns đồng bộ)
├── merges: FUNCTIONAL_COMPLETENESS_AUDIT.md (gap analysis, updated 03/05)
└── merges: SALE_PLATFORM_MASTER_FIX.md   (schema alignment + rules tổng hợp)
```

**Khi Claude Code hỏi:** trỏ về file này. Các document khác là reference, KHÔNG chạy riêng.
