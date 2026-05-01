# SALE PLATFORM — MASTER FIX (One-Pass Redesign)

> **Date:** 30/04/2026
> **Author:** Claude AI (Cowork) cho Chairman Le
> **Mục đích:** Lệnh Claude Code sửa Sale Platform v4 MỘT LẦN cho chạy được
> **Đã đọc rules:** CLAUDE.md v5.1 (R1-R13), TEAM_RULES v2.0, SYSTEM_DESIGN v1.0, ADR-001, Sale Platform CLAUDE.md

---

## PHẦN A — TRẢ LỜI 3 CÂU HỎI TÍCH HỢP

### A1. Dùng IBS One đăng nhập — cần lấy gì từ Team IBS One?

**Kết luận: HIỆN TẠI KHÔNG CẦN.**

Lý do:
- ibshi1 (IBS One L1) chưa có auth — không có NextAuth, không có middleware, không có session provider
- ibshi1 chỉ có Prisma User model: `id (cuid), email (unique), name, role (ADMIN/MANAGER/USER), department`
- Sale Platform hiện dùng X-API-Key (header-based, 3 tiers) — không có user session

**Khi IBS One triển khai auth (tương lai):**
- Cần biết: auth mechanism (NextAuth? JWT? OAuth?), token format, session endpoint
- Cần biết: API endpoint verify token (ví dụ GET /api/auth/session)
- Cần map role: IBS One role (ADMIN/MANAGER/USER) → Sale Platform tier (ADMIN/MANAGER/VIEWER)

**Hành động bây giờ:** Sale Platform chạy auth độc lập. Khi IBS One có auth → thêm 1 auth adapter (~50 lines code), không cần rewrite.

### A2. Frontend độc lập chạy trước — được không?

**Kết luận: ĐƯỢC, và NÊN LÀM NHƯ VẬY.**

Lý do tuân thủ rules:
- R8: HTML standalone (double-click, không cần server) — áp dụng cho IBS One Portal
- R12: v4.x = prototype (AH + AI), v5.x = production (Toàn)
- ADR-001: Sale Platform L2 giao tiếp IBS One L1 CHỈ qua REST API

Frontend options (cả 2 đều hợp lệ):
1. **Standalone HTML** (giống IBSHI_Index_Portal) — double-click mở, fetch API từ Sale Platform :8767
2. **React SPA** — build thành static files, serve từ FastAPI hoặc Nginx

**Khuyến nghị:** Option 1 cho MVP (nhanh, đúng pattern v4.x prototype). Toàn chuyển sang React/Next.js cho v5.x production sau.

### A3. Tích hợp sau — phức tạp không?

**Kết luận: ĐỘ PHỨC TẠP THẤP.**

Vì ADR-001 đã enforce đúng pattern:
- Sale Platform ↔ IBS One CHỈ qua REST API (không direct DB)
- User model tương thích: email + role + department có cả 2 bên

Tích hợp sau chỉ cần:
1. **Auth adapter** (50 lines): verify IBS One JWT token → map sang Sale Platform role
2. **Menu link**: thêm Sale Platform vào IBSHI_Index_Portal (1 dòng HTML)
3. **User sync**: optional — Sale Platform tự có user table, hoặc query IBS One `/api/users`

Rủi ro duy nhất: nếu IBS One chọn auth mechanism quá khác biệt (nhưng tiêu chuẩn industry là JWT, xác suất thấp).

---

## PHẦN B — TỔNG HỢP TẤT CẢ RULES ÁP DỤNG

### B1. Rules từ IBS One CLAUDE.md v5.1 (áp dụng cho Sale Platform)

| Rule | Nội dung | Áp dụng Sale Platform |
|------|----------|----------------------|
| R4 | KHÔNG thay đổi schema bảng đã có data | ✅ Bắt buộc — chỉ ADD column / CREATE table |
| R7 | Import script phải log vào import_log | ✅ Bắt buộc — sale_import_log |
| R11 | Query DB bằng Python sqlite3 module | ✅ Bắt buộc — không dùng sqlite3 CLI |
| R12 | AH = v4.x, Toàn = v5.x | ✅ Code hiện tại = v4.x prototype |
| R13 | Mọi thay đổi file → ghi CHANGELOG | ✅ Bắt buộc |

### B2. Rules từ TEAM_RULES v2.0

| Rule | Nội dung | Áp dụng |
|------|----------|---------|
| DB Rule 1 | KHÔNG thay đổi schema bảng đã có data | = R4 |
| DB Rule 2 | LUÔN backup trước ALTER/DELETE | ✅ |
| DB Rule 3 | LUÔN PRAGMA table_info() trước query | ✅ = R6 |
| DB Rule 5 | Query bằng Python sqlite3 | = R11 |
| DB Rule 6 | DB file: 01_DATABASE/ibs_core_v4_clean.db | ❌ Sale Platform dùng sale.db riêng |

### B3. Rules từ Sale Platform CLAUDE.md (11 rules)

| # | Rule | Chi tiết |
|---|------|----------|
| 1 | NEVER modify existing tables | Chỉ CREATE TABLE / ADD COLUMN |
| 2 | All imports MUST log to sale_import_log | Không ngoại lệ |
| 3 | SQLite-compatible types | TEXT cho UUID/datetime/JSON, INTEGER cho boolean |
| 4 | Query helper | query() cho reads, execute() cho writes |
| 5 | Auth | Depends(require_auth) read, Depends(require_write) write |
| 6 | Naming | tables sale_*, indexes idx_{short}_{col}, UUID PK |
| 7 | Gmail tokens | Stored per-mailbox, KHÔNG hardcode |
| 8 | PM integration | KHÔNG auto-send — luôn DRAFT |
| 9 | Logging | structlog.get_logger() — KHÔNG print() |
| 10 | State transitions | validate_*_transition() trước status changes |
| 11 | Financial changes | audit-log qua services/audit.py |

### B4. Rules từ ADR-001

| Constraint | Chi tiết |
|------------|----------|
| REST only | Giao tiếp ibshi1 CHỈ qua REST API — KHÔNG direct DB access |
| L2 scope | Departmental tool cho phòng SALE — không expose cho platform khác |
| Python accepted | Exception cho Hard Rule #4 — phải tuân thủ type hints, structlog, Pydantic, async |
| Scale warning | Nếu scale thành L1 hoặc multi-tenant → PHẢI rewrite sang Node.js/TypeScript |

### B5. Rules từ SYSTEM_DESIGN v1.0

| Principle | Chi tiết |
|-----------|----------|
| 5-Layer architecture | Sale Platform = Layer 2 (Sales Intelligence) |
| SQLite dev → PostgreSQL prod | Adapter pattern, schema `sale` |
| Version: v4.x prototype | AH + AI prototype, Builder adapt v5.x |

---

## PHẦN C — LỆNH CHO CLAUDE CODE

Copy toàn bộ block dưới đây paste vào Claude Code:

---

```
Đọc CLAUDE.md trước (trong thư mục sale_platform_v4/).

## CONTEXT
Sale Platform v4 prototype. Code Sprint 1 đã viết xong (14 routers, 13 models) nhưng cần ALIGN với:
- DB 32 tables + 6,700 records (source of truth: sql_import/schema_all.sql)
- Tất cả rules (xem dưới)
- Thiếu các tính năng operational để hệ thống chạy được

## QUY TẮC BẮT BUỘC (tóm từ 5 nguồn rules)
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
13. Python code PHẢI có type hints, Pydantic validation, async/await cho I/O
14. LUÔN PRAGMA table_info() hoặc đọc schema_all.sql trước khi query
15. Query bằng Python sqlite3 module — KHÔNG dùng sqlite3 CLI

## BƯỚC 0: Rebuild Database
cd sql_import/ && python build_db.py && cd ..
Xác nhận: 32 tables, ~6,700 records, 0 critical errors.
Nếu build_db.py chưa có → dùng: sqlite3 ../sale.db < master_import.sql

## BƯỚC 1: Fix database.py (CRITICAL)
File database.py dòng 31:
  _SQLITE_SCHEMA = os.path.join(_PROJECT_ROOT, "schema.sql")        ← SAI (16 tables cũ)
Sửa thành:
  _SQLITE_SCHEMA = os.path.join(_PROJECT_ROOT, "sql_import", "schema_all.sql")  ← ĐÚNG (32 tables)

Kiểm tra DB_PATH trong config.py → phải trỏ tới sale.db ở project root.

## BƯỚC 2: Verify tất cả models/ match schema_all.sql
Đọc sql_import/schema_all.sql. Với MỖI file trong models/:
- So sánh column names + types với schema_all.sql
- Fix bất kỳ mismatch nào
- Thêm Optional[] cho nullable columns
- UUID primary keys phải là str (TEXT trong SQLite)

Files cần verify:
- models/customer.py ← sale_customers (992 records)
- models/contact.py ← sale_customer_contacts (2,990)
- models/opportunity.py ← sale_opportunities (25)
- models/email.py ← sale_emails (125), sale_email_templates, sale_email_activity_log
- models/task.py ← sale_tasks
- models/mailbox.py ← sale_monitored_mailboxes
- models/user_role.py ← sale_user_roles
- models/contract.py ← sale_active_contracts (14), sale_contract_milestones (48), sale_settlements (28)
- models/quotation.py ← sale_quotation_history (1,007), sale_quotation_revisions (160)
- models/interaction.py ← sale_customer_interactions (175)
- models/intelligence.py ← sale_market_signals (18), sale_product_opportunities (56)
- models/dashboard.py ← aggregation model
- models/pm_bridge.py ← sale_pm_sync_log, sale_inter_dept_tasks

## BƯỚC 3: Verify tất cả routers/ match schema + models
Với MỖI file trong routers/:
- Đảm bảo query đúng column names từ schema_all.sql
- Đảm bảo return đúng Pydantic model
- Đảm bảo auth đúng: require_auth cho GET, require_write cho POST/PUT/DELETE
- Đảm bảo dùng query() cho reads, execute() cho writes
- Đảm bảo structlog logging (không print())

Routers cần verify:
- routers/customers.py — GET list, GET detail, POST create
  + Thêm sub-endpoints: GET /customers/{id}/contacts, /interactions, /quotations, /contracts
- routers/contacts.py — CRUD cho sale_customer_contacts
- routers/contracts.py — GET list, GET detail, GET /{id}/milestones, GET /{id}/settlements
- routers/quotations.py — GET list, filter by customer_id, GET /{id}/revisions
- routers/interactions.py — GET list, filter by customer_id + type, POST create
- routers/intelligence.py — GET /signals, GET /products
- routers/emails.py — existing + thêm GET /labels, GET /full
- routers/opportunities.py — 5 endpoints + state machine
- routers/tasks.py — 6 endpoints + state machine
- routers/dashboard.py — PHẢI query across tất cả populated tables (xem Bước 4)
- routers/users.py — CRUD cho sale_user_roles
- routers/mailboxes.py — CRUD cho sale_monitored_mailboxes
- routers/pm_integration.py — 6 endpoints
- routers/health.py — GET /health (public, no auth)

## BƯỚC 4: Mở rộng Dashboard
Dashboard hiện tại chỉ query ~5 tables. Mở rộng GET /api/v1/dashboard/summary:
- total_customers (từ sale_customers)
- total_contacts (từ sale_customer_contacts)
- total_opportunities + pipeline_by_stage (từ sale_opportunities)
- total_quotations + quotation_win_rate (won/total từ sale_quotation_history)
- total_contracts + active_contract_value (SUM từ sale_active_contracts)
- total_interactions + recent_interactions (5 gần nhất)
- total_emails (từ sale_emails)
- market_signals_count (từ sale_market_signals)
- pipeline_value_weighted (từ sale_opportunities: amount × probability)

## BƯỚC 5: Auth — Giữ X-API-Key, thêm User Context
Auth hiện tại (auth.py) đủ dùng cho MVP. KHÔNG thay đổi mechanism.
Thêm:
- GET /api/v1/auth/me — trả về user info dựa trên API key
- Seed 3 default users vào sale_user_roles (nếu chưa có):
  - admin@ibs.com.vn / ADMIN / "Admin"
  - sale@ibs.com.vn / MANAGER / "Sale Manager"
  - viewer@ibs.com.vn / VIEWER / "Viewer"
- Thêm endpoint POST /api/v1/users/seed-defaults (require_admin)

## BƯỚC 6: Config — Environment Variables
Verify config.py có tất cả cần thiết:
- API_KEYS: từ env var SALE_API_KEYS (comma-separated), fallback dev key
- DB_PATH: sale.db tại project root
- CORS_ORIGINS: từ env var, default ["http://localhost:3000", "http://localhost:8767"]
- LOG_LEVEL: từ env var, default INFO
- Feature flags: ENABLE_EMAIL_SYNC, ENABLE_PM_INTEGRATION, ENABLE_TASK_SCHEDULING

## BƯỚC 7: Register routers trong main.py
Verify main.py đã register TẤT CẢ 14 routers:
  from routers import (health, customers, contacts, opportunities, emails,
                       tasks, dashboard, mailboxes, users, pm_integration,
                       contracts, quotations, interactions, intelligence)

Verify prefix = /api/v1 cho tất cả (trừ health = /health hoặc /api/v1/health).
Verify CORS middleware có allow_origins từ config.

## BƯỚC 8: Startup Validation
Trong main.py @app.on_event("startup"):
1. Check sale.db exists — nếu không, auto-init từ schema_all.sql
2. Verify bảng count >= 32
3. Log startup info: tables loaded, record counts, version

## BƯỚC 9: Test End-to-End
pip install -r requirements.txt
python main.py

Verify trên http://localhost:8767/docs (Swagger):
- GET /health → 200 + version info
- GET /api/v1/customers → list (expect ~992 records)
- GET /api/v1/contacts?customer_id=<any_id> → contacts
- GET /api/v1/contracts → 14 active contracts
- GET /api/v1/quotations → quotation history
- GET /api/v1/interactions → 175 records
- GET /api/v1/intelligence/signals → 18 signals
- GET /api/v1/opportunities → 25 pipeline items
- GET /api/v1/dashboard/summary → full stats (all counts > 0)
- GET /api/v1/emails → emails list
- GET /api/v1/auth/me (with X-API-Key header) → user info

NẾU bất kỳ endpoint nào fail → fix trước khi tiếp.

## BƯỚC 10: Tạo Frontend MVP (Standalone HTML)
Tạo file sale_dashboard.html trong project root:
- Standalone HTML (double-click mở, không cần server ngoài API)
- Fetch data từ http://localhost:8767/api/v1/
- X-API-Key gửi qua header (key nhập trên UI hoặc hardcode dev key)
- Hiển thị:
  1. Dashboard summary (cards: customers, contacts, pipeline, contracts)
  2. Customer list (search + filter)
  3. Pipeline view (kanban hoặc table theo stage)
  4. Recent interactions
- Dark theme (match IBS One: --bg:#0a0e1a --card:#111828 --accent:#3b82f6)
- Chart.js từ CDN cho visualizations
- Responsive (mobile-friendly)

LƯU Ý: Đây là v4.x prototype. Toàn sẽ build v5.x production frontend riêng.

## BƯỚC 11: Commit
git add -A
git commit -m "Master Fix: align 14 routers + 13 models with 32-table schema, add dashboard expansion, auth/me, frontend MVP"
```

---

## PHẦN D — CHECKLIST SAU KHI CLAUDE CODE CHẠY XONG

### D1. Verify kết quả

| # | Check | Expected |
|---|-------|----------|
| 1 | `python main.py` không lỗi | Server start trên :8767 |
| 2 | GET /health | 200 + version |
| 3 | GET /api/v1/customers | ~992 records |
| 4 | GET /api/v1/dashboard/summary | Tất cả counts > 0 |
| 5 | GET /api/v1/contracts | 14 records |
| 6 | GET /api/v1/quotations | ~1,007 records |
| 7 | Swagger UI | Tất cả endpoints hiển thị, có auth |
| 8 | sale_dashboard.html | Mở bằng browser, hiển thị data |

### D2. Nếu cần fix tiếp

Paste vào Claude Code:
```
Đọc CLAUDE.md. Server đang chạy trên :8767.
[Mô tả lỗi cụ thể]
Fix theo rules: không modify existing tables, structlog logging, type hints, Pydantic validation.
```

---

## PHẦN E — ROADMAP SAU MASTER FIX

### Phase 2: Quotation + Contract Modules (Sprint 2)
- Quotation workflow: create → revise → send → win/lose
- Contract management: milestones → settlements → completion
- Tables đã có data: sale_quotation_history (1,007), sale_active_contracts (14)
- Thêm routers: PATCH /quotations/{id}/status, POST /contracts

### Phase 3: Email Intelligence (Sprint 3)
- Gmail sync worker (APScheduler, 5-min interval)
- Email classification (10 types: RFQ, TECHNICAL, NEGOTIATION, etc.)
- Auto-task creation từ classified emails
- SLA monitoring + escalation

### Phase 4: KHKD Integration
- KHKD 2026 targets: $19.1M revenue, 7,000 tons, 21% GM, 25 POs
- Pipeline vs KHKD comparison dashboard
- Gap analysis: target vs actual by product group

### Phase 5: IBS One Integration
- Khi ibshi1 triển khai auth → thêm auth adapter
- Link Sale Platform từ Index Portal
- User sync: IBS One users → Sale Platform roles
- Shared dashboard data (via REST API per ADR-001)

---

## PHẦN F — FILES REFERENCE

| File | Vai trò | Đọc khi |
|------|---------|---------|
| CLAUDE.md | Rules + architecture | Đầu mỗi session |
| sql_import/schema_all.sql | DB schema (source of truth) | Verify models/routers |
| sql_import/build_db.py | Build sale.db | Trước khi code |
| ADR-001 | Python exception rationale | Khi hỏi về tech stack |
| FIX_SPRINT1.md | Sprint 1 fix plan (cũ) | Superseded bởi file này |
| SPRINT1_PLAN.md | Sprint 1 plan (cũ) | Reference cho gap analysis |
| docs/etl_mapping.md | ETL source→target mapping | Khi thêm data mới |
