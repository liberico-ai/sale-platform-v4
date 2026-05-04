# SALE PLATFORM — FUNCTIONAL COMPLETENESS AUDIT

> **Date:** 30/04/2026 | **Updated:** 03/05/2026 (GitHub audit correction)
> **Mục đích:** Đánh giá đầy đủ chức năng để team Sale (3-5 người) có thể dùng Platform
> **Đã đọc:** CLAUDE.md v5.1, TEAM_RULES v2.0, Sale Platform CLAUDE.md, ADR-001, schema_all.sql
> **Input từ Chairman:** Quotation = Sale tự gửi, Notification = In-app badge, Users = 3-5 người, Documents = Link NAS

---

## ⚠️ ĐÍNH CHÍNH 03/05/2026

> **Audit ban đầu dựa trên GDrive code (cũ). GitHub repo đã implement nhiều tính năng hơn.**
> Xem **CROSS_CUTTING_DESIGN.md** để biết hiện trạng THỰC TẾ từ GitHub.
> Xem **UNIFIED_CLAUDE_CODE_COMMAND.md** để có lệnh hợp nhất duy nhất cho Claude Code.

| Metric | Audit ban đầu (GDrive) | Thực tế (GitHub) |
|--------|------------------------|-------------------|
| Routers | 14 | **25** |
| Endpoints | ~63 | **~90+** |
| Auth | 4/63 (6%) | **100% qua main.py dependencies** |
| Frontend | 0 | **6 HTML pages** |
| Tests | 0 | **10 flows, 22 functions** |
| Docker | 0 | **Dockerfile + CI/CD** |
| Workers | 4 | **5** (+followup) |
| Services | 4 | **8** (+notify, +pm_bridge) |

**Đã có trên GitHub (KHÔNG CẦN tạo mới):** auth_router, follow_ups, files, notifications, search, inter_dept, commissions, reports, templates, io_router, contacts, quotations, contracts, interactions, intelligence

**CÒN THIẾU thật sự (cần bổ sung):** per-user identity (CC-1), exception handler (CC-3), enum validation (CC-7), frontend field alignment (CC-4), async DB wrappers (CC-2), thread-safe pool (CC-9) — xem CROSS_CUTTING_DESIGN.md

---

## 1. HIỆN TRẠNG CODE (ban đầu — xem đính chính ở trên)

### 1.1 Inventory (GDrive — OUTDATED)
- ~~**14 routers**, **63 endpoints**~~ → GitHub: **25 routers, 90+ endpoints**
- **13 model files** (Pydantic) — nhưng routers KHÔNG import từ models/ (CC-6)
- ~~**4 services**~~ → GitHub: **8 services** (+ notify.py, pm_bridge.py)
- ~~**4 workers**~~ → GitHub: **5 workers** (+ followup_worker.py)
- **32 tables** + 2 views trong DB, ~6,700 records

### 1.2 ~~BÁO ĐỘNG: Auth gần như KHÔNG CÓ~~ → ĐÃ FIX trên GitHub

**GitHub main.py áp dụng auth ở router REGISTRATION level:**
```python
auth_dep = [Depends(require_auth)]    # 19 routers
write_dep = [Depends(require_write)]  # 2 routers (mailboxes, users)
admin_dep = [Depends(require_admin)]  # 1 router (io_router)
```

**Vấn đề CÒN LẠI:** Auth chỉ biết tier (ADMIN/MANAGER/VIEWER), KHÔNG biết user identity → audit trail trống. Xem CC-1 trong CROSS_CUTTING_DESIGN.md.

---

## 2. GAP ANALYSIS — CHỨC NĂNG TIÊU CHUẨN CRM (cập nhật 03/05/2026)

### NHÓM A: CRITICAL — Không có thì không dùng được

| # | Chức năng | GitHub Status | Còn thiếu gì | Effort |
|---|-----------|---------------|---------------|--------|
| A1 | **Auth trên TẤT CẢ endpoints** | ✅ ĐÃ CÓ (main.py dependencies) | Per-user identity (CC-1) | 4h |
| A2 | **Login page** | ⚠️ index.html có nhưng field names sai | Fix field alignment (CC-4) | 3h |
| A3 | **POST /customers** (tạo KH mới) | ✅ ĐÃ CÓ (routers/customers.py) | Verify body validation | 0h |
| A4 | **PATCH /customers/{id}** (sửa KH) | ✅ ĐÃ CÓ | — | 0h |
| A5 | **POST /quotations** (tạo báo giá) | ✅ ĐÃ CÓ (routers/quotations.py) | Verify state machine | 0h |
| A6 | **PATCH /quotations/{id}** | ✅ ĐÃ CÓ | — | 0h |
| A7 | **POST /contracts** (tạo hợp đồng) | ✅ ĐÃ CÓ (routers/contracts.py) | — | 0h |
| A8 | **PATCH /contracts/{id}** | ✅ ĐÃ CÓ | — | 0h |
| A9 | **Frontend** | ⚠️ 6 HTML pages nhưng field names sai vs API | Fix CC-4 | (incl. in CC-4) |
| A10 | **GET /auth/me** | ✅ ĐÃ CÓ (routers/auth_router.py) | — | 0h |

**Subtotal CRITICAL: ~~37h~~ → 7h (chỉ CC-1 + CC-4)**

### NHÓM B: HIGH — Standard CRM mà không có thì thiếu chuyên nghiệp

| # | Chức năng | GitHub Status | Còn thiếu gì | Effort |
|---|-----------|---------------|---------------|--------|
| B1 | **Follow-up scheduling** | ✅ ĐÃ CÓ (routers/follow_ups.py + workers/followup_worker.py) | — | 0h |
| B2 | **NAS file links** | ✅ ĐÃ CÓ (routers/files.py) | — | 0h |
| B3 | **Global search** | ✅ ĐÃ CÓ (routers/search.py) | — | 0h |
| B4 | **My Dashboard** | ⚠️ Cần verify endpoint | Thêm nếu chưa có | 2h |
| B5 | **Activity timeline per customer** | ❌ CHƯA CÓ | Unified timeline endpoint | 3h |
| B6 | **In-app notification badges** | ✅ ĐÃ CÓ (routers/notifications.py + services/notify.py) | — | 0h |
| B7 | **Report export** | ⚠️ routers/reports.py có nhưng chưa export file | XLSX/PDF export | 6h |
| B8 | **Seed data: default users** | ⚠️ Cần verify | — | 0.5h |
| B9 | **Seed data: email templates** | ✅ routers/templates.py có | — | 0h |
| B10 | **Quote templates** | ✅ routers/templates.py có | — | 0h |

**Subtotal HIGH: ~~34h~~ → ~11.5h (chỉ B4, B5, B7, B8)**

### NHÓM C: MEDIUM — Nên có, có thể Phase 2

| # | Chức năng | GitHub Status | Còn thiếu gì | Effort |
|---|-----------|---------------|---------------|--------|
| C1 | **Inter-dept tasks** | ✅ ĐÃ CÓ (routers/inter_dept.py) | — | 0h |
| C2 | **Report configs** | ✅ ĐÃ CÓ (routers/reports.py) | — | 0h |
| C3 | **Commission tracking** | ✅ ĐÃ CÓ (routers/commissions.py) | — | 0h |
| C4 | **Email compose** | ⚠️ Qua pm_integration | Full compose flow | 6h |
| C5 | **Bulk import** | ✅ ĐÃ CÓ (routers/io_router.py) | — | 0h |
| C6 | **Data export** | ✅ ĐÃ CÓ (routers/io_router.py) | — | 0h |
| C7 | **Duplicate detection** | ❌ CHƯA CÓ | Check khi tạo customer/contact | 3h |
| C8 | **Dashboard filters** | ⚠️ Có nhưng hạn chế | Mở rộng filters | 3h |
| C9 | **Audit trail UI** | ✅ ĐÃ CÓ (reports.py /audit-log) | — | 0h |
| C10 | **DELETE (soft delete)** | ⚠️ Cần verify | Thêm nếu chưa có | 2h |

**Subtotal MEDIUM: ~~39h~~ → ~14h (chỉ C4, C7, C8, C10)**

### TỔNG HỢP SAU ĐÍNH CHÍNH

| Nhóm | Effort ban đầu | Effort thực tế | Đã implement |
|------|----------------|----------------|--------------|
| A: CRITICAL | 37h | **7h** | 80% |
| B: HIGH | 34h | **11.5h** | 66% |
| C: MEDIUM | 39h | **14h** | 64% |
| **TỔNG** | **110h** | **~32.5h** | **~70% done** |

**Kết hợp Cross-cutting (~40h):** Tổng effort còn lại = ~72.5h. Xem UNIFIED_CLAUDE_CODE_COMMAND.md.

---

## 3. CHI TIẾT THIẾT KẾ — CHỨC NĂNG TIÊU CHUẨN

### 3.1 Customer CRUD (A3, A4)

```
POST   /api/v1/customers           — Tạo KH mới (require_write)
  Body: { name, code, country, region, address, website, business_description }
  Logic: auto-generate UUID, check duplicate code, INSERT
  Response: 201 + customer object

PATCH  /api/v1/customers/{id}      — Sửa KH (require_write)
  Body: { name?, country?, region?, address?, website?, business_description?, status? }
  Logic: UPDATE only non-null fields, set updated_at
  Audit: log vào sale_audit_log nếu status change
  Response: 200 + updated customer

DELETE /api/v1/customers/{id}      — Soft delete (require_admin)
  Logic: SET status = 'DELETED', KHÔNG xóa record
  Response: 200 + { message: "Customer deactivated" }
```

### 3.2 Quotation Workflow (A5, A6)

```
Stage flow (Sale tự gửi, không cần approval chain):

  DRAFT → SENT → NEGOTIATION → WON
                              → LOST → REOPEN → DRAFT
                              → EXPIRED

POST   /api/v1/quotations                   — Tạo quotation (require_write)
  Body: {
    customer_id, opportunity_id?,
    project_name, product_group,
    tonnage, unit_price_usd, total_value_usd,
    incharge, validity_days, notes
  }
  Logic: auto-UUID, status=DRAFT, created_at=now
  Response: 201 + quotation object

PATCH  /api/v1/quotations/{id}              — Cập nhật quotation (require_write)
  Body: { status?, unit_price_usd?, tonnage?, notes?, sent_date?, won_date?, lost_reason? }
  Logic: validate state transition, audit-log nếu financial change
  Response: 200 + updated quotation

POST   /api/v1/quotations/{id}/revise       — Tạo revision (require_write)
  Body: { revision_notes, new_price?, new_tonnage? }
  Logic: increment revision_number, copy from parent, INSERT vào sale_quotation_revisions
  Response: 201 + revision object
```

### 3.3 Contract Management (A7, A8)

```
POST   /api/v1/contracts                    — Tạo hợp đồng (require_write)
  Body: {
    customer_id, opportunity_id?, quotation_id?,
    contract_no, project_name, product_group,
    contract_value_usd, tonnage,
    pm_name, start_date, end_date
  }
  Logic: auto-UUID, status=ACTIVE, tạo từ Won quotation nếu có quotation_id
  Response: 201 + contract object

PATCH  /api/v1/contracts/{id}               — Cập nhật (require_write)
  Body: { status?, pm_name?, end_date?, notes? }
  Logic: audit-log cho financial changes
  Response: 200

POST   /api/v1/contracts/{id}/milestones    — Thêm milestone (require_write)
  Body: { milestone_type, description, planned_date, value_usd }
  Response: 201

PATCH  /api/v1/contracts/{id}/milestones/{mid} — Cập nhật milestone (require_write)
  Body: { actual_date?, invoice_status?, payment_status? }
  Logic: audit-log
  Response: 200

POST   /api/v1/contracts/{id}/settlements   — Thêm settlement (require_write)
  Body: { description, amount_usd, due_date }
  Response: 201
```

### 3.4 Follow-up Scheduling (B1)

```
POST   /api/v1/follow-ups                   — Tạo follow-up (require_write)
  Body: {
    customer_id, opportunity_id?, contact_id?,
    scheduled_date, follow_up_type (CALL/EMAIL/VISIT/MEETING),
    notes, assigned_to
  }
  Logic: auto-UUID, status=PENDING
  Response: 201

GET    /api/v1/follow-ups                   — List (require_auth)
  Filters: assigned_to, status, date_from/to, customer_id, overdue
  Sort: scheduled_date ASC (sắp nhất trước)

PATCH  /api/v1/follow-ups/{id}              — Cập nhật (require_write)
  Body: { status? (DONE/CANCELLED/RESCHEDULED), actual_date?, outcome?, notes? }
  Logic: nếu RESCHEDULED → tạo follow-up mới tự động

GET    /api/v1/follow-ups/overdue           — Danh sách quá hạn (require_auth)
  Logic: WHERE scheduled_date < now() AND status = 'PENDING'
```

### 3.5 Notification System (B6)

```
Table mới: sale_notifications
  id TEXT PK, user_id TEXT, type TEXT, title TEXT, message TEXT,
  entity_type TEXT, entity_id TEXT, is_read INTEGER DEFAULT 0,
  created_at TEXT

Sources (auto-generate notification):
  - SLA worker: task overdue → notification cho assigned_to
  - Stale worker: deal > 30 days no activity → notification cho owner
  - Follow-up: scheduled_date = today → reminder notification
  - Quotation: validity expiring in 3 days → notification

GET    /api/v1/notifications                — List (require_auth)
  Filters: is_read, type
GET    /api/v1/notifications/count          — Badge count unread
PATCH  /api/v1/notifications/{id}/read      — Mark as read
PATCH  /api/v1/notifications/read-all       — Mark all as read
```

### 3.6 NAS File Links (B2)

```
GET    /api/v1/files                        — List NAS links (require_auth)
  Filters: customer_id, opportunity_id, project_code, file_type
  Response: 1,112 existing links

POST   /api/v1/files                        — Add NAS link (require_write)
  Body: { customer_id?, opportunity_id?, project_code?,
          file_path, file_type (QUOTATION/CONTRACT/DRAWING/REPORT/OTHER),
          description }
  Logic: validate path format, INSERT
```

### 3.7 Global Search (B3)

```
GET    /api/v1/search?q=xxx                 — Search across entities (require_auth)
  Logic: UNION query across:
    - sale_customers (name, code, business_description)
    - sale_customer_contacts (name, email, phone)
    - sale_opportunities (project_name, description)
    - sale_quotation_history (project_name, customer_code)
    - sale_emails (subject, snippet)
  Response: [{ entity_type, entity_id, title, subtitle, match_field }]
  Limit: 20 results per entity type
```

### 3.8 My Dashboard (B4)

```
GET    /api/v1/dashboard/my?user=xxx        — Personal dashboard (require_auth)
  Response: {
    my_tasks: { total, overdue, in_progress, completed_this_week },
    my_pipeline: { deals, total_value, stages: [...] },
    my_follow_ups: { today, overdue, this_week },
    my_recent_activities: [ last 10 interactions/emails ],
    my_notifications: { unread_count }
  }
```

---

## 4. FRONTEND MVP — THIẾT KẾ 7 SCREENS

Standalone HTML (sale_dashboard.html), dark theme, fetch từ :8767.

| Screen | Nội dung | API endpoints |
|--------|----------|---------------|
| **1. Login** | Nhập API key → lưu sessionStorage → redirect dashboard | POST /auth/me |
| **2. Dashboard** | KPI cards + pipeline chart + task summary + notifications | /dashboard/executive, /notifications/count |
| **3. My View** | My tasks, my follow-ups, my pipeline, recent activity | /dashboard/my |
| **4. Customers** | List + search + click → detail (contacts, interactions, timeline) | /customers, /search |
| **5. Pipeline** | Table view theo stage, click → opportunity detail | /opportunities, /dashboard/pipeline |
| **6. Quotations** | List + tạo mới + revise + win/lose buttons | /quotations, POST/PATCH |
| **7. Tasks** | Kanban board (4 columns) + create task | /tasks/board, POST/PATCH |

Mỗi screen đều có:
- Header: logo + user name + notification bell (badge count) + logout
- Sidebar: navigation 7 screens
- Responsive: mobile-friendly

---

## 5. LỆNH CHO CLAUDE CODE — FULL FUNCTIONAL FIX

```
Đọc CLAUDE.md và FUNCTIONAL_COMPLETENESS_AUDIT.md trước.

## CONTEXT
Sale Platform v4 có 14 routers + 63 endpoints nhưng:
- 94% endpoints KHÔNG CÓ AUTH
- Không có CRUD cho customers, quotations, contracts
- Không có frontend
- Thiếu 6 tables/routers: follow-ups, NAS links, notifications, search, quote templates, inter-dept tasks
Team Sale 3-5 người cần dùng được platform cho công việc hàng ngày.

## QUY TẮC
(Giữ nguyên 15 rules từ SALE_PLATFORM_MASTER_FIX.md)

## PHASE 1: Auth Fix (CRITICAL — làm trước)

### 1a. Thêm auth cho TẤT CẢ routers
Mở TỪNG file trong routers/. Thêm:
  - require_auth (from auth import require_auth) cho TẤT CẢ GET endpoints (trừ /health)
  - require_write (from auth import require_write) cho TẤT CẢ POST/PATCH endpoints
  - require_admin (from auth import require_admin) cho user management

Cách thêm: mỗi endpoint function thêm parameter:
  async def list_customers(..., _=Depends(require_auth)):
Cho POST/PATCH:
  async def create_customer(..., _=Depends(require_write)):

### 1b. Thêm GET /api/v1/auth/me
Trong routers/ tạo auth_router.py:
  GET /auth/me → đọc X-API-Key → lookup trong config → trả { user, role, tier }

### 1c. Seed default users
POST /api/v1/users/seed-defaults (require_admin):
  Insert 3 users nếu chưa có:
  - admin@ibs.com.vn / ADMIN / "Huyến (Admin)"
  - sale@ibs.com.vn / MANAGER / "Sale Manager"
  - viewer@ibs.com.vn / VIEWER / "Viewer"

## PHASE 2: Customer CRUD

### 2a. POST /api/v1/customers (require_write)
Body: { name, code?, country?, region?, address?, website?, business_description? }
Logic: auto-UUID, check duplicate code, INSERT, return 201
Nếu code is None → auto-generate từ name (first 3 chars uppercase + sequence)

### 2b. PATCH /api/v1/customers/{id} (require_write)
Body: partial update, SET updated_at = now()
Nếu status change → audit_log

### 2c. Soft DELETE /api/v1/customers/{id} (require_admin)
SET status = 'DELETED', không xóa record

## PHASE 3: Quotation Workflow

### 3a. POST /api/v1/quotations (require_write)
Table: sale_quotation_history
Body: { customer_id, customer_code?, project_name, product_group,
        tonnage, unit_price_usd, total_value_usd,
        incharge, validity_days?, notes? }
Logic: status=DRAFT, created_at=now(), revision_count=0
Validate: customer_id exists in sale_customers

### 3b. PATCH /api/v1/quotations/{id} (require_write)
State transitions:
  DRAFT → SENT, NEGOTIATION
  SENT → NEGOTIATION, WON, LOST, EXPIRED
  NEGOTIATION → WON, LOST, EXPIRED
  LOST → DRAFT (reopen)
  EXPIRED → DRAFT (reopen)
Dùng validate_transition pattern từ services/state_machine.py
Audit-log nếu price/tonnage change

### 3c. POST /api/v1/quotations/{id}/revise (require_write)
Tạo revision trong sale_quotation_revisions
Copy key fields từ parent, increment revision_number

## PHASE 4: Contract CRUD

### 4a. POST /api/v1/contracts (require_write)
Table: sale_active_contracts
Body: { customer_id, contract_no, project_name, product_group,
        contract_value_usd, tonnage, pm_name, start_date?, end_date? }
Optional: quotation_id → auto-fill từ won quotation
status = ACTIVE

### 4b. PATCH /api/v1/contracts/{id} (require_write)
Update fields, audit-log cho financial changes

### 4c. POST /api/v1/contracts/{id}/milestones (require_write)
### 4d. PATCH /api/v1/contracts/{id}/milestones/{mid} (require_write)
### 4e. POST /api/v1/contracts/{id}/settlements (require_write)

## PHASE 5: Missing Routers

### 5a. Follow-ups router (routers/follow_ups.py)
Table: sale_follow_up_schedules
GET  /follow-ups (list, filter: assigned_to, status, overdue, customer_id, date range)
GET  /follow-ups/overdue (WHERE scheduled_date < now AND status=PENDING)
POST /follow-ups (create: customer_id, scheduled_date, type, notes, assigned_to)
PATCH /follow-ups/{id} (update status: DONE/CANCELLED/RESCHEDULED)

### 5b. NAS Files router (routers/files.py)
Table: sale_nas_file_links (1,112 records already)
GET  /files (list, filter: customer_id, opportunity_id, project_code, file_type)
POST /files (add link: file_path, file_type, description, customer_id?, opp_id?)

### 5c. Notifications router (routers/notifications.py)
Tạo table mới: sale_notifications
  id TEXT PK, user_id TEXT, type TEXT (SLA/STALE/FOLLOWUP/QUOTATION),
  title TEXT, message TEXT, entity_type TEXT, entity_id TEXT,
  is_read INTEGER DEFAULT 0, created_at TEXT
GET  /notifications (list, filter: is_read)
GET  /notifications/count (unread count)
PATCH /notifications/{id}/read
PATCH /notifications/read-all
Thêm vào schema_all.sql: CREATE TABLE IF NOT EXISTS sale_notifications (...)

### 5d. Search router (routers/search.py)
GET  /search?q=xxx
UNION query: customers (name,code) + contacts (name,email) + opportunities (project_name) + quotations (project_name) + emails (subject)
Return: [{ entity_type, entity_id, title, subtitle, match_field }] limit 100

## PHASE 6: Dashboard Expansion

### 6a. GET /api/v1/dashboard/my?user=xxx
Query: my tasks (assigned_to=user), my pipeline (assigned_to=user),
       my follow-ups (assigned_to=user, today+overdue), my notifications (unread)

### 6b. Mở rộng /dashboard/summary
Thêm: total_follow_ups, overdue_follow_ups, total_files, notification_count

## PHASE 7: Register & Test

### 7a. Register new routers trong main.py
from routers import follow_ups, files, notifications, search, auth_router
app.include_router(auth_router.router, prefix="/api/v1", tags=["Auth"])
app.include_router(follow_ups.router, prefix="/api/v1/follow-ups", tags=["Follow-ups"])
app.include_router(files.router, prefix="/api/v1/files", tags=["Files"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])

### 7b. Update workers to generate notifications
- workers/sla_worker.py: khi task overdue → INSERT vào sale_notifications
- workers/stale_worker.py: khi deal stale → INSERT vào sale_notifications
Thêm worker mới:
- workers/followup_worker.py: daily 7AM, check follow-ups due today → notification

### 7c. Test checklist
python main.py
Verify TẤT CẢ endpoints cần X-API-Key:
  curl http://localhost:8767/api/v1/customers → 401 Unauthorized
  curl -H "X-API-Key: dev-key-local-only" http://localhost:8767/api/v1/customers → 200

Verify new CRUD:
  POST /customers → 201
  POST /quotations → 201, status=DRAFT
  PATCH /quotations/{id} status=SENT → 200
  POST /contracts → 201
  POST /follow-ups → 201
  GET /search?q=braden → results
  GET /notifications/count → { count: N }
  GET /dashboard/my?user=admin@ibs.com.vn → personal stats

### 7d. Commit
git add -A && git commit -m "Full functional fix: auth on all 63+ endpoints, customer/quotation/contract CRUD, follow-ups, notifications, search, my-dashboard"
```

---

## 6. TỔNG KẾT — EFFORT ESTIMATE

| Phase | Nội dung | Endpoints mới/sửa | Effort |
|-------|----------|-------------------|--------|
| Phase 1 | Auth fix + me + seed | 59 sửa + 2 mới | 4h |
| Phase 2 | Customer CRUD | 3 mới | 3h |
| Phase 3 | Quotation workflow | 3 mới | 6h |
| Phase 4 | Contract CRUD | 5 mới | 5h |
| Phase 5 | Follow-ups, Files, Notifications, Search | 12 mới | 12h |
| Phase 6 | Dashboard expansion | 2 mới/sửa | 4h |
| Phase 7 | Register, workers, test | — | 4h |
| **TỔNG** | | **27 endpoints mới, 59 sửa** | **~38h** |

### So với SALE_PLATFORM_MASTER_FIX.md (document trước)
- MASTER_FIX: 11 bước, focus align code ↔ DB schema
- Document này: 7 phases, focus **chức năng đầy đủ để team dùng được**
- Hai document BỔ SUNG nhau: chạy MASTER_FIX trước (align schema), sau đó chạy FUNCTIONAL_FIX (thêm chức năng)
- Hoặc MERGE thành 1 lệnh duy nhất cho Claude Code (xem Phần 5 ở trên)

---

## 7. PHASE 2+ FEATURES (sau khi team đã dùng được)

| Feature | Effort | Priority |
|---------|--------|----------|
| Frontend MVP (7 screens HTML) | 16h | HIGH — sau khi API hoàn chỉnh |
| Email compose & send | 6h | MEDIUM |
| Bulk import CSV/Excel | 6h | MEDIUM |
| Data export CSV/Excel | 4h | MEDIUM |
| Inter-dept tasks | 4h | MEDIUM |
| Commission tracking | 4h | LOW |
| Report configs + scheduled reports | 4h | LOW |
| Duplicate detection | 3h | LOW |
| Audit trail UI | 2h | LOW |
