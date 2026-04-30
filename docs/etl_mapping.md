# IBS HI Sale Platform v2.1 - ETL Mapping Document

**Version:** 2.1  
**Date:** 2026-04-28  
**Architecture:** FastAPI + SQLite (dev) -> PostgreSQL (prod)  
**Total Tables:** 28 (16 existing + 12 new)  
**Data Sources:** GDrive (7,531 files, 7.2GB) + NAS (16 KINH DOANH-KTKH folders)

---

## Table of Contents

1. [Phase Overview](#phase-overview)
2. [Data Source Registry](#data-source-registry)
3. [ETL Mapping: Existing Tables (1-16)](#etl-mapping-existing-tables-1-16)
4. [ETL Mapping: New Tables (17-28)](#etl-mapping-new-tables-17-28)
5. [Dependency Graph](#dependency-graph)
6. [Import Execution Order](#import-execution-order)

---

## Phase Overview

| Phase | Priority | Tables | Target Date | Focus |
|-------|----------|--------|-------------|-------|
| Phase 1 (P0) | Critical MVP | Tables 1-16 + 19 | ASAP (4-6 wk) | Email+Task, Pipeline, Quotation Revision |
| Phase 2 (P1) | Core Expansion | Tables 17, 18, 20, 21 | Oct-Dec 2026 | Market Intel, Product-Capability, Auto-Quote, CRM 360 |
| Phase 3 (P2) | Revenue Ops | Tables 22, 23, 24, 25 | Jan-Mar 2027 | Commission, Contract Lifecycle |
| Phase 4 (P3) | Scale & Automate | Tables 26, 27, 28 | Apr-Jun 2027 | Auto-Report, Digital Marketing, Inter-dept Engine |

---

## Data Source Registry

| ID | Source | Location | Format | Size | Key Fields |
|----|--------|----------|--------|------|------------|
| DS1 | Quotation Record (updated to 08.2025).xlsx | GDrive/Sale | XLSX | ~5MB | WF dong bo: 1,036 rows x 53 cols; RECORD: 1,236 rows; type of product: 17 types |
| DS2 | 03.BaoGia_Quotations/ | NAS + GDrive | Mixed (PDF, XLSX) | ~2GB | 7,209 quotation files organized by month (202401-2026) |
| DS3 | customers.json | GDrive/Sale | JSON | 209MB | Full customer database |
| DS4 | Client List (2025).xlsx | GDrive/Sale | XLSX | ~1MB | 61 clients, codes, account manager assignments |
| DS5 | IBSHI Khach hang tiem nang_rev01.xlsx | GDrive/Sale | XLSX | ~1MB | 33 pipeline opportunities + 15 capital recovery records |
| DS6 | Sale Plan 25-26-27 (Gia khoan).xlsx | GDrive/Sale | XLSX | ~3MB | Invoice Status: 1,048 rows x 65 cols; REVISED SALES PLAN |
| DS7 | BAO CAO THANG 01.2026 - KTKH.xlsx | GDrive/Sale | XLSX | ~2MB | 7 sheets, 1,025 rows x 83 cols |
| DS8 | 02.BaoCao_Reports/ | NAS | Mixed | ~500MB | 78 report files (weekly + monthly) |
| DS9 | MKT/ | GDrive/Sale | Mixed | ~200MB | 13 files (corporate presentations, company profiles) |
| DS10 | 05.HopDong_Contracts/ | NAS + GDrive | Mixed | ~1GB | 50+ contract files (05.01 WithoutPrice, 05.02 WithPrice) |
| DS11 | Gmail API | Online | API | N/A | Monitored mailboxes (ibshi@, hieunh@) |
| DS12 | 06.ChiPhiSanXuat_CostBreakdown/ | NAS | XLSX | ~100MB | Production cost breakdowns by product |
| DS13 | 08.KHKDKeHoach_BusinessPlans/ | NAS | XLSX | ~50MB | KHKD annual plans and targets |
| DS14 | 14.PhanTichDoiThu_CompetitorAnalysis/ | NAS | Mixed | ~30MB | Competitor intelligence files |
| DS15 | 11.QuanLyKhachHang_CRM/ | NAS | Mixed | ~50MB | Legacy CRM records |
| DS16 | 12.BaoCaoTaiChinh_Financial/ | NAS | XLSX | ~100MB | Financial reports |
| DS17 | 04.MauBieu_Templates/ | NAS | Mixed | ~20MB | Standard form templates |
| DS18 | 13.TraiNghiemKhachHang_CX/ | NAS | Mixed | ~10MB | Customer experience records |
| DS19 | 10.Marketing/ | NAS | Mixed | ~200MB | Marketing materials |
| DS20 | L1 ibshi1 (PM/Workflow) | Internal API | JSON | N/A | Project codes, workflow status, 2-way sync |

---

## ETL Mapping: Existing Tables (1-16)

### Table 1: sale_customers

| Field | Value |
|-------|-------|
| **Module** | M4 Pipeline (P0), M5 CRM 360 |
| **Data Sources** | DS3 (customers.json, 209MB), DS4 (Client List 2025, 61 clients), DS1 (WF dong bo Cus-Code column) |
| **Key Transformations** | 1. Parse customers.json -> extract unique customers with dedup on name+country. 2. Merge Client List codes as `code` field. 3. Map WF dong bo Cus-Code to link existing records. 4. Normalize country names (VN -> Vietnam). 5. Set status = ACTIVE for Client List entries, PROSPECT for others. |
| **Estimated Rows** | ~988 (from Workflow 2026 master list) |
| **Import Priority** | P0 - must load first, all other tables depend on customer_id |
| **Dependencies** | None (root table) |

---

### Table 2: sale_customer_contacts

| Field | Value |
|-------|-------|
| **Module** | M5 CRM 360 |
| **Data Sources** | DS3 (customers.json contact arrays), DS4 (Client List contact columns), DS11 (Gmail from/to/cc parsing) |
| **Key Transformations** | 1. Extract contact objects from customers.json per customer. 2. Dedup on email address. 3. Mark primary contact per customer based on Client List "Account Manager" field. 4. Parse email signatures for position/phone extraction. |
| **Estimated Rows** | ~2,000 (avg 2 contacts per customer) |
| **Import Priority** | P0 |
| **Dependencies** | sale_customers |

---

### Table 3: sale_product_categories

| Field | Value |
|-------|-------|
| **Module** | M2 Product-Capability, M4 Pipeline |
| **Data Sources** | DS1 (Quotation Record "type of product" sheet, 17 types), DS13 (KHKD targets) |
| **Key Transformations** | 1. Map 17 product types to 7 KHKD categories (HRSG, DIVERTER, SHIP, PV, HANDLING, DUCT, OTHER). 2. Load FY targets from KHKD plan. 3. Seed data already defined in schema.sql. |
| **Estimated Rows** | 7 (fixed KHKD categories) + expandable to 17 subcategories |
| **Import Priority** | P0 - seed data pre-loaded |
| **Dependencies** | None (reference table) |

---

### Table 4: sale_opportunities

| Field | Value |
|-------|-------|
| **Module** | M4 Pipeline (P0) |
| **Data Sources** | DS1 (WF dong bo: 1,036 rows x 53 cols), DS5 (33 pipeline opps + 15 capital recovery), DS6 (Sale Plan REVISED), DS7 (BAO CAO THANG) |
| **Key Transformations** | 1. Map WF dong bo 53 columns to opportunity fields (PL-HD -> pl_hd, Product Group -> product_group, Stage -> stage, etc.). 2. Parse financial columns: Contract Value, Unit Price, GM%, Material/Labor/Sub costs. 3. Map customer names to sale_customers.id via fuzzy matching. 4. Calculate win_probability from stage. 5. Parse date columns (estimated_signing, start_date, end_date). 6. Import 15 capital recovery records from DS5 as WON stage. 7. Set stale_flag = 1 where last_activity > 30 days. |
| **Estimated Rows** | ~1,100 (1,036 WF + 33 pipeline + dedup) |
| **Import Priority** | P0 - central table for pipeline |
| **Dependencies** | sale_customers, sale_product_categories |

---

### Table 5: sale_emails

| Field | Value |
|-------|-------|
| **Module** | M3 Email Auto (P0) |
| **Data Sources** | DS11 (Gmail API - real-time sync) |
| **Key Transformations** | 1. Gmail API fetch via OAuth2 per monitored mailbox. 2. AI classification: email_type (RFQ, QUOTATION, FOLLOW_UP, CONTRACT, GENERAL). 3. NER extraction: customer name, project reference, amounts. 4. Auto-link to opportunity via subject/body matching. 5. Auto-link to customer via from_address domain matching. |
| **Estimated Rows** | ~5,000 initial (backfill 6 months) + ~200/week ongoing |
| **Import Priority** | P0 - core email engine |
| **Dependencies** | sale_opportunities, sale_customers, sale_monitored_mailboxes |

---

### Table 6: sale_tasks

| Field | Value |
|-------|-------|
| **Module** | M3 Email Auto (P0), M4 Pipeline |
| **Data Sources** | DS11 (auto-generated from email classification), manual creation, DS20 (L1 sync) |
| **Key Transformations** | 1. Auto-create tasks from classified emails (RFQ -> PREPARE_QUOTATION task). 2. Set SLA based on task_type (RFQ = 5 business days). 3. Route to_dept based on email_type. 4. Sync with L1 PM tasks via sale_pm_sync_log. |
| **Estimated Rows** | ~3,000 (proportional to emails + manual) |
| **Import Priority** | P0 |
| **Dependencies** | sale_opportunities, sale_emails |

---

### Table 7: sale_follow_up_schedules

| Field | Value |
|-------|-------|
| **Module** | M4.6 Smart Reminder (P0) |
| **Data Sources** | Auto-generated from sale_opportunities stage transitions |
| **Key Transformations** | 1. Create schedule on opportunity stage change. 2. Set reminder_days JSON based on schedule_type (QUOTATION_SENT: [3,7,14,30]). 3. Calculate next_follow_up from quotation_date + first reminder_day. |
| **Estimated Rows** | ~1,100 (one per active opportunity) |
| **Import Priority** | P0 |
| **Dependencies** | sale_opportunities |

---

### Table 8: sale_email_templates

| Field | Value |
|-------|-------|
| **Module** | M3 Email Auto (P0) |
| **Data Sources** | DS17 (04.MauBieu_Templates/), manual entry |
| **Key Transformations** | 1. Seed 6 default templates (already in schema.sql). 2. Import additional templates from NAS template folder. 3. Parse variable placeholders ({{customer_name}}, etc.). |
| **Estimated Rows** | ~20 (6 seeded + customizations) |
| **Import Priority** | P0 - seed data pre-loaded |
| **Dependencies** | None (reference table) |

---

### Table 9: sale_email_activity_log

| Field | Value |
|-------|-------|
| **Module** | M3 Email Auto (P0) |
| **Data Sources** | Auto-generated from email processing pipeline |
| **Key Transformations** | 1. Log every email action (CLASSIFIED, TASK_CREATED, LINKED_TO_OPP, ESCALATED). 2. Capture action_by (system vs user). 3. Store details as JSON. |
| **Estimated Rows** | ~15,000 (avg 3 actions per email) |
| **Import Priority** | P0 |
| **Dependencies** | sale_emails, sale_opportunities, sale_tasks |

---

### Table 10: sale_khkd_targets

| Field | Value |
|-------|-------|
| **Module** | M4 Pipeline - KHKD Progress Tracking |
| **Data Sources** | DS13 (08.KHKDKeHoach_BusinessPlans/), DS6 (Sale Plan REVISED) |
| **Key Transformations** | 1. Seed FY2026-2027 targets (already in schema.sql). 2. Parse KHKD plan Excel for annual targets. 3. Calculate workload_to_find = total_tons - backlog_tons. |
| **Estimated Rows** | ~5 (one per fiscal year, 3-year rolling) |
| **Import Priority** | P0 - seed data pre-loaded |
| **Dependencies** | None (reference table) |

---

### Table 11: sale_nas_file_links

| Field | Value |
|-------|-------|
| **Module** | Cross-module (file reference index) |
| **Data Sources** | NAS folder scan (all 16 KINH DOANH-KTKH folders), DS2 (quotation files), DS10 (contracts) |
| **Key Transformations** | 1. Recursive scan of NAS folders. 2. Map entity_type (OPPORTUNITY, CUSTOMER, CONTRACT, QUOTATION, REPORT). 3. Extract entity_id by parsing folder names and file naming conventions. 4. Classify file_type from extension. |
| **Estimated Rows** | ~10,000 (subset of 7,531 GDrive files relevant to sale entities) |
| **Import Priority** | P1 (bulk indexing after core data loaded) |
| **Dependencies** | sale_opportunities, sale_customers |

---

### Table 12: sale_monitored_mailboxes

| Field | Value |
|-------|-------|
| **Module** | M3 Email Auto (P0) |
| **Data Sources** | Manual configuration, Google Admin directory |
| **Key Transformations** | 1. Seed 2 initial mailboxes (already in schema.sql). 2. Add mailboxes as employees are onboarded. 3. OAuth2 token management. |
| **Estimated Rows** | ~10 (sales + KTKH team mailboxes) |
| **Import Priority** | P0 - seed data pre-loaded |
| **Dependencies** | None (configuration table) |

---

### Table 13: sale_user_roles

| Field | Value |
|-------|-------|
| **Module** | Cross-module (access control) |
| **Data Sources** | Manual configuration, DS20 (L1 user sync via l1_user_id) |
| **Key Transformations** | 1. Seed 5 initial users (already in schema.sql). 2. Sync with L1 ibshi1 user table. 3. Map department codes (SALE, KTKH, KT, SX). |
| **Estimated Rows** | ~25 (all sale-related users across departments) |
| **Import Priority** | P0 - seed data pre-loaded |
| **Dependencies** | None (configuration table) |

---

### Table 14: sale_pm_sync_log

| Field | Value |
|-------|-------|
| **Module** | Cross-module (L1-L2 integration) |
| **Data Sources** | DS20 (L1 ibshi1 PM/Workflow API), auto-generated on sync events |
| **Key Transformations** | 1. Log every L1<->L2 sync event. 2. Map opportunity_id to L1 project_code. 3. Store payload as JSON diff. 4. Track PENDING drafts for manual review. |
| **Estimated Rows** | ~5,000/year (proportional to opportunity updates) |
| **Import Priority** | P0 (sync infrastructure) |
| **Dependencies** | sale_opportunities |

---

### Table 15: sale_import_log

| Field | Value |
|-------|-------|
| **Module** | Cross-module (data governance) |
| **Data Sources** | Auto-generated on every ETL run |
| **Key Transformations** | 1. Create one record per import batch. 2. Track success/failure counts. 3. Store error details as JSON. |
| **Estimated Rows** | ~500 (grows with each import cycle) |
| **Import Priority** | P0 (mandatory audit) |
| **Dependencies** | None (audit table) |

---

### Table 16: sale_audit_log

| Field | Value |
|-------|-------|
| **Module** | Cross-module (data governance) |
| **Data Sources** | Auto-generated on every data mutation |
| **Key Transformations** | 1. Trigger-based capture of old/new values. 2. Focus on financial field changes (contract_value, gm_percent, stage). 3. Track changed_by from session context. |
| **Estimated Rows** | ~50,000/year (grows with platform usage) |
| **Import Priority** | P0 (mandatory audit) |
| **Dependencies** | None (audit table) |

---

## ETL Mapping: New Tables (17-28)

### Table 17: sale_market_signals

| Field | Value |
|-------|-------|
| **Module** | M1 Market Intelligence |
| **Data Sources** | DS14 (14.PhanTichDoiThu_CompetitorAnalysis/), web scraping (industry portals), manual entry, news RSS feeds |
| **Key Transformations** | 1. Parse competitor analysis files for structured data (competitor name, market move, date). 2. NLP extraction from industry news articles. 3. AI relevance scoring (0.0-1.0) based on product group match and customer overlap. 4. Auto-link to related_customer_id via entity recognition. 5. Set expires_at for tender notices based on submission deadlines. 6. Tag with product group from sale_product_categories. |
| **Estimated Rows** | ~500 initial (backfill from NAS) + ~50/month ongoing |
| **Import Priority** | P1 (Phase 2) |
| **Dependencies** | sale_customers, sale_product_categories |

---

### Table 18: sale_product_opportunities

| Field | Value |
|-------|-------|
| **Module** | M2 Product-Capability |
| **Data Sources** | DS1 (Quotation Record "type of product" x "Cus-Code" matrix), DS4 (Client List), DS5 (pipeline opps), historical sale_opportunities aggregation |
| **Key Transformations** | 1. Cross-join sale_product_categories x sale_customers to generate initial matrix. 2. Calculate fit_score from historical win rate per product-customer pair. 3. Aggregate past_project_count, avg_unit_price, avg_gm_pct, total_revenue from sale_opportunities WHERE stage = 'WON'. 4. Identify capability gaps where customer requested product but IBS has no track record. 5. Flag is_strategic = 1 for top-20 revenue combinations. 6. Extract competitor_threat from sale_opportunities.competitor field. |
| **Estimated Rows** | ~2,000 (7 categories x ~300 active customers, filtered to relevant pairs) |
| **Import Priority** | P1 (Phase 2) |
| **Dependencies** | sale_customers, sale_product_categories, sale_opportunities (for historical aggregation) |

---

### Table 19: sale_quotation_revisions

| Field | Value |
|-------|-------|
| **Module** | M4.5 Quotation Revision (P0) |
| **Data Sources** | DS1 (RECORD sheet: 1,236 rows), DS2 (03.BaoGia_Quotations/ 7,209 files), DS1 (WF dong bo: quotation dates and values) |
| **Key Transformations** | 1. Parse RECORD sheet: map each row to an opportunity via project name + customer fuzzy match. 2. Extract revision_number from quotation file naming convention (QT-xxx-R1, R2, R3). 3. Scan 03.BaoGia_Quotations/ folder structure: group files by opportunity, assign revision sequence. 4. Calculate price_delta_pct = (current_price - previous_price) / previous_price * 100. 5. Extract financial fields (unit_price, total_value, material/labor/overhead) from quotation Excel files where available. 6. Map nas_file_path from folder structure. 7. Set customer_response based on stage progression in sale_opportunities. |
| **Estimated Rows** | ~3,500 (1,236 base records + avg 2.8 revisions per opportunity from 7,209 files) |
| **Import Priority** | P0 (Phase 1 - core quotation tracking) |
| **Dependencies** | sale_opportunities, sale_customers |

---

### Table 20: sale_quote_templates

| Field | Value |
|-------|-------|
| **Module** | M4.7 Auto-Quote Engine |
| **Data Sources** | DS12 (06.ChiPhiSanXuat_CostBreakdown/), DS17 (04.MauBieu_Templates/), historical sale_quotation_revisions aggregation |
| **Key Transformations** | 1. Parse cost breakdown files per product category: extract material%, labor%, overhead%, subcontract% splits. 2. Calculate base_unit_price as median of historical quotations per product_type x weight_range. 3. Define weight ranges from historical distribution (e.g., <50t, 50-200t, 200-500t, >500t). 4. Extract complexity_factor from actual vs estimated cost ratios. 5. Build cost_breakdown_json from template files in 04.MauBieu_Templates/. 6. Set target_gm_pct from KHKD targets (21% default). |
| **Estimated Rows** | ~50 (7 product categories x ~7 weight ranges, plus variants) |
| **Import Priority** | P1 (Phase 2) |
| **Dependencies** | sale_product_categories, sale_quotation_revisions (for historical analysis) |

---

### Table 21: sale_customer_interactions

| Field | Value |
|-------|-------|
| **Module** | M5 CRM 360 |
| **Data Sources** | DS8 (02.BaoCao_Reports/ - 78 files), DS18 (13.TraiNghiemKhachHang_CX/), DS15 (11.QuanLyKhachHang_CRM/), DS11 (Gmail meeting invites), manual entry |
| **Key Transformations** | 1. Parse monthly/weekly reports for meeting and visit records: extract date, customer, attendees, summary. 2. Import CRM folder records as historical interactions. 3. Extract meeting invites from Gmail (calendar events with customer attendees). 4. NLP summarization of meeting minutes from NAS files. 5. AI sentiment scoring (0.0-1.0) from interaction summaries. 6. Link to opportunity_id via customer + date proximity matching. 7. Map attendees_ibs to sale_user_roles entries. |
| **Estimated Rows** | ~3,000 initial (backfill from reports + CRM) + ~100/month ongoing |
| **Import Priority** | P1 (Phase 2) |
| **Dependencies** | sale_customers, sale_customer_contacts, sale_opportunities |

---

### Table 22: sale_commissions

| Field | Value |
|-------|-------|
| **Module** | M6 Commission |
| **Data Sources** | DS6 (Sale Plan 25-26-27 Invoice Status: 1,048 rows x 65 cols, REVISED SALES PLAN), sale_opportunities (GP fields) |
| **Key Transformations** | 1. Parse Invoice Status sheet: extract contract value, GP amount, salesperson assignment. 2. Calculate commission_tier: TIER_1 (<15% GM), TIER_2 (15-25% GM), TIER_3 (>25% GM). 3. Apply commission_rate per tier (configured, e.g., 1%/2%/3%). 4. Calculate commission_amount = gm_value * commission_rate. 5. Split commissions for salesperson_role = LEAD (70%) vs SUPPORT (30%). 6. Map fiscal_quarter from opportunity signing/delivery dates. 7. Convert USD to VND at current exchange rate. |
| **Estimated Rows** | ~1,500 (one per WON opportunity x salesperson, historical + ongoing) |
| **Import Priority** | P2 (Phase 3) |
| **Dependencies** | sale_opportunities, sale_user_roles |

---

### Table 23: sale_contract_milestones

| Field | Value |
|-------|-------|
| **Module** | M7.1 Capital Recovery |
| **Data Sources** | DS10 (05.HopDong_Contracts/ - 50+ files), DS6 (Invoice Status: 1,048 rows x 65 cols), DS7 (BAO CAO THANG: 1,025 rows x 83 cols), DS5 (15 capital recovery records) |
| **Key Transformations** | 1. Parse Invoice Status for milestone-level payment data: invoice number, amount, status, dates. 2. Extract payment terms from contract files (30/60/90 day NET). 3. Map milestone_type from invoice description (ADVANCE = deposit, DELIVERY = shipment, FAT/SAT = testing). 4. Calculate overdue_days = today - (invoice_date + payment_term_days) WHERE payment not received. 5. Import 15 capital recovery records from DS5 with their milestone structures. 6. Link to opportunity_id via contract number matching. 7. Parse BAO CAO THANG for actual payment receipt dates. |
| **Estimated Rows** | ~4,000 (avg 4 milestones per contract x ~1,000 historical contracts) |
| **Import Priority** | P2 (Phase 3) |
| **Dependencies** | sale_opportunities |

---

### Table 24: sale_change_orders

| Field | Value |
|-------|-------|
| **Module** | M7.2 Change Orders |
| **Data Sources** | DS10 (05.HopDong_Contracts/ - amendment files), manual entry from project managers |
| **Key Transformations** | 1. Scan contract folders for amendment/change order documents. 2. Parse change order PDFs/Excel for scope, value, and schedule changes. 3. Calculate delta_value_usd = revised - original. 4. Calculate impact_on_gm_pct from cost impact analysis. 5. Link to opportunity_id via contract reference. 6. Auto-number change_order_number per opportunity. |
| **Estimated Rows** | ~300 (estimated ~30% of contracts have change orders, avg 1-2 each) |
| **Import Priority** | P2 (Phase 3) |
| **Dependencies** | sale_opportunities |

---

### Table 25: sale_settlements

| Field | Value |
|-------|-------|
| **Module** | M7.3 Settlement |
| **Data Sources** | DS6 (Invoice Status for actuals), DS12 (06.ChiPhiSanXuat_CostBreakdown/ for actual costs), DS16 (12.BaoCaoTaiChinh_Financial/ for reconciliation), DS7 (BAO CAO THANG for payment tracking) |
| **Key Transformations** | 1. Pull planned values from sale_opportunities (contract_value, gm_percent). 2. Aggregate actual costs from cost breakdown files per project. 3. Calculate actual_total_cost = material + labor + overhead + subcontract. 4. Calculate actual_gm_value = actual_revenue - actual_total_cost. 5. Calculate variances: revenue_variance = actual - planned. 6. Aggregate total_invoiced and total_received from sale_contract_milestones. 7. Calculate outstanding_amount = total_invoiced - total_received. 8. Track retention held/released from contract payment terms. |
| **Estimated Rows** | ~500 (completed/settled projects, growing as projects finish) |
| **Import Priority** | P2 (Phase 3) |
| **Dependencies** | sale_opportunities, sale_contract_milestones, sale_change_orders |

---

### Table 26: sale_report_configs

| Field | Value |
|-------|-------|
| **Module** | M8 Auto-Report |
| **Data Sources** | DS8 (02.BaoCao_Reports/ - 78 files for template analysis), manual configuration |
| **Key Transformations** | 1. Analyze existing report structure from 02.BaoCao_Reports/ folder to define standard report types. 2. Map BAO CAO THANG 7-sheet structure to template_config JSON (which tables, filters, groupings). 3. Configure default schedules: WEEKLY_PIPELINE = every Monday, MONTHLY_KTKH = 1st of month. 4. Set recipients from sale_user_roles WHERE role IN ('ADMIN', 'MANAGER'). 5. Define NAS output paths following existing folder conventions. |
| **Estimated Rows** | ~15 (standard report configurations) |
| **Import Priority** | P3 (Phase 4) |
| **Dependencies** | sale_user_roles (for recipients) |

---

### Table 27: sale_digital_content

| Field | Value |
|-------|-------|
| **Module** | M10 Digital Marketing |
| **Data Sources** | DS9 (MKT/ - 13 files), DS19 (10.Marketing/ on NAS) |
| **Key Transformations** | 1. Scan MKT/ folder: classify each file by content_type (BROCHURE, PRESENTATION, COMPANY_PROFILE). 2. Extract metadata: title, language, file format, file size. 3. Map product_category_id from content analysis (which products are featured). 4. Index NAS 10.Marketing/ folder for additional assets. 5. Set version = 1 and is_latest = 1 for current files; deprecate older versions. 6. Generate thumbnail_path for visual preview in UI. |
| **Estimated Rows** | ~100 (13 GDrive + NAS marketing assets + historical versions) |
| **Import Priority** | P3 (Phase 4) |
| **Dependencies** | sale_product_categories |

---

### Table 28: sale_inter_dept_tasks

| Field | Value |
|-------|-------|
| **Module** | M11 Inter-dept Task Engine |
| **Data Sources** | Auto-generated from workflows, sale_tasks escalations, manual creation |
| **Key Transformations** | 1. Create structured workflows from common patterns: RFQ -> KTKH cost estimation -> SX capacity check -> SALE quotation. 2. Define SLA hours per workflow_type (RFQ_REVIEW = 48h, COST_ESTIMATION = 72h). 3. Auto-route to_dept based on workflow_type rules. 4. Link to sale_tasks.id for tasks that trigger cross-dept workflows. 5. Track step_number progression through multi-step workflows. 6. Calculate sla_met based on completed_at vs due_date. |
| **Estimated Rows** | ~2,000/year (proportional to complex opportunities requiring cross-dept work) |
| **Import Priority** | P3 (Phase 4) |
| **Dependencies** | sale_tasks, sale_opportunities, sale_user_roles |

---

## Dependency Graph

```
Level 0 (No dependencies - load first):
  sale_customers
  sale_product_categories
  sale_khkd_targets
  sale_email_templates
  sale_monitored_mailboxes
  sale_user_roles
  sale_import_log
  sale_audit_log

Level 1 (Depends on Level 0):
  sale_customer_contacts       <- sale_customers
  sale_opportunities           <- sale_customers, sale_product_categories
  sale_market_signals          <- sale_customers, sale_product_categories
  sale_digital_content         <- sale_product_categories
  sale_report_configs          <- sale_user_roles

Level 2 (Depends on Level 1):
  sale_emails                  <- sale_opportunities, sale_customers, sale_monitored_mailboxes
  sale_follow_up_schedules     <- sale_opportunities
  sale_quotation_revisions     <- sale_opportunities
  sale_contract_milestones     <- sale_opportunities
  sale_change_orders           <- sale_opportunities
  sale_commissions             <- sale_opportunities, sale_user_roles
  sale_product_opportunities   <- sale_customers, sale_product_categories, sale_opportunities
  sale_customer_interactions   <- sale_customers, sale_customer_contacts, sale_opportunities
  sale_nas_file_links          <- sale_opportunities, sale_customers
  sale_pm_sync_log             <- sale_opportunities

Level 3 (Depends on Level 2):
  sale_tasks                   <- sale_opportunities, sale_emails
  sale_email_activity_log      <- sale_emails, sale_opportunities, sale_tasks
  sale_quote_templates         <- sale_product_categories, sale_quotation_revisions
  sale_settlements             <- sale_opportunities, sale_contract_milestones, sale_change_orders

Level 4 (Depends on Level 3):
  sale_inter_dept_tasks        <- sale_tasks, sale_opportunities, sale_user_roles
```

---

## Import Execution Order

The following is the recommended ETL execution sequence, respecting all foreign key dependencies:

### Batch 1: Foundation (Day 1)
1. `sale_import_log` - Initialize audit tracking
2. `sale_audit_log` - Initialize change tracking
3. `sale_product_categories` - 7 KHKD categories (seed data)
4. `sale_khkd_targets` - FY targets (seed data)
5. `sale_email_templates` - 6 standard templates (seed data)
6. `sale_monitored_mailboxes` - 2 initial mailboxes (seed data)
7. `sale_user_roles` - 5 initial users (seed data)
8. `sale_customers` - 988 customers from DS3 + DS4

### Batch 2: Core Relationships (Day 2-3)
9. `sale_customer_contacts` - ~2,000 contacts from DS3 + DS4
10. `sale_opportunities` - ~1,100 pipeline records from DS1 + DS5

### Batch 3: Email Engine (Day 4-5)
11. `sale_emails` - Gmail backfill (~5,000 emails)
12. `sale_follow_up_schedules` - Auto-generate from opportunities
13. `sale_quotation_revisions` - ~3,500 from DS1 + DS2

### Batch 4: Task Engine (Day 6-7)
14. `sale_tasks` - ~3,000 auto-generated + historical
15. `sale_email_activity_log` - ~15,000 from email processing
16. `sale_pm_sync_log` - Initialize L1-L2 sync

### Batch 5: File Index (Week 2)
17. `sale_nas_file_links` - ~10,000 from NAS scan

### Batch 6: Phase 2 Tables (Oct-Dec 2026)
18. `sale_market_signals` - ~500 from DS14
19. `sale_product_opportunities` - ~2,000 from cross-analysis
20. `sale_quote_templates` - ~50 from DS12 + DS17
21. `sale_customer_interactions` - ~3,000 from DS8 + DS15

### Batch 7: Phase 3 Tables (Jan-Mar 2027)
22. `sale_commissions` - ~1,500 from DS6
23. `sale_contract_milestones` - ~4,000 from DS10 + DS6
24. `sale_change_orders` - ~300 from DS10
25. `sale_settlements` - ~500 calculated from actuals

### Batch 8: Phase 4 Tables (Apr-Jun 2027)
26. `sale_report_configs` - ~15 manual configuration
27. `sale_digital_content` - ~100 from DS9 + DS19
28. `sale_inter_dept_tasks` - Auto-generated from workflows

---

## Notes

- **Deduplication Strategy:** All imports use fuzzy matching (Levenshtein distance + normalized names) for customer and project matching. Threshold: 85% similarity = auto-merge, 70-85% = manual review, <70% = new record.
- **Currency Handling:** All REAL money fields store USD values. VND equivalents use exchange rate from sale_khkd_targets or daily rate. PostgreSQL migration will use NUMERIC(15,2).
- **Date Format:** All TEXT date fields use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) via SQLite datetime() function.
- **JSON Fields:** Fields storing arrays/objects (tags, attendees, cost_breakdown_json, etc.) use JSON text. PostgreSQL migration will use JSONB.
- **NAS Paths:** All nas_*_path fields store relative paths from NAS root (//NAS/KINH DOANH-KTKH/). Files remain on NAS; only paths are indexed.
- **L1 Sync:** sale_pm_sync_log manages bidirectional sync with ibshi1 (L1). Opportunities map to L1 projects via project_code. Draft sync requires manual review before commit.
