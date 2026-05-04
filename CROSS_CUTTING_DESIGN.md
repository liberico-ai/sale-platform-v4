# SALE PLATFORM — CROSS-CUTTING DESIGN (Đồng Bộ Xuyên Suốt)

> **Date:** 03/05/2026
> **Source:** Audit từ GitHub repo `liberico-ai/sale-platform-v4`
> **Mục đích:** Thiết kế các tính năng xuyên suốt (cross-cutting) đồng bộ cho toàn bộ 25 routers
> **Đã audit:** 25 routers, 90+ endpoints, 13 models, 4 workers, 8 services, 6 frontend pages, tests, Docker

---

## 0. HIỆN TRẠNG GITHUB vs GDRIVE

| Metric | GDrive (cũ) | GitHub (thực tế) |
|--------|-------------|-------------------|
| Routers | 14 | **25** (+auth_router, follow_ups, files, notifications, search, inter_dept, commissions, reports, templates, io_router, ROUTER_MANIFEST) |
| Endpoints | ~63 | **~90+** |
| Auth applied | 4/63 (6%) | **Tất cả routers** qua main.py `dependencies=auth_dep` |
| Frontend | 0 | **6 HTML pages** (index, sale_dashboard, email-hub, task-board, pipeline, project-board) |
| Tests | 0 | **10 test flows, ~22 functions** |
| Docker | 0 | **Dockerfile + docker-compose.yml + deploy.yml** |
| Workers | 3 | **4** (+followup_worker) |
| Services | 6 | **7** (+notify.py) |

**Kết luận:** Code trên GitHub đã implement phần lớn các tính năng trong FUNCTIONAL_COMPLETENESS_AUDIT.md. Tuy nhiên, 10 vấn đề cross-cutting cần fix ĐỒNG BỘ trước khi team dùng được.

---

## 1. TOP 10 VẤN ĐỀ CROSS-CUTTING

| # | Vấn đề | Severity | Impact |
|---|--------|----------|--------|
| CC-1 | Không có per-user identity trong auth | CRITICAL | Audit trail trống changed_by, không biết ai làm gì |
| CC-2 | Sync DB trên async framework | HIGH | DB calls block event loop, chậm dưới load |
| CC-3 | Không có global exception handler | HIGH | Unhandled errors → raw 500 |
| CC-4 | Frontend field names sai vs API | HIGH | SPA bị broken hoàn toàn |
| CC-5 | Pagination không đồng nhất | MEDIUM | 6 routers pagination khác pattern chung |
| CC-6 | Pydantic models trong models/ KHÔNG ĐƯỢC SỬ DỤNG | MEDIUM | Routers tự define inline, duplicate code |
| CC-7 | Không có enum validation | MEDIUM | Invalid status/stage/type pass validation |
| CC-8 | Workers dùng SQLite SQL | MEDIUM | Sẽ break khi chuyển PostgreSQL |
| CC-9 | SimpleConnectionPool không thread-safe | HIGH | Corrupt data dưới concurrent PG requests |
| CC-10 | ~60% routers chưa có tests | MEDIUM | Regression risk cao |

---

## 2. THIẾT KẾ ĐỒNG BỘ — 10 CROSS-CUTTING PATTERNS

### CC-1: User Identity trong Auth

**Vấn đề:** Auth hiện tại chỉ trả tier (ADMIN/MANAGER/VIEWER), không biết AI LÀ AI. Mọi audit_log.changed_by = None.

**Design:**

```python
# auth.py — thêm UserContext dataclass

from dataclasses import dataclass
from typing import Optional

@dataclass
class UserContext:
    """Authenticated user context, available in every endpoint."""
    key_tier: str          # "ADMIN" | "MANAGER" | "VIEWER"
    user_id: Optional[str] # UUID from sale_user_roles (nullable for API-only keys)
    user_email: Optional[str]
    user_name: Optional[str]
    department: Optional[str]

# API Key → User mapping (config hoặc DB lookup)
# config.py thêm:
API_KEY_USER_MAP = {
    "admin-key-xxx": {"user_id": "uuid-admin", "email": "admin@ibs.com.vn", "name": "Admin"},
    "sale-key-xxx":  {"user_id": "uuid-sale",  "email": "sale@ibs.com.vn",  "name": "Sale Manager"},
}

# Hoặc lookup từ sale_user_roles WHERE api_key = ?
# (thêm cột api_key vào sale_user_roles)

async def get_current_user(request: Request) -> UserContext:
    """Resolve API key → UserContext. Use as Depends()."""
    key = request.headers.get("X-API-Key", "")
    tier = _resolve_tier(key)  # existing logic
    user_info = _resolve_user(key)  # NEW: lookup user
    return UserContext(
        key_tier=tier,
        user_id=user_info.get("user_id"),
        user_email=user_info.get("email"),
        user_name=user_info.get("name"),
        department=user_info.get("department"),
    )

# Sử dụng trong routers:
async def create_opportunity(
    body: OpportunityCreate,
    user: UserContext = Depends(get_current_user),  # NEW
):
    # ... create logic ...
    audit_log(entity="opportunity", entity_id=opp_id,
              changed_by=user.user_id,  # ← Bây giờ biết AI thay đổi
              field="status", old_value=None, new_value="PROSPECT")
```

**Migration:**
1. Thêm cột `api_key TEXT` vào `sale_user_roles`
2. Seed API keys cho 3-5 users
3. Thêm `get_current_user` dependency
4. Grep tất cả `changed_by=None` → thay bằng `changed_by=user.user_id`
5. notifications.py: bỏ duplicate X-API-Key parsing, dùng `get_current_user`

**Effort:** 4h | **Impact:** Tất cả routers + audit.py + notifications.py

---

### CC-2: Async DB Layer

**Vấn đề:** FastAPI là async framework, nhưng mọi DB call là sync (sqlite3/psycopg2). Dưới load, DB calls block event loop.

**Design — Phase approach:**

```
Phase 1 (Bây giờ): Dùng run_in_executor() wrapper → không block event loop
Phase 2 (Khi scale): Chuyển sang aiosqlite + asyncpg
```

```python
# database.py — thêm async wrappers

import asyncio
from concurrent.futures import ThreadPoolExecutor

_db_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="db")

async def async_query(sql: str, params: tuple = ()) -> list[dict]:
    """Non-blocking query wrapper."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_db_executor, query, sql, params)

async def async_execute(sql: str, params: tuple = ()) -> int:
    """Non-blocking execute wrapper."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_db_executor, execute, sql, params)
```

**Migration:**
1. Thêm `async_query()` + `async_execute()` vào database.py
2. Routers mới dùng async versions
3. Routers cũ chuyển dần (không cần 1 lần — backward compatible)

**Effort:** 2h wrapper + 8h migrate routers | **Impact:** database.py + tất cả routers

---

### CC-3: Global Exception Handler

**Vấn đề:** Unhandled errors → raw 500. Không có structured error response.

**Design:**

```python
# main.py — thêm exception handlers

from fastapi import Request
from fastapi.responses import JSONResponse

class SalePlatformError(Exception):
    """Base exception for Sale Platform."""
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message

class EntityNotFoundError(SalePlatformError):
    def __init__(self, entity: str, entity_id: str):
        super().__init__(404, "NOT_FOUND", f"{entity} '{entity_id}' not found")

class InvalidTransitionError(SalePlatformError):
    def __init__(self, entity: str, current: str, target: str, allowed: list):
        super().__init__(422, "INVALID_TRANSITION",
            f"Cannot transition {entity} from {current} to {target}. Allowed: {allowed}")

class DuplicateError(SalePlatformError):
    def __init__(self, entity: str, field: str, value: str):
        super().__init__(409, "DUPLICATE", f"{entity} with {field}='{value}' already exists")


# Error envelope — ĐỒNG NHẤT cho tất cả errors
@app.exception_handler(SalePlatformError)
async def sale_error_handler(request: Request, exc: SalePlatformError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "code": exc.code,
            "message": exc.message,
        }
    )

@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    logger.exception("unhandled_error", path=request.url.path, error=str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred. Please try again.",
        }
    )

# Success envelope — optional, cho consistency
# (Hiện tại mỗi router trả format khác nhau, nhưng ít nhất list endpoints đã consistent)
```

**Migration:**
1. Tạo `errors.py` với exception classes
2. Thêm handlers vào main.py
3. Dần chuyển routers từ `raise HTTPException(...)` → `raise EntityNotFoundError(...)`
4. Backward compatible — HTTPException vẫn hoạt động

**Effort:** 3h | **Impact:** main.py + errors.py + dần migrate routers

---

### CC-4: Frontend Field Name Alignment

**Vấn đề:** Frontend gọi `c.customer_code` nhưng API trả `c.code`. Frontend gọi `c.company_name` nhưng API trả `c.name`. Frontend gọi `o.title` nhưng API trả `o.project_name`. → SPA broken.

**Design:**

```
Nguyên tắc: API là source of truth. Frontend PHẢI match API field names.
```

**Field mapping cần fix (trong static/*.html):**

| Frontend (SAI) | API (ĐÚNG) | File |
|----------------|-----------|------|
| c.customer_code | c.code | index.html |
| c.company_name | c.name | index.html |
| o.title | o.project_name | index.html, pipeline.html |
| o.estimated_value | o.amount | index.html |
| o.customer_id (POST body) | Cần verify | index.html |

**Migration:**
1. Chạy API: `GET /api/v1/customers?limit=1` → note exact field names
2. Grep all `\.customer_code\b`, `\.company_name\b`, `\.title\b` trong static/
3. Replace với đúng field names
4. Test: mở browser → verify data hiển thị đúng

**Effort:** 3h | **Impact:** 6 HTML files trong static/

---

### CC-5: Pagination Đồng Nhất

**Vấn đề:** 19/25 routers dùng `{total, items, limit, offset}`, nhưng 6 routers khác pattern:
- templates.py: `{items, count}` (no pagination)
- follow_ups.py /overdue: `{items, count}` (no offset)
- commissions.py /by-salesperson: `{items, count}`
- inter_dept.py /board: trả tất cả (no pagination)
- search.py: dùng `per_type_limit` riêng
- reports.py /audit-log: trả tất cả

**Design — Standard pagination pattern:**

```python
# Tạo utility function trong database.py hoặc utils.py

from pydantic import BaseModel
from typing import Generic, TypeVar, List
from fastapi import Query

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    items: List[T]
    limit: int
    offset: int

# Standard query params — import vào MỌI router
def pagination_params(
    limit: int = Query(50, ge=1, le=200, description="Max items per page"),
    offset: int = Query(0, ge=0, description="Items to skip"),
):
    return {"limit": limit, "offset": offset}

# Sử dụng trong router:
@router.get("/follow-ups/overdue")
async def list_overdue(page=Depends(pagination_params)):
    # ... query with LIMIT {page['limit']} OFFSET {page['offset']} ...
    return {"total": count, "items": rows, "limit": page["limit"], "offset": page["offset"]}
```

**Ngoại lệ hợp lệ:**
- search.py: dùng `per_type_limit` OK vì search khác nature
- /board endpoints (tasks, inter_dept): trả grouped data, pagination không áp dụng

**Migration:** Fix 4 routers (templates, follow_ups/overdue, commissions/by-salesperson, reports/audit-log)

**Effort:** 2h | **Impact:** 4 routers

---

### CC-6: Pydantic Models Consolidation

**Vấn đề:** `models/` directory tồn tại 13 files nhưng routers KHÔNG import từ đây — mỗi router tự define inline Pydantic models. Duplicate code, không consistent.

**Design:**

```
Nguyên tắc:
1. models/ là SINGLE SOURCE OF TRUTH cho Pydantic schemas
2. Mỗi entity có 3 models: {Entity}Base, {Entity}Create, {Entity}Response
3. Routers import từ models/ — KHÔNG define inline
```

```python
# models/customer.py — CHUẨN

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class CustomerStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = None
    region: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    business_description: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass  # Inherits all fields, name is required

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = None
    region: Optional[str] = None
    status: Optional[CustomerStatus] = None
    # ... all optional for partial update

class CustomerResponse(CustomerBase):
    id: str
    status: CustomerStatus = CustomerStatus.ACTIVE
    created_at: str
    updated_at: str

# Routers import:
# from models.customer import CustomerCreate, CustomerUpdate, CustomerResponse
```

**Migration:**
1. Update models/ files theo chuẩn trên (Base/Create/Update/Response)
2. Thêm Enum classes cho status, stage, type
3. Refactor routers: xóa inline models, import từ models/
4. Test: Swagger UI vẫn hiển thị đúng schemas

**Effort:** 8h | **Impact:** 13 model files + 25 routers

---

### CC-7: Enum Validation

**Vấn đề:** `status`, `stage`, `priority`, `email_type`, `follow_up_type` — tất cả là `Optional[str]`, bất kỳ string nào đều pass.

**Design:**

```python
# models/enums.py — TẤT CẢ enums tập trung 1 file

from enum import Enum

class OpportunityStage(str, Enum):
    PROSPECT = "PROSPECT"
    CONTACTED = "CONTACTED"
    RFQ_RECEIVED = "RFQ_RECEIVED"
    COSTING = "COSTING"
    QUOTED = "QUOTED"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    LOST = "LOST"
    IN_PROGRESS = "IN_PROGRESS"

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"

class EmailType(str, Enum):
    RFQ = "RFQ"
    TECHNICAL = "TECHNICAL"
    NEGOTIATION = "NEGOTIATION"
    CONTRACT = "CONTRACT"
    PAYMENT = "PAYMENT"
    FOLLOWUP = "FOLLOWUP"
    INTERNAL = "INTERNAL"
    VENDOR = "VENDOR"
    COMPLAINT = "COMPLAINT"
    GENERAL = "GENERAL"

class QuotationStatus(str, Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    LOST = "LOST"
    EXPIRED = "EXPIRED"

class FollowUpType(str, Enum):
    CALL = "CALL"
    EMAIL = "EMAIL"
    VISIT = "VISIT"
    MEETING = "MEETING"

class NotificationType(str, Enum):
    SLA_BREACH = "SLA_BREACH"
    STALE_DEAL = "STALE_DEAL"
    FOLLOWUP_DUE = "FOLLOWUP_DUE"
    QUOTATION_EXPIRING = "QUOTATION_EXPIRING"
    TASK_ASSIGNED = "TASK_ASSIGNED"
    ESCALATION = "ESCALATION"

class CommissionStatus(str, Enum):
    CALCULATED = "CALCULATED"
    APPROVED = "APPROVED"
    PAID = "PAID"

# Dùng trong Pydantic models:
# stage: OpportunityStage = OpportunityStage.PROSPECT
# email_type: Optional[EmailType] = None
```

**Migration:**
1. Tạo `models/enums.py`
2. Import enums vào models/ files
3. Update routers nơi validate inline (state_machine.py vẫn giữ transition logic riêng)
4. FastAPI auto-generates dropdown trong Swagger cho Enum fields

**Effort:** 3h | **Impact:** models/enums.py + models/*.py + Swagger docs cải thiện

---

### CC-8: DB Dialect Abstraction

**Vấn đề:** Workers dùng SQLite-specific SQL (`datetime('now')`, `date('now')`). Sẽ break trên PostgreSQL.

**Design:**

```python
# database.py — thêm dialect helpers

def now_expr() -> str:
    """SQL expression for current timestamp, dialect-aware."""
    if config.DB_TYPE == "postgresql":
        return "NOW()"
    return "datetime('now')"

def date_diff_expr(column: str, days: int) -> str:
    """SQL expression for date comparison, dialect-aware."""
    if config.DB_TYPE == "postgresql":
        return f"{column} < NOW() - INTERVAL '{days} days'"
    return f"{column} < datetime('now', '-{days} days')"

def date_today_expr() -> str:
    if config.DB_TYPE == "postgresql":
        return "CURRENT_DATE"
    return "date('now')"

# Workers sử dụng:
# from database import now_expr, date_diff_expr
# sql = f"SELECT * FROM sale_tasks WHERE due_date < {now_expr()}"
# instead of:
# sql = "SELECT * FROM sale_tasks WHERE due_date < datetime('now')"
```

**Migration:**
1. Thêm helpers vào database.py
2. Grep `datetime('now')` và `date('now')` trong workers/ và routers/
3. Replace với helper functions
4. Test cả SQLite và PostgreSQL

**Effort:** 3h | **Impact:** database.py + 4 workers + routers dùng date functions

---

### CC-9: Thread-Safe Connection Pool

**Vấn đề:** `psycopg2.SimpleConnectionPool` KHÔNG thread-safe. Uvicorn multiple workers sẽ corrupt connections.

**Design:**

```python
# database.py — PostgreSQL connection fix

import psycopg2.pool

# TRƯỚC (SAI):
# _pg_pool = psycopg2.pool.SimpleConnectionPool(minconn=2, maxconn=10, dsn=...)

# SAU (ĐÚNG):
_pg_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=2,
    maxconn=int(os.getenv("PG_POOL_MAX", "10")),
    dsn=config.PG_DSN
)

# Hoặc Phase 2: chuyển sang asyncpg
```

**Migration:** 1 dòng thay đổi trong database.py. Test với `uvicorn --workers 4`.

**Effort:** 0.5h | **Impact:** database.py

---

### CC-10: Test Coverage Expansion

**Vấn đề:** 10/25 routers có tests (~40%). 15 routers untested.

**Design — Test matrix:**

```
TESTED (giữ nguyên):
✅ health, customers, opportunities, tasks, dashboard, mailboxes, users, files, auth

CẦN THÊM:
❌ contacts         → test CRUD + primary demotion
❌ quotations       → test state machine (DRAFT→SENT→WON)
❌ contracts        → test CRUD + milestones + settlements
❌ interactions     → test create + filters
❌ intelligence     → test list + filters
❌ emails           → test classify + create-task-from-email
❌ follow_ups       → test CRUD + overdue + auto-reschedule
❌ notifications    → test count + mark-read
❌ search           → test multi-entity search
❌ commissions      → test calculate + state machine
❌ inter_dept       → test board + escalate
❌ reports          → test config CRUD + audit-log
❌ templates        → test quote + email templates
❌ io_router        → test CSV import/export + dry_run
❌ pm_integration   → test draft-reply + proxy
```

**Test pattern chuẩn cho MỌI router:**

```python
# tests/test_{router}.py

def test_list_requires_auth(client):
    """GET without key → 401."""
    resp = client.get("/api/v1/{entity}")
    assert resp.status_code == 401

def test_list_with_auth(client, admin_key):
    """GET with key → 200 + paginated response."""
    resp = client.get("/api/v1/{entity}", headers={"X-API-Key": admin_key})
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "items" in data

def test_create_requires_write(client, viewer_key):
    """POST with viewer key → 403."""
    resp = client.post("/api/v1/{entity}", headers={"X-API-Key": viewer_key}, json={...})
    assert resp.status_code == 403

def test_create_happy_path(client, admin_key):
    """POST with valid body → 201."""
    ...

def test_create_invalid_body(client, admin_key):
    """POST with invalid body → 422."""
    ...
```

**Effort:** 12h | **Impact:** tests/ directory

---

## 3. LỆNH CHO CLAUDE CODE — CROSS-CUTTING FIX

```
Đọc CLAUDE.md và CROSS_CUTTING_DESIGN.md trước.

## CONTEXT
GitHub repo liberico-ai/sale-platform-v4 có 25 routers, 90+ endpoints.
Auth đã applied ở router level trong main.py.
Nhưng 10 cross-cutting issues cần fix ĐỒNG BỘ.

## PRIORITY ORDER (fix theo thứ tự)

### FIX 1: Global Exception Handler (CC-3)
Tạo file errors.py:
- SalePlatformError(status_code, code, message)
- EntityNotFoundError(entity, entity_id)
- InvalidTransitionError(entity, current, target, allowed)
- DuplicateError(entity, field, value)

Thêm vào main.py:
- @app.exception_handler(SalePlatformError) → JSON {error: true, code, message}
- @app.exception_handler(Exception) → JSON {error: true, code: "INTERNAL_ERROR"} + log

### FIX 2: User Identity (CC-1)
Thêm vào auth.py:
- UserContext dataclass (key_tier, user_id, user_email, user_name, department)
- get_current_user(request) dependency → resolve API key → UserContext
- Thêm cột api_key TEXT vào sale_user_roles (ALTER TABLE ADD COLUMN)

Cập nhật services/audit.py:
- audit_log() nhận user_id parameter thay vì None

Cập nhật routers có write operations:
- Thêm user: UserContext = Depends(get_current_user) vào POST/PATCH functions
- Pass user.user_id vào audit_log changed_by

Xóa duplicate X-API-Key parsing trong routers/notifications.py.

### FIX 3: Enum Validation (CC-7)
Tạo models/enums.py với tất cả enums:
OpportunityStage, TaskStatus, EmailType, QuotationStatus, FollowUpType,
NotificationType, CommissionStatus, ContractStatus, InterDeptPriority

Import vào models/*.py files. Update Pydantic fields: str → Enum.

### FIX 4: Pydantic Models Consolidation (CC-6)
Update models/ files: Base/Create/Update/Response pattern.
Import enums từ models/enums.py.
Refactor 1-2 routers pilot (customers, quotations) → import từ models/.
Các routers khác: để Toàn migrate dần trong v5.x.

### FIX 5: Pagination Consistency (CC-5)
Fix 4 routers:
- templates.py /email list → thêm limit/offset, return {total, items, limit, offset}
- follow_ups.py /overdue → thêm offset, return standard format
- commissions.py /by-salesperson → thêm pagination
- reports.py /audit-log → thêm limit/offset

### FIX 6: Frontend Field Alignment (CC-4)
Grep và fix trong static/*.html:
- customer_code → code
- company_name → name
- o.title → o.project_name
- estimated_value → amount
Test: mở browser, verify data hiển thị.

### FIX 7: DB Dialect Helpers (CC-8)
Thêm vào database.py: now_expr(), date_diff_expr(), date_today_expr()
Grep datetime('now') và date('now') trong workers/ + routers/ → replace.

### FIX 8: Thread-Safe Pool (CC-9)
database.py: SimpleConnectionPool → ThreadedConnectionPool (1 line)

### FIX 9: Async DB Wrappers (CC-2)
Thêm async_query() + async_execute() wrappers vào database.py.
Routers mới dùng async. Routers cũ giữ sync (backward compatible).

### FIX 10: Test Expansion (CC-10)
Thêm tests cho 5 critical routers trước:
- test_quotations.py (state machine)
- test_contracts.py (CRUD + milestones)
- test_contacts.py (primary demotion)
- test_follow_ups.py (overdue + reschedule)
- test_notifications.py (count + read)

## QUY TẮC
1-15 rules từ SALE_PLATFORM_MASTER_FIX.md vẫn áp dụng.
Thêm:
16. KHÔNG define Pydantic model inline trong router — import từ models/
17. TẤT CẢ status/stage/type dùng Enum (models/enums.py)
18. TẤT CẢ list endpoints dùng standard pagination {total, items, limit, offset}
19. TẤT CẢ write endpoints pass user_id vào audit_log
20. TẤT CẢ date SQL dùng dialect helpers (now_expr, date_diff_expr)

## COMMIT
git add -A
git commit -m "Cross-cutting fix: exception handler, user identity, enums, pagination, frontend align, dialect helpers, thread-safe pool"
```

---

## 4. TỔNG KẾT — EFFORT VÀ IMPACT

| Fix | Effort | Files changed | Priority |
|-----|--------|---------------|----------|
| CC-3: Exception handler | 3h | 2 new + main.py | P0 |
| CC-1: User identity | 4h | auth.py + audit.py + ~10 routers | P0 |
| CC-7: Enums | 3h | 1 new + 13 models | P1 |
| CC-6: Models consolidation | 8h | 13 models + 2 pilot routers | P1 |
| CC-5: Pagination | 2h | 4 routers | P1 |
| CC-4: Frontend alignment | 3h | 6 HTML files | P1 |
| CC-8: Dialect helpers | 3h | database.py + 4 workers | P2 |
| CC-9: Thread-safe pool | 0.5h | database.py | P2 |
| CC-2: Async wrappers | 2h | database.py | P2 |
| CC-10: Tests | 12h | 5 test files | P2 |
| **TỔNG** | **~40h** | | |

### Relationship với documents trước

```
SALE_PLATFORM_MASTER_FIX.md    → Align code ↔ DB schema (11 bước)
FUNCTIONAL_COMPLETENESS_AUDIT.md → Thêm CRUD + tính năng thiếu (7 phases)
CROSS_CUTTING_DESIGN.md         → Đồng bộ patterns xuyên suốt (10 fixes)  ← BẠN ĐANG ĐÂY
```

**Thứ tự chạy Claude Code:**
1. CROSS_CUTTING_DESIGN (fix patterns trước) → code base consistent
2. FUNCTIONAL_COMPLETENESS_AUDIT (thêm features) → code mới theo đúng patterns
3. MASTER_FIX (nếu chưa chạy) → align schema

Hoặc MERGE tất cả thành 1 lệnh duy nhất (recommended — tránh conflict giữa 3 passes).
