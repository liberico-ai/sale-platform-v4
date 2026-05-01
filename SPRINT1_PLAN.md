# SALE PLATFORM v4 — SPRINT 1 EXECUTION PLAN

## Lệnh cho Claude Code

Dán lệnh dưới đây vào Claude Code khi mở project `sale_platform_v4/`:

---

```
Đọc CLAUDE.md trước. Sau đó thực hiện Sprint 1 Sale Platform theo plan dưới đây.

## BƯỚC 0: Build Database
cd sql_import/ && python build_db.py && cd ..
Xác nhận sale.db có 32 tables, ~6,700 records.

## BƯỚC 1: Cập nhật database.py
- Dòng 31: đổi schema path từ "schema.sql" → "sql_import/schema_all.sql"
- Đây là schema chính thức (32 tables + 2 views + 92 indexes)
- KHÔNG sửa schema_all.sql — chỉ sửa database.py để trỏ đúng

## BƯỚC 2: Cập nhật config.py
- DB_PATH mặc định: sale.db (nằm ở project root, build từ sql_import/)
- Đảm bảo EMAIL_TYPES có đủ 10 types
- Thêm IMPORT_DIR = "sql_import/" nếu chưa có

## BƯỚC 3: Kiểm tra & sửa routers/ cho đúng schema mới
32 tables hiện tại — các routers cần cover:
- customers.py: sale_customers (992 records), sale_customer_contacts (2,990)
- opportunities.py: sale_opportunities (92), sale_quotation_history (968), sale_quotation_revisions (147)
- emails.py: sale_emails (95), sale_email_labels (47), sale_email_full (108)
- tasks.py: sale_tasks, sale_follow_up_schedules
- dashboard.py: aggregate queries across all tables
- Thêm router mới nếu cần: contracts.py cho sale_active_contracts + sale_contract_milestones + sale_settlements

Nguyên tắc:
- query() cho reads, execute() cho writes
- Depends(require_auth) cho read, Depends(require_write) cho write
- State machine: validate_*_transition() trước khi đổi status
- Financial changes: audit log qua services/audit.py
- KHÔNG auto-send email — luôn DRAFT

## BƯỚC 4: Kiểm tra models/ match schema
Mỗi model cần match đúng columns trong schema_all.sql.
Pydantic models phải có Optional fields cho nullable columns.

## BƯỚC 5: Test API
pip install -r requirements.txt
python main.py
# Test: http://localhost:8767/docs
# Verify: GET /health, GET /api/customers, GET /api/dashboard/summary

## BƯỚC 6: Commit
git add -A && git commit -m "Sprint 1: DB pipeline integration + schema alignment"

## QUY TẮC BẮT BUỘC (từ CLAUDE.md)
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

## THÔNG TIN BUSINESS
- 992 customers, 2,990 contacts, 92 opportunities
- 968 quotation history records, 147 quotation revisions
- 14 active contracts, 55 milestones, 32 settlements
- 897 NAS file links, 175 customer interactions
- KHKD 2026: $19.1M revenue, 7,000 tons, 21% GM, 25 POs
- 7 product groups: HRSG, Diverter, Shipbuilding, PV, Handling, Duct, Other
```

---

## Chi tiết kỹ thuật cho Claude Code

### Schema chính thức: sql_import/schema_all.sql

32 tables theo nhóm:

**Core CRM:** sale_customers, sale_customer_contacts, sale_product_categories, sale_opportunities, sale_customer_interactions, sale_commissions, sale_digital_content

**Email:** sale_emails, sale_email_templates, sale_email_activity_log, sale_email_labels, sale_email_full

**Pipeline:** sale_quotation_revisions, sale_quotation_history, sale_quote_templates, sale_active_contracts

**Contract:** sale_contract_milestones, sale_change_orders, sale_settlements, sale_khkd_targets

**Operations:** sale_tasks, sale_follow_up_schedules, sale_nas_file_links, sale_monitored_mailboxes, sale_user_roles, sale_pm_sync_log, sale_import_log, sale_audit_log

**Intelligence:** sale_market_signals, sale_product_opportunities

**Inter-dept:** sale_inter_dept_tasks, sale_report_configs

### Gaps giữa code hiện tại vs DB

| Component | Hiện tại | Cần thêm |
|-----------|----------|----------|
| database.py | Trỏ schema.sql (16 tables) | Trỏ sql_import/schema_all.sql (32 tables) |
| routers/customers.py | sale_customers only | + sale_customer_contacts queries |
| routers/opportunities.py | sale_opportunities | + sale_quotation_history, sale_active_contracts |
| routers/emails.py | sale_emails | + sale_email_labels, sale_email_full |
| routers/ | 10 routers | + contracts.py (milestones, settlements) |
| routers/ | 10 routers | + intelligence.py (market_signals, product_opportunities) |
| models/ | 9 models | + contracts, intelligence, interactions models |
| dashboard.py | Basic stats | Full 32-table aggregate dashboard |

### ibshi1 Integration (Sprint 3)
- ibshi1 = Next.js 14 + Prisma + PostgreSQL tại :3000
- Sale→PM: tạo WorkflowTask từ email context
- PM→Sale: poll mỗi 10 phút, detect milestone changes, auto-draft reply
- Draft flow: PM Update → Auto-draft → Sale Review → Send
- KHÔNG BAO GIỜ auto-send email

### File đã có sẵn (không cần tạo lại)
- Tất cả code trong routers/, services/, workers/, models/ — chỉ cần sửa/mở rộng
- sql_import/ pipeline hoàn chỉnh (28 files, 6,700+ records)
- build_db.py — chạy để build sale.db
- schema_all.sql — 32 tables, 92 indexes, 2 views

---

## NAS Business Process Map (từ Gap Analysis 28/04/2026)

Platform hiện tại chỉ cover 4/13 business functions trên NAS. Đây là bản đồ đầy đủ:

| # | NAS Folder | Business Function | Coverage | Gap |
|---|-----------|-------------------|----------|-----|
| 00 | Thu Tu / Letter | Correspondence | PARTIAL | Email Hub covers email. NO letter registry, memo tracking, CV-IBS-xxx numbering |
| 01 | Ho So Nang Luc | Company Profile | NONE | No capability profile management or version control |
| 02 | Bao Cao | Reports | NONE | No reporting module. NAS has Weekly/Monthly/Quarterly/Yearly + Checklist |
| 03 | Bao Gia | Quotations | PARTIAL | Pipeline tracks stages. NO quotation doc generation, YYYYMM-YY.NNN revision tracking, cost breakdown |
| 04 | Marketing | Marketing | NONE | No marketing module. NAS has new product dev, partnerships, brokers, strategy |
| 05 | Hop Dong | Contracts | NONE | No contract lifecycle. NAS tracks contracts, business plans, cost estimates |
| 06 | Thu Hoi Cong No | Debt Collection | NONE | No AR module. 12 active customers (VOGT, BRADEN, THYSSEN, SHINWA, DAMEN, etc.) |
| 07 | Tai Lieu Rieng KD | Sale Internal Docs | NONE | No internal doc management for SOPs, templates |
| 08 | Don Gia Vat Tu | Material Unit Price | NONE | No material pricing database. Critical input for Auto-Quote |
| 09 | Tai Lieu KTKT | E&P Internal | N/A | Out of Sale scope — cross-dept integration later |
| 10 | Du Toan Noi Bo | Internal Cost Est. | NONE | No cost estimation module |
| 11 | Quyet Toan | Internal Settlement | NONE | No settlement/reconciliation module |
| 12 | Giao Khoan | Subcontracting | NONE | No subcontracting management |

**Coverage score: 31% (4/13 fully covered)**

## Module Roadmap (Prioritized)

### P0 — Critical (daily workflows, no digital alternative)

| Module | Name | New Tables | Est. Effort | Data Available |
|--------|------|-----------|-------------|----------------|
| M4.5 | Quotation Lifecycle | sale_quotation_revisions ✅, sale_quotation_history ✅ | 4-5 wks | 968 quotes + 147 revisions IN DB |
| M7 | Contract Lifecycle | sale_contract_milestones ✅, sale_change_orders ✅, sale_active_contracts ✅ | 3-4 wks | 14 active + 55 milestones IN DB |
| M7.1 | Capital Recovery | sale_invoices, sale_payments, sale_ar_aging (NEW) | 3-4 wks | 12 active AR customers, 32 settlements IN DB |
| M8 | Auto-Report | sale_report_configs ✅, sale_kpi_snapshots (NEW) | 3-4 wks | Dashboard data ready |

### P1 — Important (improve efficiency, manual workarounds exist)

| Module | Name | New Tables | Est. Effort | Data Available |
|--------|------|-----------|-------------|----------------|
| M4.7 | Auto-Quote Engine | sale_material_prices (NEW), sale_cost_templates (NEW) | 3-4 wks | NAS 08.DonGiaVatTu pending import |
| M10 | Digital Marketing | sale_digital_content ✅, sale_market_signals ✅ | 2-3 wks | 11 content + 18 signals IN DB |

### P2 — Nice-to-have (lower urgency)

| Module | Name | Est. Effort |
|--------|------|-------------|
| M11 | Inter-dept Tasks | 3-4 wks |
| M1.1 | Company Profile Manager | 2 wks |
| M0 | Document Registry | 1-2 wks |

**✅ = table already exists in schema_all.sql with data**

## Implementation Phases

| Phase | Timeline | Modules | Outcome |
|-------|----------|---------|---------|
| Phase 1 (CURRENT) | Now – May 2026 | Email Hub + Pipeline + Task/Project Board ✅ | Core platform live, 6,700+ records loaded |
| Phase 2 | Jun – Jul 2026 | M4.5 Quotation + M7 Contract | Full quote-to-contract workflow digitized |
| Phase 3 | Aug – Sep 2026 | M7.1 Debt Collection + M8 Auto-Report | Financial visibility + automated reporting |
| Phase 4 | Oct – Nov 2026 | M4.7 Auto-Quote + M10 Marketing | AI-powered quoting + marketing ops |
| Phase 5 | Dec 2026 – Feb 2027 | M11 + M1.1 + M0 | Full 9-function coverage (100%) |

## Tables Already in DB vs Code Needs

DB có 32 tables với data. Code hiện tại chỉ có routers/models cho 16 tables gốc. Cần mở rộng code để expose toàn bộ 32 tables qua API.

**Tables có data NHƯNG chưa có router:**
- sale_customer_contacts (2,990 records) — cần contacts.py hoặc mở rộng customers.py
- sale_customer_interactions (175) — cần interactions.py
- sale_quotation_history (968) — cần quotations.py
- sale_active_contracts (14) + sale_contract_milestones (55) + sale_settlements (32) — cần contracts.py
- sale_market_signals (18) + sale_product_opportunities (51) — cần intelligence.py
- sale_email_labels (47) + sale_email_full (108) — mở rộng emails.py
- sale_nas_file_links (897) — cần files.py hoặc mở rộng existing

**Tables có schema NHƯNG chưa có data (Phase 2+ sẽ populate):**
- sale_commissions, sale_change_orders, sale_inter_dept_tasks, sale_report_configs
- sale_quote_templates, sale_email_templates, sale_email_activity_log
- sale_follow_up_schedules

## Lệnh Claude Code cho Phase 2 (sau khi Sprint 1 xong)

```
Đọc CLAUDE.md và SPRINT1_PLAN.md.

Phase 2: Quotation Lifecycle (M4.5) + Contract Lifecycle (M7)

Data đã có trong DB:
- sale_quotation_history: 968 records (từ Quotation Record xlsx)
- sale_quotation_revisions: 147 records (từ NAS scan)  
- sale_active_contracts: 14 records (active as of Apr 2026)
- sale_contract_milestones: 55 records
- sale_settlements: 32 records

Cần build:
1. routers/quotations.py — CRUD + search + revision history + PDF export
2. routers/contracts.py — CRUD + milestone tracking + change orders + settlement
3. models/quotation.py — Pydantic models matching schema_all.sql
4. models/contract.py — Pydantic models matching schema_all.sql
5. services/quotation_engine.py — YYYYMM-YY.NNN numbering, revision workflow
6. services/contract_service.py — milestone alerts, settlement calculations
7. Cập nhật dashboard.py — thêm quotation + contract metrics
8. Cập nhật main.py — register new routers

Tuân thủ 11 rules trong CLAUDE.md. State machine cho quotation stages.
Financial changes (contract values, settlements) PHẢI audit-log.
```
