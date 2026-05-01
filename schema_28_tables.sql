-- ═══════════════════════════════════════════════════════════════════════════════
-- IBS HI SALE PLATFORM v2.1 - 12 NEW TABLES (Tables 17-28)
-- Extends schema.sql (16 existing tables) to complete 28-table architecture
-- Covers: M1, M2, M4.5, M4.7, M5, M6, M7, M8, M10, M11
-- Generated: 2026-04-28
-- Convention: TEXT PK (UUID), TEXT dates, REAL money, IF NOT EXISTS guards
-- ═══════════════════════════════════════════════════════════════════════════════


-- ═══════════════════════════════════════════════════════════════
-- TABLE 17: sale_market_signals                        [M1 Market Intelligence]
-- Captures competitor alerts, market events, industry news, and tender notices
-- Sources: 14.PhanTichDoiThu_CompetitorAnalysis/, web scraping, manual entry
-- Feeds: opportunity scoring, competitive positioning, strategic planning
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_market_signals (
    id              TEXT PRIMARY KEY,
    signal_type     TEXT NOT NULL,           -- COMPETITOR_MOVE | TENDER_NOTICE | INDUSTRY_NEWS | PRICE_CHANGE | REGULATION | MARKET_EVENT
    title           TEXT NOT NULL,
    description     TEXT,
    source_url      TEXT,
    source_name     TEXT,                    -- e.g. 'EPVN', 'PetroVietnam Portal', manual
    region          TEXT,                    -- geographic relevance
    industry        TEXT,                    -- steel, shipbuilding, energy, etc.
    competitor_name TEXT,                    -- nullable, only for COMPETITOR_MOVE
    relevance_score REAL,                   -- 0.0-1.0 AI-assigned relevance
    impact_level    TEXT DEFAULT 'MEDIUM',   -- LOW | MEDIUM | HIGH | CRITICAL
    related_product_group TEXT,             -- FK concept to sale_product_categories.code
    related_customer_id   TEXT REFERENCES sale_customers(id),
    expires_at      TEXT,                    -- for tender notices with deadlines
    is_actionable   INTEGER DEFAULT 1,
    actioned_by     TEXT,
    actioned_at     TEXT,
    tags            TEXT,                    -- JSON array of tags
    created_by      TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sms_type ON sale_market_signals(signal_type);
CREATE INDEX IF NOT EXISTS idx_sms_impact ON sale_market_signals(impact_level);
CREATE INDEX IF NOT EXISTS idx_sms_region ON sale_market_signals(region);
CREATE INDEX IF NOT EXISTS idx_sms_created ON sale_market_signals(created_at);
CREATE INDEX IF NOT EXISTS idx_sms_customer ON sale_market_signals(related_customer_id);
CREATE INDEX IF NOT EXISTS idx_sms_expires ON sale_market_signals(expires_at);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 18: sale_product_opportunities                 [M2 Product-Capability]
-- Product-customer fit matrix: maps IBS capabilities to customer needs
-- Sources: Quotation Record "type of product" (17 types), Client List,
--          IBSHI Khach hang tiem nang_rev01.xlsx (33 pipeline opps)
-- Feeds: auto-quote suggestions, cross-sell alerts, capability gap analysis
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_product_opportunities (
    id              TEXT PRIMARY KEY,
    product_category_id TEXT REFERENCES sale_product_categories(id),
    customer_id     TEXT REFERENCES sale_customers(id),
    fit_score       REAL,                   -- 0.0-1.0 capability match
    capability_status TEXT DEFAULT 'FULL',  -- FULL | PARTIAL | GAP | DEVELOPING
    gap_description TEXT,                   -- what capability is missing
    past_project_count INTEGER DEFAULT 0,   -- historical track record
    last_quoted_at  TEXT,
    last_won_at     TEXT,
    avg_unit_price  REAL,                   -- NUMERIC(15,2) historical avg
    avg_gm_pct      REAL,                   -- historical avg GM%
    total_revenue   REAL,                   -- NUMERIC(15,2) lifetime revenue from this combo
    total_weight_ton REAL,                  -- lifetime tons
    competitor_threat TEXT,                 -- primary competitor for this product-customer pair
    notes           TEXT,
    is_strategic    INTEGER DEFAULT 0,      -- flagged for strategic focus
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_spo_product ON sale_product_opportunities(product_category_id);
CREATE INDEX IF NOT EXISTS idx_spo_customer ON sale_product_opportunities(customer_id);
CREATE INDEX IF NOT EXISTS idx_spo_fit ON sale_product_opportunities(fit_score);
CREATE INDEX IF NOT EXISTS idx_spo_strategic ON sale_product_opportunities(is_strategic);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 19: sale_quotation_revisions                   [M4.5 Quotation Revision]
-- Tracks revision history per opportunity: price changes, scope edits
-- Sources: 03.BaoGia_Quotations/ (7,209 files), Quotation Record RECORD sheet
--          (1,236 rows), WF dong bo (1,036 rows x 53 cols)
-- Feeds: revision analytics, price drift detection, negotiation patterns
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_quotation_revisions (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),  -- nullable for historical import
    revision_number INTEGER NOT NULL DEFAULT 1,
    revision_date   TEXT NOT NULL,
    revision_reason TEXT,                   -- SCOPE_CHANGE | PRICE_NEGOTIATION | MATERIAL_UPDATE | CUSTOMER_REQUEST | INTERNAL_REVIEW
    quotation_ref   TEXT,                   -- e.g. "QT-2026-001-R2"
    weight_ton      REAL,
    unit_price_usd  REAL,                   -- NUMERIC(15,2)
    total_value_usd REAL,                   -- NUMERIC(15,2)
    total_value_vnd REAL,                   -- NUMERIC(15,2)
    material_cost   REAL,                   -- NUMERIC(15,2)
    labor_cost      REAL,                   -- NUMERIC(15,2)
    overhead_cost   REAL,                   -- NUMERIC(15,2)
    gm_percent      REAL,
    gm_value        REAL,                   -- NUMERIC(15,2)
    scope_summary   TEXT,                   -- what changed in scope
    price_delta_pct REAL,                   -- % change from previous revision
    nas_file_path   TEXT,                   -- path to quotation PDF on NAS
    sent_to         TEXT,                   -- customer contact who received it
    sent_at         TEXT,
    customer_response TEXT,                 -- PENDING | ACCEPTED | COUNTER | REJECTED | NO_RESPONSE
    response_date   TEXT,
    valid_until     TEXT,                   -- quotation validity date
    prepared_by     TEXT,
    approved_by     TEXT,
    approved_at     TEXT,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sqr_opp ON sale_quotation_revisions(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_sqr_ref ON sale_quotation_revisions(quotation_ref);
CREATE INDEX IF NOT EXISTS idx_sqr_date ON sale_quotation_revisions(revision_date);
CREATE INDEX IF NOT EXISTS idx_sqr_response ON sale_quotation_revisions(customer_response);
CREATE UNIQUE INDEX IF NOT EXISTS idx_sqr_opp_rev ON sale_quotation_revisions(opportunity_id, revision_number);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 20: sale_quote_templates                       [M4.7 Auto-Quote Engine]
-- Reusable cost breakdown templates and standard pricing for auto-quoting
-- Sources: 06.ChiPhiSanXuat_CostBreakdown/, 04.MauBieu_Templates/,
--          historical quotation data, product category benchmarks
-- Feeds: one-click quote generation, cost estimation, pricing consistency
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_quote_templates (
    id              TEXT PRIMARY KEY,
    template_name   TEXT NOT NULL,
    product_category_id TEXT REFERENCES sale_product_categories(id),
    product_type    TEXT,                   -- specific product variant
    weight_range_min REAL,                  -- applicable tonnage range
    weight_range_max REAL,
    base_unit_price REAL,                   -- NUMERIC(15,2) USD/ton baseline
    material_pct    REAL,                   -- % of total for material
    labor_pct       REAL,                   -- % of total for labor
    overhead_pct    REAL,                   -- % of total for overhead
    subcontract_pct REAL,                   -- % of total for subcontracting
    target_gm_pct   REAL,                   -- target gross margin
    complexity_factor REAL DEFAULT 1.0,     -- multiplier for complex jobs
    lead_time_weeks INTEGER,                -- standard production lead time
    cost_breakdown_json TEXT,               -- detailed line-item JSON
    assumptions     TEXT,                   -- pricing assumptions text
    currency        TEXT DEFAULT 'USD',
    valid_from      TEXT,
    valid_until     TEXT,
    is_active       INTEGER DEFAULT 1,
    version         INTEGER DEFAULT 1,
    created_by      TEXT,
    approved_by     TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sqt_product ON sale_quote_templates(product_category_id);
CREATE INDEX IF NOT EXISTS idx_sqt_type ON sale_quote_templates(product_type);
CREATE INDEX IF NOT EXISTS idx_sqt_active ON sale_quote_templates(is_active);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 21: sale_customer_interactions                 [M5 CRM 360]
-- Unified interaction log: meetings, calls, site visits, exhibitions
-- Sources: BaoCao_Reports/ (78 files), email activity log, manual entry,
--          13.TraiNghiemKhachHang_CX/
-- Feeds: CRM 360 timeline, relationship health scoring, account insights
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_customer_interactions (
    id              TEXT PRIMARY KEY,
    customer_id     TEXT NOT NULL REFERENCES sale_customers(id),
    contact_id      TEXT REFERENCES sale_customer_contacts(id),
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    interaction_type TEXT NOT NULL,          -- MEETING | CALL | SITE_VISIT | EXHIBITION | FACTORY_TOUR | VIDEO_CALL | LUNCH | EMAIL
    interaction_date TEXT NOT NULL,
    duration_minutes INTEGER,
    location        TEXT,                    -- office, customer site, exhibition name
    attendees_ibs   TEXT,                   -- JSON array of IBS attendees
    attendees_customer TEXT,                -- JSON array of customer attendees
    subject         TEXT NOT NULL,
    summary         TEXT,                   -- meeting notes / call summary
    outcome         TEXT,                   -- POSITIVE | NEUTRAL | NEGATIVE | FOLLOW_UP_NEEDED
    next_action     TEXT,                   -- agreed next step
    next_action_due TEXT,                   -- deadline for next step
    sentiment_score REAL,                   -- AI-derived 0.0-1.0
    nas_file_path   TEXT,                   -- meeting minutes on NAS
    attachments     TEXT,                   -- JSON array of attachment refs
    recorded_by     TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sci_customer ON sale_customer_interactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_sci_contact ON sale_customer_interactions(contact_id);
CREATE INDEX IF NOT EXISTS idx_sci_opp ON sale_customer_interactions(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_sci_type ON sale_customer_interactions(interaction_type);
CREATE INDEX IF NOT EXISTS idx_sci_date ON sale_customer_interactions(interaction_date);
CREATE INDEX IF NOT EXISTS idx_sci_outcome ON sale_customer_interactions(outcome);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 22: sale_commissions                           [M6 Commission]
-- GP-based commission calculation with tiers and payout tracking
-- Sources: Sale Plan 25-26-27 (Gia khoan) Invoice Status (1,048 rows x 65 cols),
--          REVISED SALES PLAN, sale_opportunities GP fields
-- Feeds: salesperson compensation, GP incentive dashboards, payout reports
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_commissions (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),  -- nullable for historical import
    salesperson     TEXT NOT NULL,           -- assigned_to from opportunity
    salesperson_role TEXT,                   -- LEAD | SUPPORT | REFERRAL
    fiscal_year     TEXT NOT NULL,
    fiscal_quarter  TEXT,                    -- Q1, Q2, Q3, Q4
    contract_value_usd REAL,                -- NUMERIC(15,2) from opportunity
    gm_value_usd   REAL,                   -- NUMERIC(15,2) actual GM
    gm_percent      REAL,
    commission_tier TEXT,                    -- TIER_1 (<15% GM) | TIER_2 (15-25%) | TIER_3 (>25%)
    commission_rate REAL,                   -- % rate applied
    commission_amount_usd REAL,             -- NUMERIC(15,2) calculated payout
    commission_amount_vnd REAL,             -- NUMERIC(15,2) VND equivalent
    bonus_amount    REAL,                   -- NUMERIC(15,2) extra bonus if applicable
    adjustment      REAL,                   -- NUMERIC(15,2) manual adjustment
    adjustment_reason TEXT,
    status          TEXT DEFAULT 'CALCULATED', -- CALCULATED | APPROVED | PAID | DISPUTED | CANCELLED
    calculation_date TEXT,
    approved_by     TEXT,
    approved_at     TEXT,
    paid_at         TEXT,
    payment_ref     TEXT,                   -- internal payment reference
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_scom_opp ON sale_commissions(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_scom_person ON sale_commissions(salesperson);
CREATE INDEX IF NOT EXISTS idx_scom_fy ON sale_commissions(fiscal_year);
CREATE INDEX IF NOT EXISTS idx_scom_status ON sale_commissions(status);
CREATE INDEX IF NOT EXISTS idx_scom_tier ON sale_commissions(commission_tier);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 23: sale_contract_milestones                   [M7.1 Capital Recovery]
-- Delivery milestones, payment terms, and invoice scheduling per contract
-- Sources: 05.HopDong_Contracts/ (50+ files), Sale Plan Invoice Status,
--          BAO CAO THANG 01.2026 - KTKH (1,025 rows x 83 cols)
-- Feeds: capital recovery tracking, cash flow forecasting, delivery dashboards
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_contract_milestones (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),  -- nullable for historical import
    milestone_number INTEGER NOT NULL,
    milestone_type  TEXT NOT NULL,           -- ADVANCE | DELIVERY | FAT | SAT | FINAL | RETENTION
    title           TEXT NOT NULL,
    description     TEXT,
    planned_date    TEXT,
    actual_date     TEXT,
    weight_ton      REAL,                   -- tonnage for this milestone
    invoice_amount_usd REAL,                -- NUMERIC(15,2)
    invoice_amount_vnd REAL,                -- NUMERIC(15,2)
    payment_term_days INTEGER,              -- e.g. 30, 60, 90
    invoice_number  TEXT,
    invoice_date    TEXT,
    invoice_status  TEXT DEFAULT 'NOT_INVOICED', -- NOT_INVOICED | INVOICED | PARTIALLY_PAID | PAID | OVERDUE | DISPUTED
    payment_received_date TEXT,
    payment_amount  REAL,                   -- NUMERIC(15,2) actual received
    overdue_days    INTEGER DEFAULT 0,
    penalty_amount  REAL,                   -- NUMERIC(15,2) late penalty if any
    nas_contract_path TEXT,
    nas_invoice_path TEXT,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_scm_opp ON sale_contract_milestones(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_scm_type ON sale_contract_milestones(milestone_type);
CREATE INDEX IF NOT EXISTS idx_scm_status ON sale_contract_milestones(invoice_status);
CREATE INDEX IF NOT EXISTS idx_scm_planned ON sale_contract_milestones(planned_date);
CREATE INDEX IF NOT EXISTS idx_scm_overdue ON sale_contract_milestones(overdue_days);
CREATE UNIQUE INDEX IF NOT EXISTS idx_scm_opp_num ON sale_contract_milestones(opportunity_id, milestone_number);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 24: sale_change_orders                         [M7.2 Change Orders]
-- Scope changes, price adjustments, and contract amendments
-- Sources: 05.HopDong_Contracts/, manual entry from project managers
-- Feeds: margin erosion alerts, scope creep tracking, contract audit trail
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_change_orders (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),  -- nullable for historical import
    change_order_number INTEGER NOT NULL,
    co_ref          TEXT,                   -- e.g. "CO-2026-001"
    change_type     TEXT NOT NULL,           -- SCOPE_ADD | SCOPE_REDUCE | PRICE_ADJUST | SCHEDULE_CHANGE | SPEC_CHANGE
    title           TEXT NOT NULL,
    description     TEXT,
    requested_by    TEXT,                   -- customer or internal
    request_date    TEXT,
    original_value_usd REAL,                -- NUMERIC(15,2) before change
    revised_value_usd  REAL,                -- NUMERIC(15,2) after change
    delta_value_usd REAL,                   -- NUMERIC(15,2) difference
    original_weight_ton REAL,
    revised_weight_ton  REAL,
    delta_weight_ton REAL,
    impact_on_gm_pct REAL,                  -- GM% impact
    schedule_impact_days INTEGER,            -- schedule shift in days
    status          TEXT DEFAULT 'DRAFT',    -- DRAFT | SUBMITTED | CUSTOMER_APPROVED | INTERNAL_APPROVED | REJECTED | IMPLEMENTED
    approved_by_customer TEXT,
    approved_by_internal TEXT,
    approved_at     TEXT,
    implemented_at  TEXT,
    nas_file_path   TEXT,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sco_opp ON sale_change_orders(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_sco_status ON sale_change_orders(status);
CREATE INDEX IF NOT EXISTS idx_sco_type ON sale_change_orders(change_type);
CREATE INDEX IF NOT EXISTS idx_sco_date ON sale_change_orders(request_date);
CREATE UNIQUE INDEX IF NOT EXISTS idx_sco_opp_num ON sale_change_orders(opportunity_id, change_order_number);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 25: sale_settlements                           [M7.3 Settlement]
-- Final project reconciliation: planned vs actual cost/revenue/margin
-- Sources: Sale Plan Invoice Status, BAO CAO THANG reports,
--          06.ChiPhiSanXuat_CostBreakdown/, 12.BaoCaoTaiChinh_Financial/
-- Feeds: project profitability analysis, lessons learned, forecasting accuracy
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_settlements (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),  -- nullable for historical import
    settlement_date TEXT,
    settlement_status TEXT DEFAULT 'OPEN',   -- OPEN | IN_PROGRESS | DRAFT | SUBMITTED | APPROVED | CLOSED
    -- Planned values (from contract)
    planned_value_usd   REAL,               -- NUMERIC(15,2)
    planned_weight_ton  REAL,
    planned_gm_pct      REAL,
    planned_gm_value    REAL,               -- NUMERIC(15,2)
    -- Actual values (from execution)
    actual_revenue_usd  REAL,               -- NUMERIC(15,2)
    actual_weight_ton   REAL,
    actual_material_cost REAL,              -- NUMERIC(15,2)
    actual_labor_cost   REAL,               -- NUMERIC(15,2)
    actual_overhead_cost REAL,              -- NUMERIC(15,2)
    actual_subcontract_cost REAL,           -- NUMERIC(15,2)
    actual_total_cost   REAL,               -- NUMERIC(15,2)
    actual_gm_pct       REAL,
    actual_gm_value     REAL,               -- NUMERIC(15,2)
    -- Variance analysis
    revenue_variance_usd REAL,              -- NUMERIC(15,2) actual - planned
    cost_variance_usd   REAL,               -- NUMERIC(15,2)
    gm_variance_pct     REAL,
    weight_variance_ton  REAL,
    -- Payment status
    total_invoiced      REAL,               -- NUMERIC(15,2)
    total_received      REAL,               -- NUMERIC(15,2)
    outstanding_amount  REAL,               -- NUMERIC(15,2)
    retention_held      REAL,               -- NUMERIC(15,2) retention money
    retention_released  REAL,               -- NUMERIC(15,2)
    -- Approvals
    prepared_by     TEXT,
    reviewed_by     TEXT,
    approved_by     TEXT,
    approved_at     TEXT,
    lessons_learned TEXT,
    nas_file_path   TEXT,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_ss_opp ON sale_settlements(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_ss_status ON sale_settlements(settlement_status);
CREATE INDEX IF NOT EXISTS idx_ss_date ON sale_settlements(settlement_date);
CREATE UNIQUE INDEX IF NOT EXISTS idx_ss_opp_unique ON sale_settlements(opportunity_id);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 26: sale_report_configs                        [M8 Auto-Report]
-- Scheduled report definitions, templates, and distribution lists
-- Sources: 02.BaoCao_Reports/ (78 files) structure analysis,
--          BAO CAO THANG format (7 sheets, 83 cols)
-- Feeds: automated weekly/monthly report generation, email distribution
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_report_configs (
    id              TEXT PRIMARY KEY,
    report_name     TEXT NOT NULL,
    report_type     TEXT NOT NULL,           -- WEEKLY_PIPELINE | MONTHLY_KTKH | QUARTERLY_REVIEW | KHKD_PROGRESS | COMMISSION_SUMMARY | CAPITAL_RECOVERY | CUSTOM
    description     TEXT,
    schedule_cron   TEXT,                    -- cron expression: "0 8 * * MON" = every Monday 8am
    schedule_type   TEXT DEFAULT 'MANUAL',   -- MANUAL | DAILY | WEEKLY | MONTHLY | QUARTERLY
    template_format TEXT DEFAULT 'XLSX',     -- XLSX | PDF | HTML | EMAIL
    template_config TEXT,                    -- JSON: which tables, filters, columns, charts
    filters_json    TEXT,                    -- JSON: date range, product group, assigned_to, etc.
    recipients      TEXT,                    -- JSON array of email addresses
    cc_recipients   TEXT,                    -- JSON array
    delivery_method TEXT DEFAULT 'EMAIL',    -- EMAIL | NAS | BOTH
    nas_output_path TEXT,                    -- where to save on NAS
    last_run_at     TEXT,
    last_run_status TEXT,                    -- SUCCESS | FAILED | PARTIAL
    last_run_error  TEXT,
    run_count       INTEGER DEFAULT 0,
    is_active       INTEGER DEFAULT 1,
    created_by      TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_src_type ON sale_report_configs(report_type);
CREATE INDEX IF NOT EXISTS idx_src_schedule ON sale_report_configs(schedule_type);
CREATE INDEX IF NOT EXISTS idx_src_active ON sale_report_configs(is_active);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 27: sale_digital_content                       [M10 Digital Marketing]
-- Corporate brochures, presentations, campaigns, and marketing assets
-- Sources: MKT/ (13 files), 10.Marketing/ on NAS,
--          company profiles, corporate presentations
-- Feeds: sales enablement, marketing campaign tracking, content library
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_digital_content (
    id              TEXT PRIMARY KEY,
    content_type    TEXT NOT NULL,           -- BROCHURE | PRESENTATION | COMPANY_PROFILE | CASE_STUDY | VIDEO | INFOGRAPHIC | SOCIAL_POST | CAMPAIGN
    title           TEXT NOT NULL,
    title_vn        TEXT,
    description     TEXT,
    language        TEXT DEFAULT 'en',       -- en | vn | both
    target_audience TEXT,                    -- PROSPECT | EXISTING_CUSTOMER | PARTNER | PUBLIC
    product_category_id TEXT REFERENCES sale_product_categories(id),
    file_format     TEXT,                    -- PDF | PPTX | DOCX | MP4 | PNG | HTML
    file_size_mb    REAL,
    nas_file_path   TEXT,                    -- primary file location on NAS
    gdrive_file_id  TEXT,                    -- Google Drive file ID if synced
    thumbnail_path  TEXT,
    version         INTEGER DEFAULT 1,
    is_latest       INTEGER DEFAULT 1,
    -- Campaign tracking (for CAMPAIGN type)
    campaign_start  TEXT,
    campaign_end    TEXT,
    campaign_channel TEXT,                   -- EMAIL | LINKEDIN | WEBSITE | EXHIBITION | DIRECT_MAIL
    campaign_budget REAL,                    -- NUMERIC(15,2)
    campaign_leads  INTEGER DEFAULT 0,       -- leads generated
    -- Usage tracking
    view_count      INTEGER DEFAULT 0,
    download_count  INTEGER DEFAULT 0,
    share_count     INTEGER DEFAULT 0,
    last_used_at    TEXT,
    -- Metadata
    tags            TEXT,                    -- JSON array
    created_by      TEXT,
    approved_by     TEXT,
    is_active       INTEGER DEFAULT 1,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sdc_type ON sale_digital_content(content_type);
CREATE INDEX IF NOT EXISTS idx_sdc_product ON sale_digital_content(product_category_id);
CREATE INDEX IF NOT EXISTS idx_sdc_audience ON sale_digital_content(target_audience);
CREATE INDEX IF NOT EXISTS idx_sdc_active ON sale_digital_content(is_active);
CREATE INDEX IF NOT EXISTS idx_sdc_channel ON sale_digital_content(campaign_channel);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 28: sale_inter_dept_tasks                      [M11 Inter-dept Task Engine]
-- Cross-department task routing with SLA tracking and escalation
-- Departments: SALE, KTKH, KT, SX, TM, QLDA, TCKT, QAQC, MKT
-- Sources: internal workflows, email-triggered tasks, manual assignment
-- Feeds: cross-dept collaboration, SLA compliance, workload distribution
-- Note: Extends sale_tasks (Table 6) for structured inter-dept workflows
--       sale_tasks handles individual tasks; this handles formal dept-to-dept
--       workflows with approval chains and multi-step processes
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_inter_dept_tasks (
    id              TEXT PRIMARY KEY,
    task_id         TEXT REFERENCES sale_tasks(id), -- optional link to base task
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    workflow_type   TEXT NOT NULL,           -- RFQ_REVIEW | COST_ESTIMATION | TECHNICAL_REVIEW | CAPACITY_CHECK | QC_INSPECTION | DRAWING_REVIEW | CONTRACT_REVIEW
    workflow_ref    TEXT,                    -- e.g. "WF-2026-001"
    title           TEXT NOT NULL,
    description     TEXT,
    -- Routing
    from_dept       TEXT NOT NULL,           -- originating department
    from_user       TEXT,
    to_dept         TEXT NOT NULL,           -- target department
    to_user         TEXT,                    -- specific assignee
    cc_depts        TEXT,                    -- JSON array of departments to notify
    -- Workflow state
    step_number     INTEGER DEFAULT 1,       -- current step in multi-step workflow
    total_steps     INTEGER DEFAULT 1,
    status          TEXT DEFAULT 'PENDING',   -- PENDING | IN_PROGRESS | WAITING_INPUT | COMPLETED | REJECTED | CANCELLED | ESCALATED
    priority        TEXT DEFAULT 'NORMAL',    -- LOW | NORMAL | HIGH | URGENT
    -- SLA
    sla_hours       INTEGER,
    due_date        TEXT,
    started_at      TEXT,
    completed_at    TEXT,
    sla_met         INTEGER,                 -- 1 = met, 0 = breached, NULL = not yet due
    -- Deliverables
    input_data      TEXT,                    -- JSON: what was provided
    output_data     TEXT,                    -- JSON: what was delivered
    deliverable_path TEXT,                   -- NAS path to deliverable
    -- Escalation
    is_escalated    INTEGER DEFAULT 0,
    escalated_to    TEXT,
    escalated_at    TEXT,
    escalation_reason TEXT,
    -- Approval chain
    requires_approval INTEGER DEFAULT 0,
    approved_by     TEXT,
    approved_at     TEXT,
    rejection_reason TEXT,
    -- Tracking
    comments        TEXT,                    -- JSON array of threaded comments
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sidt_workflow ON sale_inter_dept_tasks(workflow_type);
CREATE INDEX IF NOT EXISTS idx_sidt_from ON sale_inter_dept_tasks(from_dept);
CREATE INDEX IF NOT EXISTS idx_sidt_to ON sale_inter_dept_tasks(to_dept);
CREATE INDEX IF NOT EXISTS idx_sidt_status ON sale_inter_dept_tasks(status);
CREATE INDEX IF NOT EXISTS idx_sidt_opp ON sale_inter_dept_tasks(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_sidt_due ON sale_inter_dept_tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_sidt_priority ON sale_inter_dept_tasks(priority);
CREATE INDEX IF NOT EXISTS idx_sidt_sla ON sale_inter_dept_tasks(sla_met);
CREATE INDEX IF NOT EXISTS idx_sidt_task ON sale_inter_dept_tasks(task_id);


-- ═══════════════════════════════════════════════════════════════
-- END OF SCHEMA EXTENSION
-- Total: 12 new tables (17-28), completing 28-table architecture
-- ═══════════════════════════════════════════════════════════════
