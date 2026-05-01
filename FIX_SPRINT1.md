# FIX SPRINT 1 — Align Code với DB 32 Tables

## Lệnh cho Claude Code

Copy toàn bộ block dưới đây paste vào Claude Code:

---

```
Đọc CLAUDE.md trước.

Sprint 1 code đã viết xong nhưng trỏ schema cũ (16 tables). DB thực tế đã có 32 tables + 6,700+ records.
Nhiệm vụ: ALIGN code hiện tại với DB mới. KHÔNG viết lại — chỉ sửa và mở rộng.

## BƯỚC 0: Build Database
cd sql_import/ && python build_db.py && cd ..
Xác nhận: 32 tables, ~6,700 records, 0 critical errors.

## BƯỚC 1: Fix database.py (CRITICAL)
File database.py dòng 31 trỏ sai:
  _SQLITE_SCHEMA = os.path.join(_PROJECT_ROOT, "schema.sql")        ← SAI (16 tables cũ)
Sửa thành:
  _SQLITE_SCHEMA = os.path.join(_PROJECT_ROOT, "sql_import", "schema_all.sql")  ← ĐÚNG (32 tables)

Tương tự kiểm tra DB_PATH trong config.py → phải trỏ tới sale.db ở project root.

## BƯỚC 2: Thêm routers mới cho tables có data
DB có 32 tables nhưng code chỉ có routers cho ~10 tables gốc. Thêm:

### 2a. routers/contacts.py (MỚI)
- GET /api/contacts?customer_id=xxx — list contacts của 1 customer
- GET /api/contacts/{id} — chi tiết 1 contact
- POST /api/contacts — tạo contact mới
- Table: sale_customer_contacts (2,990 records)
- Liên kết: customer_id → sale_customers.id

### 2b. routers/contracts.py (MỚI)
- GET /api/contracts — list active contracts
- GET /api/contracts/{id} — chi tiết + milestones
- GET /api/contracts/{id}/milestones — milestones của contract
- GET /api/contracts/{id}/settlements — settlements của contract
- Tables: sale_active_contracts (14), sale_contract_milestones (55), sale_settlements (32)

### 2c. routers/quotations.py (MỚI)
- GET /api/quotations — list quotation history
- GET /api/quotations?customer_id=xxx — filter by customer
- GET /api/quotations/{id}/revisions — revision history
- Tables: sale_quotation_history (968), sale_quotation_revisions (147)

### 2d. routers/interactions.py (MỚI)
- GET /api/interactions — list all interactions
- GET /api/interactions?customer_id=xxx — filter by customer
- GET /api/interactions?type=CLIENT_VISIT — filter by type
- Table: sale_customer_interactions (175 records — meetings, visits, calls)

### 2e. routers/intelligence.py (MỚI)
- GET /api/intelligence/signals — market signals
- GET /api/intelligence/products — product opportunities
- Tables: sale_market_signals (18), sale_product_opportunities (51)

### 2f. Mở rộng routers/emails.py
Thêm endpoints cho:
- GET /api/emails/labels — list email labels (sale_email_labels, 47 records)
- GET /api/emails/full — full email mapping (sale_email_full, 108 records)

### 2g. Mở rộng routers/customers.py
Thêm:
- GET /api/customers/{id}/contacts — contacts của customer (join sale_customer_contacts)
- GET /api/customers/{id}/interactions — interactions của customer
- GET /api/customers/{id}/quotations — quotation history của customer
- GET /api/customers/{id}/contracts — contracts của customer

## BƯỚC 3: Thêm Pydantic models
Tạo models tương ứng cho mỗi router mới:
- models/contact.py — CustomerContact, CustomerContactCreate
- models/contract.py — ActiveContract, ContractMilestone, Settlement
- models/quotation.py — QuotationHistory, QuotationRevision
- models/interaction.py — CustomerInteraction, CustomerInteractionCreate
- models/intelligence.py — MarketSignal, ProductOpportunity

Đọc schema_all.sql để lấy đúng column names + types.
Optional fields cho nullable columns. UUID primary keys là TEXT.

## BƯỚC 4: Cập nhật dashboard.py
Dashboard hiện tại chỉ query ~5 tables. Mở rộng GET /api/dashboard/summary:
- Thêm: total_contacts, total_quotations, total_contracts, total_interactions
- Thêm: quotation_win_rate (won/total từ sale_quotation_history)
- Thêm: active_contract_value (SUM từ sale_active_contracts)
- Thêm: recent_interactions (5 gần nhất)
- Thêm: pipeline_by_stage (count per stage)

## BƯỚC 5: Register routers trong main.py
Thêm vào main.py:
  from routers import contacts, contracts, quotations, interactions, intelligence
  app.include_router(contacts.router, prefix="/api", tags=["Contacts"])
  app.include_router(contracts.router, prefix="/api", tags=["Contracts"])
  app.include_router(quotations.router, prefix="/api", tags=["Quotations"])
  app.include_router(interactions.router, prefix="/api", tags=["Interactions"])
  app.include_router(intelligence.router, prefix="/api", tags=["Intelligence"])

## BƯỚC 6: Test
pip install -r requirements.txt
python main.py
Verify trên http://localhost:8767/docs:
- GET /health → 200
- GET /api/customers → 992 records
- GET /api/contacts?customer_id=xxx → contacts
- GET /api/contracts → 14 active contracts
- GET /api/quotations → quotation history
- GET /api/interactions → 175 records
- GET /api/intelligence/signals → 18 signals
- GET /api/dashboard/summary → full stats

## BƯỚC 7: Commit
git add -A && git commit -m "Align Sprint 1 with 32-table DB schema — add contacts, contracts, quotations, interactions, intelligence routers"

## QUY TẮC BẮT BUỘC
1. KHÔNG modify existing tables — chỉ CREATE TABLE / ADD COLUMN
2. Mọi import PHẢI log vào sale_import_log
3. SQLite types: TEXT cho UUID/datetime/JSON, INTEGER cho boolean
4. Dùng query() cho reads, execute() cho writes
5. Auth: Depends(require_auth) read, Depends(require_write) write
6. Naming: tables sale_*, indexes idx_{short}_{col}, UUID primary keys
7. Gmail tokens: stored per-mailbox, KHÔNG hardcode
8. PM integration: KHÔNG auto-send — luôn DRAFT
9. Logging: structlog.get_logger() — KHÔNG print()
10. State transitions: validate_*_transition() trước status changes
11. Financial changes: audit-log qua services/audit.py
```
