-- ═══════════════════════════════════════════════════════════════════════════════
-- IBS HI SALE PLATFORM v4 - CONSOLIDATED SCHEMA (32 Tables + 2 Views)
-- Merges: schema_base.sql (16) + schema_new.sql (12) + 4 inline tables
-- Generated: 2026-04-29
-- Run: sqlite3 sale.db < schema_all.sql (before master_import.sql)
-- Convention: TEXT PK (UUID), TEXT dates, REAL money, IF NOT EXISTS guards
-- ═══════════════════════════════════════════════════════════════════════════════


-- ═══════════════════════════════════════════════════════════════
-- SECTION A: BASE TABLES (1-16) — from schema_base.sql
-- ═══════════════════════════════════════════════════════════════


-- ── TABLE 1: sale_customers ──
-- Source: Workflow 2026 (988 records) + khach_hang (63 records)
CREATE TABLE IF NOT EXISTS sale_customers (
    id              TEXT PRIMARY KEY,
    code            TEXT UNIQUE,
    name            TEXT NOT NULL,
    country         TEXT,
    region          TEXT,
    address         TEXT,
    website         TEXT,
    business_description TEXT,
    status          TEXT DEFAULT 'ACTIVE',
    legacy_id       INTEGER,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sc_code ON sale_customers(code);
CREATE INDEX IF NOT EXISTS idx_sc_region ON sale_customers(region);


-- ── TABLE 2: sale_customer_contacts ──
-- Individual contacts within customer organizations
CREATE TABLE IF NOT EXISTS sale_customer_contacts (
    id              TEXT PRIMARY KEY,
    customer_id     TEXT NOT NULL REFERENCES sale_customers(id),
    name            TEXT NOT NULL,
    email           TEXT,
    phone           TEXT,
    position        TEXT,
    linkedin        TEXT,
    is_primary      INTEGER DEFAULT 0,
    created_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_scc_customer ON sale_customer_contacts(customer_id);


-- ── TABLE 3: sale_product_categories ──
-- KHKD product groups: HRSG, DIVERTER, SHIP, PV, HANDLING, DUCT, OTHER
CREATE TABLE IF NOT EXISTS sale_product_categories (
    id              TEXT PRIMARY KEY,
    code            TEXT UNIQUE NOT NULL,
    name_en         TEXT NOT NULL,
    name_vn         TEXT,
    target_tons     REAL,
    target_unit_price REAL,
    target_revenue  REAL,
    target_gm_pct   REAL,
    target_gm_value REAL,
    created_at      TEXT DEFAULT (datetime('now'))
);


-- ── TABLE 4: sale_opportunities ──
-- Central pipeline table: links emails, tasks, and deals
CREATE TABLE IF NOT EXISTS sale_opportunities (
    id                      TEXT PRIMARY KEY,
    pl_hd                   TEXT,
    product_group           TEXT NOT NULL,
    customer_id             TEXT REFERENCES sale_customers(id),
    customer_name           TEXT,
    project_name            TEXT NOT NULL,
    scope_en                TEXT,
    scope_vn                TEXT,
    stage                   TEXT NOT NULL DEFAULT 'PROSPECT',
    win_probability         INTEGER DEFAULT 50,
    weight_ton              REAL,
    contract_value_vnd      REAL,
    contract_value_usd      REAL,
    unit_price_usd          REAL,
    gm_percent              REAL,
    gm_value_usd            REAL,
    material_cost_usd       REAL,
    labor_cost_usd          REAL,
    subcontractor_cost_usd  REAL,
    profit_usd              REAL,
    estimated_signing       TEXT,
    start_date              TEXT,
    duration_months         INTEGER,
    end_date                TEXT,
    quotation_date          TEXT,
    qty_2025                REAL,
    value_2025              REAL,
    gp_2025                 REAL,
    qty_2026                REAL,
    value_2026              REAL,
    gp_2026                 REAL,
    milestones              TEXT,
    assigned_to             TEXT,
    nas_quotation_path      TEXT,
    nas_contract_path       TEXT,
    notes                   TEXT,
    last_activity_date      TEXT DEFAULT (datetime('now')),
    stale_flag              INTEGER DEFAULT 0,
    loss_reason             TEXT,
    competitor              TEXT,
    created_at              TEXT DEFAULT (datetime('now')),
    updated_at              TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_so_stage ON sale_opportunities(stage);
CREATE INDEX IF NOT EXISTS idx_so_customer ON sale_opportunities(customer_id);
CREATE INDEX IF NOT EXISTS idx_so_assigned ON sale_opportunities(assigned_to);
CREATE INDEX IF NOT EXISTS idx_so_product ON sale_opportunities(product_group);
CREATE INDEX IF NOT EXISTS idx_so_stale ON sale_opportunities(stale_flag);


-- ── TABLE 5: sale_emails ──
-- Synced from Gmail via API — structured for programmatic sync
CREATE TABLE IF NOT EXISTS sale_emails (
    id              TEXT PRIMARY KEY,
    gmail_id        TEXT UNIQUE,
    thread_id       TEXT,
    mailbox_id      TEXT REFERENCES sale_monitored_mailboxes(id),
    source_dept     TEXT,
    email_type      TEXT,
    confidence      REAL,
    from_address    TEXT,
    from_name       TEXT,
    to_addresses    TEXT,
    cc_addresses    TEXT,
    subject         TEXT,
    snippet         TEXT,
    body_text       TEXT,
    has_attachments INTEGER DEFAULT 0,
    attachment_names TEXT,
    received_at     TEXT,
    processed_at    TEXT,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    customer_id     TEXT REFERENCES sale_customers(id),
    is_read         INTEGER DEFAULT 0,
    is_actioned     INTEGER DEFAULT 0,
    actioned_by     TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_se_type ON sale_emails(email_type);
CREATE INDEX IF NOT EXISTS idx_se_thread ON sale_emails(thread_id);
CREATE INDEX IF NOT EXISTS idx_se_opp ON sale_emails(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_se_received ON sale_emails(received_at);
CREATE INDEX IF NOT EXISTS idx_se_gmail ON sale_emails(gmail_id);


-- ── TABLE 6: sale_tasks ──
-- Unified task engine for all work types
CREATE TABLE IF NOT EXISTS sale_tasks (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    email_id        TEXT REFERENCES sale_emails(id),
    parent_task_id  TEXT REFERENCES sale_tasks(id),
    task_type       TEXT NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT,
    from_dept       TEXT NOT NULL,
    to_dept         TEXT NOT NULL,
    assigned_to     TEXT,
    assigned_by     TEXT,
    sla_hours       INTEGER,
    due_date        TEXT,
    status          TEXT NOT NULL DEFAULT 'PENDING',
    started_at      TEXT,
    completed_at    TEXT,
    result          TEXT,
    is_escalated    INTEGER DEFAULT 0,
    escalated_to    TEXT,
    escalated_at    TEXT,
    escalation_count INTEGER DEFAULT 0,
    nas_file_path   TEXT,
    attachments     TEXT,
    priority        TEXT DEFAULT 'NORMAL',
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_st_status ON sale_tasks(status);
CREATE INDEX IF NOT EXISTS idx_st_assigned ON sale_tasks(assigned_to);
CREATE INDEX IF NOT EXISTS idx_st_opp ON sale_tasks(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_st_due ON sale_tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_st_type ON sale_tasks(task_type);
CREATE INDEX IF NOT EXISTS idx_st_dept ON sale_tasks(to_dept);


-- ── TABLE 7: sale_follow_up_schedules ──
-- Automated reminder engine for quotations and negotiations
CREATE TABLE IF NOT EXISTS sale_follow_up_schedules (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT NOT NULL REFERENCES sale_opportunities(id),
    schedule_type   TEXT NOT NULL,
    reminder_days   TEXT,
    next_follow_up  TEXT,
    last_follow_up  TEXT,
    follow_up_count INTEGER DEFAULT 0,
    is_active       INTEGER DEFAULT 1,
    customer_id     TEXT REFERENCES sale_customers(id),
    contact_id      TEXT REFERENCES sale_customer_contacts(id),
    assigned_to     TEXT,
    status          TEXT DEFAULT 'PENDING',     -- PENDING | DONE | CANCELLED | RESCHEDULED
    outcome         TEXT,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sfu_next ON sale_follow_up_schedules(next_follow_up);
CREATE INDEX IF NOT EXISTS idx_sfu_opp ON sale_follow_up_schedules(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_sfu_status ON sale_follow_up_schedules(status);
CREATE INDEX IF NOT EXISTS idx_sfu_assigned ON sale_follow_up_schedules(assigned_to);
CREATE INDEX IF NOT EXISTS idx_sfu_customer ON sale_follow_up_schedules(customer_id);


-- ── TABLE 8: sale_email_templates ──
-- Pre-built email templates for standard communications
CREATE TABLE IF NOT EXISTS sale_email_templates (
    id              TEXT PRIMARY KEY,
    template_type   TEXT NOT NULL UNIQUE,
    subject         TEXT,
    body            TEXT,
    language        TEXT DEFAULT 'en',
    variables       TEXT,
    is_active       INTEGER DEFAULT 1,
    created_at      TEXT DEFAULT (datetime('now'))
);


-- ── TABLE 9: sale_email_activity_log ──
-- Audit trail for all email actions
CREATE TABLE IF NOT EXISTS sale_email_activity_log (
    id              TEXT PRIMARY KEY,
    email_id        TEXT REFERENCES sale_emails(id),
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    task_id         TEXT REFERENCES sale_tasks(id),
    action_type     TEXT NOT NULL,
    action_by       TEXT,
    details         TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_seal_email ON sale_email_activity_log(email_id);
CREATE INDEX IF NOT EXISTS idx_seal_opp ON sale_email_activity_log(opportunity_id);


-- ── TABLE 10: sale_khkd_targets ──
-- Business plan tracking FY2026-2027: $19.1M revenue, 7000 tons, 21% GM, 25 POs
CREATE TABLE IF NOT EXISTS sale_khkd_targets (
    id              TEXT PRIMARY KEY,
    fiscal_year     TEXT NOT NULL,
    total_revenue_target    REAL,
    total_tons_target       REAL,
    total_gm_pct_target     REAL,
    total_gm_value_target   REAL,
    total_po_target         INTEGER,
    backlog_tons            REAL,
    workload_to_find        REAL,
    min_monthly_capacity    REAL,
    created_at      TEXT DEFAULT (datetime('now'))
);


-- ── TABLE 11: sale_nas_file_links ──
-- References to NAS file storage (files stay on NAS, paths indexed here)
CREATE TABLE IF NOT EXISTS sale_nas_file_links (
    id              TEXT PRIMARY KEY,
    entity_type     TEXT NOT NULL,
    entity_id       TEXT NOT NULL,
    nas_path        TEXT NOT NULL,
    file_name       TEXT,
    file_type       TEXT,
    description     TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_snfl_entity ON sale_nas_file_links(entity_type, entity_id);


-- ── TABLE 12: sale_monitored_mailboxes ──
-- Gmail mailboxes synced with the platform
CREATE TABLE IF NOT EXISTS sale_monitored_mailboxes (
    id              TEXT PRIMARY KEY,
    email_address   TEXT UNIQUE NOT NULL,
    display_name    TEXT,
    department      TEXT NOT NULL,
    owner_name      TEXT,
    oauth_token     TEXT,
    token_valid     INTEGER DEFAULT 0,
    sync_enabled    INTEGER DEFAULT 1,
    sync_from_date  TEXT,
    last_sync_at    TEXT,
    last_sync_count INTEGER DEFAULT 0,
    is_active       INTEGER DEFAULT 1,
    deactivated_at  TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_smm_email ON sale_monitored_mailboxes(email_address);


-- ── TABLE 13: sale_user_roles ──
-- Platform access control and department assignments
CREATE TABLE IF NOT EXISTS sale_user_roles (
    id              TEXT PRIMARY KEY,
    user_name       TEXT NOT NULL,
    email           TEXT UNIQUE,
    department      TEXT NOT NULL,
    role            TEXT NOT NULL DEFAULT 'MEMBER',
    permissions     TEXT,
    is_active       INTEGER DEFAULT 1,
    joined_at       TEXT DEFAULT (datetime('now')),
    deactivated_at  TEXT,
    l1_user_id      TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sur_dept ON sale_user_roles(department);
CREATE INDEX IF NOT EXISTS idx_sur_active ON sale_user_roles(is_active);


-- ── TABLE 14: sale_pm_sync_log ──
-- 2-way sync audit: Sale (L2) <-> PM/Workflow (L1)
CREATE TABLE IF NOT EXISTS sale_pm_sync_log (
    id              TEXT PRIMARY KEY,
    direction       TEXT NOT NULL,
    source_entity   TEXT NOT NULL,
    source_id       TEXT NOT NULL,
    target_entity   TEXT NOT NULL,
    target_id       TEXT,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    project_code    TEXT,
    sync_type       TEXT NOT NULL,
    action          TEXT NOT NULL,
    payload         TEXT,
    status          TEXT NOT NULL DEFAULT 'PENDING',
    error_message   TEXT,
    triggered_by    TEXT,
    reviewed_by     TEXT,
    reviewed_at     TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_spsl_direction ON sale_pm_sync_log(direction);
CREATE INDEX IF NOT EXISTS idx_spsl_project ON sale_pm_sync_log(project_code);
CREATE INDEX IF NOT EXISTS idx_spsl_opp ON sale_pm_sync_log(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_spsl_status ON sale_pm_sync_log(status);


-- ── TABLE 15: sale_import_log ──
-- Mandatory audit log for all data imports
CREATE TABLE IF NOT EXISTS sale_import_log (
    id              TEXT PRIMARY KEY,
    import_type     TEXT NOT NULL,
    source_file     TEXT,
    records_total   INTEGER,
    records_imported INTEGER,
    records_failed  INTEGER,
    errors          TEXT,
    imported_by     TEXT,
    started_at      TEXT DEFAULT (datetime('now')),
    completed_at    TEXT
);


-- ── TABLE 16: sale_audit_log ──
-- Tracks changes to financial fields, status transitions, role changes
CREATE TABLE IF NOT EXISTS sale_audit_log (
    id              TEXT PRIMARY KEY,
    entity_type     TEXT NOT NULL,
    entity_id       TEXT NOT NULL,
    action          TEXT NOT NULL,
    field_name      TEXT,
    old_value       TEXT,
    new_value       TEXT,
    changed_by      TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON sale_audit_log(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_created ON sale_audit_log(created_at);


-- ── TABLE 16b: sale_notifications ──
-- In-app notification feed: SLA / stale-deal / followup / quotation alerts
-- Written by workers (sla_worker, stale_worker, followup_worker) and read by API.
CREATE TABLE IF NOT EXISTS sale_notifications (
    id              TEXT PRIMARY KEY,
    user_id         TEXT,                        -- assignee email or user_name; NULL = broadcast
    type            TEXT NOT NULL,               -- SLA_OVERDUE, STALE_DEAL, FOLLOWUP_DUE, QUOTATION_EXPIRING
    title           TEXT NOT NULL,
    message         TEXT,
    entity_type     TEXT,                        -- task | opportunity | follow_up | quotation
    entity_id       TEXT,
    is_read         INTEGER DEFAULT 0,
    severity        TEXT DEFAULT 'INFO',         -- INFO | WARN | CRIT
    created_at      TEXT DEFAULT (datetime('now')),
    read_at         TEXT
);
CREATE INDEX IF NOT EXISTS idx_notif_user ON sale_notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notif_unread ON sale_notifications(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_notif_type ON sale_notifications(type);
CREATE INDEX IF NOT EXISTS idx_notif_created ON sale_notifications(created_at);


-- ═══════════════════════════════════════════════════════════════
-- SECTION B: EXTENDED TABLES (17-28) — from schema_new.sql
-- ═══════════════════════════════════════════════════════════════


-- ── TABLE 17: sale_market_signals ──  [M1 Market Intelligence]
-- Competitor alerts, market events, industry news, tender notices
CREATE TABLE IF NOT EXISTS sale_market_signals (
    id              TEXT PRIMARY KEY,
    signal_type     TEXT NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT,
    source_url      TEXT,
    source_name     TEXT,
    region          TEXT,
    industry        TEXT,
    competitor_name TEXT,
    relevance_score REAL,
    impact_level    TEXT DEFAULT 'MEDIUM',
    related_product_group TEXT,
    related_customer_id   TEXT REFERENCES sale_customers(id),
    expires_at      TEXT,
    is_actionable   INTEGER DEFAULT 1,
    actioned_by     TEXT,
    actioned_at     TEXT,
    tags            TEXT,
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


-- ── TABLE 18: sale_product_opportunities ──  [M2 Product-Capability]
-- Product-customer fit matrix
CREATE TABLE IF NOT EXISTS sale_product_opportunities (
    id              TEXT PRIMARY KEY,
    product_category_id TEXT REFERENCES sale_product_categories(id),
    customer_id     TEXT REFERENCES sale_customers(id),
    fit_score       REAL,
    capability_status TEXT DEFAULT 'FULL',
    gap_description TEXT,
    past_project_count INTEGER DEFAULT 0,
    last_quoted_at  TEXT,
    last_won_at     TEXT,
    avg_unit_price  REAL,
    avg_gm_pct      REAL,
    total_revenue   REAL,
    total_weight_ton REAL,
    competitor_threat TEXT,
    notes           TEXT,
    is_strategic    INTEGER DEFAULT 0,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_spo_product ON sale_product_opportunities(product_category_id);
CREATE INDEX IF NOT EXISTS idx_spo_customer ON sale_product_opportunities(customer_id);
CREATE INDEX IF NOT EXISTS idx_spo_fit ON sale_product_opportunities(fit_score);
CREATE INDEX IF NOT EXISTS idx_spo_strategic ON sale_product_opportunities(is_strategic);


-- ── TABLE 19: sale_quotation_revisions ──  [M4.5 Quotation Revision]
-- Revision history per opportunity: price changes, scope edits
CREATE TABLE IF NOT EXISTS sale_quotation_revisions (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    revision_number INTEGER NOT NULL DEFAULT 1,
    revision_date   TEXT NOT NULL,
    revision_reason TEXT,
    quotation_ref   TEXT,
    weight_ton      REAL,
    unit_price_usd  REAL,
    total_value_usd REAL,
    total_value_vnd REAL,
    material_cost   REAL,
    labor_cost      REAL,
    overhead_cost   REAL,
    gm_percent      REAL,
    gm_value        REAL,
    scope_summary   TEXT,
    price_delta_pct REAL,
    nas_file_path   TEXT,
    sent_to         TEXT,
    sent_at         TEXT,
    customer_response TEXT,
    response_date   TEXT,
    valid_until     TEXT,
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


-- ── TABLE 20: sale_quote_templates ──  [M4.7 Auto-Quote Engine]
-- Reusable cost breakdown templates and standard pricing
CREATE TABLE IF NOT EXISTS sale_quote_templates (
    id              TEXT PRIMARY KEY,
    template_name   TEXT NOT NULL,
    product_category_id TEXT REFERENCES sale_product_categories(id),
    product_type    TEXT,
    weight_range_min REAL,
    weight_range_max REAL,
    base_unit_price REAL,
    material_pct    REAL,
    labor_pct       REAL,
    overhead_pct    REAL,
    subcontract_pct REAL,
    target_gm_pct   REAL,
    complexity_factor REAL DEFAULT 1.0,
    lead_time_weeks INTEGER,
    cost_breakdown_json TEXT,
    assumptions     TEXT,
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


-- ── TABLE 21: sale_customer_interactions ──  [M5 CRM 360]
-- Unified interaction log: meetings, calls, site visits, exhibitions
CREATE TABLE IF NOT EXISTS sale_customer_interactions (
    id              TEXT PRIMARY KEY,
    customer_id     TEXT NOT NULL REFERENCES sale_customers(id),
    contact_id      TEXT REFERENCES sale_customer_contacts(id),
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    interaction_type TEXT NOT NULL,
    interaction_date TEXT NOT NULL,
    duration_minutes INTEGER,
    location        TEXT,
    attendees_ibs   TEXT,
    attendees_customer TEXT,
    subject         TEXT NOT NULL,
    summary         TEXT,
    outcome         TEXT,
    next_action     TEXT,
    next_action_due TEXT,
    sentiment_score REAL,
    nas_file_path   TEXT,
    attachments     TEXT,
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


-- ── TABLE 22: sale_commissions ──  [M6 Commission]
-- GP-based commission calculation with tiers and payout tracking
CREATE TABLE IF NOT EXISTS sale_commissions (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    salesperson     TEXT NOT NULL,
    salesperson_role TEXT,
    fiscal_year     TEXT NOT NULL,
    fiscal_quarter  TEXT,
    contract_value_usd REAL,
    gm_value_usd   REAL,
    gm_percent      REAL,
    commission_tier TEXT,
    commission_rate REAL,
    commission_amount_usd REAL,
    commission_amount_vnd REAL,
    bonus_amount    REAL,
    adjustment      REAL,
    adjustment_reason TEXT,
    status          TEXT DEFAULT 'CALCULATED',
    calculation_date TEXT,
    approved_by     TEXT,
    approved_at     TEXT,
    paid_at         TEXT,
    payment_ref     TEXT,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_scom_opp ON sale_commissions(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_scom_person ON sale_commissions(salesperson);
CREATE INDEX IF NOT EXISTS idx_scom_fy ON sale_commissions(fiscal_year);
CREATE INDEX IF NOT EXISTS idx_scom_status ON sale_commissions(status);
CREATE INDEX IF NOT EXISTS idx_scom_tier ON sale_commissions(commission_tier);


-- ── TABLE 23: sale_contract_milestones ──  [M7.1 Capital Recovery]
-- Delivery milestones, payment terms, and invoice scheduling
CREATE TABLE IF NOT EXISTS sale_contract_milestones (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    milestone_number INTEGER NOT NULL,
    milestone_type  TEXT NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT,
    planned_date    TEXT,
    actual_date     TEXT,
    weight_ton      REAL,
    invoice_amount_usd REAL,
    invoice_amount_vnd REAL,
    payment_term_days INTEGER,
    invoice_number  TEXT,
    invoice_date    TEXT,
    invoice_status  TEXT DEFAULT 'NOT_INVOICED',
    payment_received_date TEXT,
    payment_amount  REAL,
    overdue_days    INTEGER DEFAULT 0,
    penalty_amount  REAL,
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


-- ── TABLE 24: sale_change_orders ──  [M7.2 Change Orders]
-- Scope changes, price adjustments, contract amendments
CREATE TABLE IF NOT EXISTS sale_change_orders (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    change_order_number INTEGER NOT NULL,
    co_ref          TEXT,
    change_type     TEXT NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT,
    requested_by    TEXT,
    request_date    TEXT,
    original_value_usd REAL,
    revised_value_usd  REAL,
    delta_value_usd REAL,
    original_weight_ton REAL,
    revised_weight_ton  REAL,
    delta_weight_ton REAL,
    impact_on_gm_pct REAL,
    schedule_impact_days INTEGER,
    status          TEXT DEFAULT 'DRAFT',
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


-- ── TABLE 25: sale_settlements ──  [M7.3 Settlement]
-- Final project reconciliation: planned vs actual cost/revenue/margin
CREATE TABLE IF NOT EXISTS sale_settlements (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    settlement_date TEXT,
    settlement_status TEXT DEFAULT 'OPEN',
    planned_value_usd   REAL,
    planned_weight_ton  REAL,
    planned_gm_pct      REAL,
    planned_gm_value    REAL,
    actual_revenue_usd  REAL,
    actual_weight_ton   REAL,
    actual_material_cost REAL,
    actual_labor_cost   REAL,
    actual_overhead_cost REAL,
    actual_subcontract_cost REAL,
    actual_total_cost   REAL,
    actual_gm_pct       REAL,
    actual_gm_value     REAL,
    revenue_variance_usd REAL,
    cost_variance_usd   REAL,
    gm_variance_pct     REAL,
    weight_variance_ton  REAL,
    total_invoiced      REAL,
    total_received      REAL,
    outstanding_amount  REAL,
    retention_held      REAL,
    retention_released  REAL,
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


-- ── TABLE 26: sale_report_configs ──  [M8 Auto-Report]
-- Scheduled report definitions, templates, distribution lists
CREATE TABLE IF NOT EXISTS sale_report_configs (
    id              TEXT PRIMARY KEY,
    report_name     TEXT NOT NULL,
    report_type     TEXT NOT NULL,
    description     TEXT,
    schedule_cron   TEXT,
    schedule_type   TEXT DEFAULT 'MANUAL',
    template_format TEXT DEFAULT 'XLSX',
    template_config TEXT,
    filters_json    TEXT,
    recipients      TEXT,
    cc_recipients   TEXT,
    delivery_method TEXT DEFAULT 'EMAIL',
    nas_output_path TEXT,
    last_run_at     TEXT,
    last_run_status TEXT,
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


-- ── TABLE 27: sale_digital_content ──  [M10 Digital Marketing]
-- Corporate brochures, presentations, campaigns, marketing assets
CREATE TABLE IF NOT EXISTS sale_digital_content (
    id              TEXT PRIMARY KEY,
    content_type    TEXT NOT NULL,
    title           TEXT NOT NULL,
    title_vn        TEXT,
    description     TEXT,
    language        TEXT DEFAULT 'en',
    target_audience TEXT,
    product_category_id TEXT REFERENCES sale_product_categories(id),
    file_format     TEXT,
    file_size_mb    REAL,
    nas_file_path   TEXT,
    gdrive_file_id  TEXT,
    thumbnail_path  TEXT,
    version         INTEGER DEFAULT 1,
    is_latest       INTEGER DEFAULT 1,
    campaign_start  TEXT,
    campaign_end    TEXT,
    campaign_channel TEXT,
    campaign_budget REAL,
    campaign_leads  INTEGER DEFAULT 0,
    view_count      INTEGER DEFAULT 0,
    download_count  INTEGER DEFAULT 0,
    share_count     INTEGER DEFAULT 0,
    last_used_at    TEXT,
    tags            TEXT,
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


-- ── TABLE 28: sale_inter_dept_tasks ──  [M11 Inter-dept Task Engine]
-- Cross-department task routing with SLA tracking and escalation
CREATE TABLE IF NOT EXISTS sale_inter_dept_tasks (
    id              TEXT PRIMARY KEY,
    task_id         TEXT REFERENCES sale_tasks(id),
    opportunity_id  TEXT REFERENCES sale_opportunities(id),
    workflow_type   TEXT NOT NULL,
    workflow_ref    TEXT,
    title           TEXT NOT NULL,
    description     TEXT,
    from_dept       TEXT NOT NULL,
    from_user       TEXT,
    to_dept         TEXT NOT NULL,
    to_user         TEXT,
    cc_depts        TEXT,
    step_number     INTEGER DEFAULT 1,
    total_steps     INTEGER DEFAULT 1,
    status          TEXT DEFAULT 'PENDING',
    priority        TEXT DEFAULT 'NORMAL',
    sla_hours       INTEGER,
    due_date        TEXT,
    started_at      TEXT,
    completed_at    TEXT,
    sla_met         INTEGER,
    input_data      TEXT,
    output_data     TEXT,
    deliverable_path TEXT,
    is_escalated    INTEGER DEFAULT 0,
    escalated_to    TEXT,
    escalated_at    TEXT,
    escalation_reason TEXT,
    requires_approval INTEGER DEFAULT 0,
    approved_by     TEXT,
    approved_at     TEXT,
    rejection_reason TEXT,
    comments        TEXT,
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
-- SECTION C: INLINE TABLES (29-32) — previously created within import files
-- ═══════════════════════════════════════════════════════════════


-- ── TABLE 29: sale_quotation_history ──  (from 17_quotation_enrichment.sql)
-- 1,001 historical quotation records from Quotation Record xlsx (2019-2025)
CREATE TABLE IF NOT EXISTS sale_quotation_history (
    id              TEXT PRIMARY KEY,
    quotation_no    INTEGER NOT NULL,
    customer_code   TEXT,
    customer_name   TEXT,
    country         TEXT,
    market          TEXT,
    product_type    TEXT,
    project_name    TEXT,
    scope_of_work   TEXT,
    launch_date     TEXT,
    duration_months REAL,
    weight_ton      REAL,
    price_usd_mt    REAL,
    value_vnd       REAL,
    value_usd       REAL,
    gross_profit_usd REAL,
    gp_percent      REAL,
    date_offer      TEXT,
    incharge        TEXT,
    status          TEXT,
    remark          TEXT,
    owner           TEXT,
    customer_id     TEXT REFERENCES sale_customers(id),
    source          TEXT DEFAULT 'Quotation Record xlsx',
    created_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_qh_no ON sale_quotation_history(quotation_no);
CREATE INDEX IF NOT EXISTS idx_qh_cust ON sale_quotation_history(customer_code);
CREATE INDEX IF NOT EXISTS idx_qh_status ON sale_quotation_history(status);


-- ── TABLE 30: sale_active_contracts ──  (from 21_email_active_contracts.sql)
-- Active/ongoing contracts as of Apr 2026 (from ibshi@ email scan)
CREATE TABLE IF NOT EXISTS sale_active_contracts (
    id              TEXT PRIMARY KEY,
    po_number       TEXT NOT NULL,
    customer_name   TEXT NOT NULL,
    project_name    TEXT,
    product_type    TEXT,
    contract_status TEXT DEFAULT 'ACTIVE',
    start_date      TEXT,
    latest_activity TEXT,
    value_notes     TEXT,
    project_manager TEXT,
    customer_id     TEXT REFERENCES sale_customers(id),
    source          TEXT DEFAULT 'Email scan ibshi@',
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);


-- ── TABLE 31: sale_email_labels ──  (from 22_email_customer_labels.sql)
-- 47 Gmail customer labels from ibshi@ mailbox
CREATE TABLE IF NOT EXISTS sale_email_labels (
    id              TEXT PRIMARY KEY,
    label_name      TEXT NOT NULL,
    conversation_count INTEGER DEFAULT 0,
    customer_id     TEXT REFERENCES sale_customers(id),
    source          TEXT DEFAULT 'Gmail labels ibshi@',
    created_at      TEXT DEFAULT (datetime('now'))
);


-- ── TABLE 32: sale_email_full ──  (from 23_full_email_mapping.sql)
-- 108 emails from ibshi@ Chrome deep scan Jan-Apr 2026, business-intelligence focused
CREATE TABLE IF NOT EXISTS sale_email_full (
    id              TEXT PRIMARY KEY,
    email_date      TEXT NOT NULL,
    subject_summary TEXT NOT NULL,
    direction       TEXT,
    customer_name   TEXT,
    project_code    TEXT,
    email_type      TEXT,
    action_required TEXT,
    priority        TEXT,
    details         TEXT,
    customer_id     TEXT REFERENCES sale_customers(id),
    source          TEXT DEFAULT 'Email scan ibshi@ full',
    created_at      TEXT DEFAULT (datetime('now'))
);


-- ═══════════════════════════════════════════════════════════════
-- SECTION D: VIEWS
-- ═══════════════════════════════════════════════════════════════


-- Follow-up action items from email intelligence
CREATE VIEW IF NOT EXISTS v_sale_followups AS
SELECT email_date, customer_name, project_code, subject_summary, action_required, priority, details
FROM sale_email_full
WHERE action_required IN ('URGENT', 'ACTION_IBS', 'FOLLOW_UP', 'PENDING_PAYMENT', 'PENDING_APPROVAL')
ORDER BY
  CASE priority WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END,
  email_date DESC;

-- Project activity summary from email intelligence
CREATE VIEW IF NOT EXISTS v_project_activity AS
SELECT project_code, customer_name, COUNT(*) as email_count,
  MIN(email_date) as first_activity, MAX(email_date) as last_activity,
  GROUP_CONCAT(DISTINCT email_type) as activity_types,
  SUM(CASE WHEN action_required != 'NONE' THEN 1 ELSE 0 END) as pending_actions
FROM sale_email_full
GROUP BY project_code, customer_name
ORDER BY last_activity DESC;


-- ═══════════════════════════════════════════════════════════════
-- SECTION E: SEED DATA
-- ═══════════════════════════════════════════════════════════════


-- Product Categories (7 KHKD groups with FY2026 targets)
INSERT OR IGNORE INTO sale_product_categories (id, code, name_en, name_vn, target_tons, target_unit_price, target_revenue, target_gm_pct, target_gm_value) VALUES
('a1b2c3d4e5f6g7h8', 'HRSG', 'Heat Recovery Steam Generator', 'Nồi hơi tái tạo', 1200.0, 15920.83, 19095000, 21, 3976050),
('b2c3d4e5f6g7h8i9', 'DIVERTER', 'Diverter Valve', 'Van chuyển hướng', 800.0, 23887.5, 19110000, 21, 4013100),
('c3d4e5f6g7h8i9j0', 'SHIP', 'Ship Breaking', 'Cắt tàu', 1500.0, 12730.0, 19095000, 21, 4009950),
('d4e5f6g7h8i9j0k1', 'PV', 'Photovoltaic', 'Năng lượng mặt trời', 900.0, 21216.67, 19095000, 21, 4009950),
('e5f6g7h8i9j0k1l2', 'HANDLING', 'Material Handling', 'Vận chuyển vật liệu', 1100.0, 17359.09, 19095000, 21, 4009950),
('f6g7h8i9j0k1l2m3', 'DUCT', 'Ductwork', 'Ống dẫn khí', 700.0, 27278.57, 19095000, 21, 4009950),
('g7h8i9j0k1l2m3n4', 'OTHER', 'Other Products', 'Sản phẩm khác', 800.0, 23868.75, 19095000, 21, 4009950);

-- KHKD Targets (FY2026-2027)
INSERT OR IGNORE INTO sale_khkd_targets (id, fiscal_year, total_revenue_target, total_tons_target, total_gm_pct_target, total_gm_value_target, total_po_target, backlog_tons, workload_to_find, min_monthly_capacity) VALUES
('khkd-2026-2027-001', '2026-2027', 19095000, 7000, 21, 3976050, 25, 2667, 6333, 750);

-- Email Templates (6 standard templates)
INSERT OR IGNORE INTO sale_email_templates (id, template_type, subject, body, language, variables) VALUES
('tmpl-001', 'RFQ_ACK', 'Re: RFQ Acknowledgment', 'Dear {{customer_name}},

Thank you for your RFQ. We have received your request and will provide a quotation within 5 business days.

Best regards,
{{sender_name}}', 'en', '["customer_name", "sender_name"]'),
('tmpl-002', 'FOLLOWUP_3D', 'Quotation Status - 3 Day Follow-up', 'Dear {{customer_name}},

Following up on your RFQ from {{rfq_date}}. We are finalizing your quotation and will send it shortly.

Best regards,
{{sender_name}}', 'en', '["customer_name", "rfq_date", "sender_name"]'),
('tmpl-003', 'FOLLOWUP_7D', 'Quotation Status - 7 Day Follow-up', 'Dear {{customer_name}},

We are pleased to inform you that your quotation is being prepared. Please expect it within 2 business days.

Best regards,
{{sender_name}}', 'en', '["customer_name", "sender_name"]'),
('tmpl-004', 'FOLLOWUP_14D', 'Quotation Status - 14 Day Follow-up', 'Dear {{customer_name}},

We have sent you a detailed quotation on {{quote_date}}. Please review and let us know if you have any questions.

Best regards,
{{sender_name}}', 'en', '["customer_name", "quote_date", "sender_name"]'),
('tmpl-005', 'FOLLOWUP_30D', 'Quotation Review - 30 Day Follow-up', 'Dear {{customer_name}},

We would like to follow up on the quotation we provided on {{quote_date}}. We are interested in discussing next steps.

Best regards,
{{sender_name}}', 'en', '["customer_name", "quote_date", "sender_name"]'),
('tmpl-006', 'QUOTATION_COVER', 'Quotation Transmittal', 'Dear {{customer_name}},

Please find attached our quotation for {{project_name}}. We look forward to your feedback.

Best regards,
{{sender_name}}', 'en', '["customer_name", "project_name", "sender_name"]');

-- Monitored Mailboxes (2 initial mailboxes)
INSERT OR IGNORE INTO sale_monitored_mailboxes (id, email_address, display_name, department, owner_name, token_valid, sync_enabled, is_active) VALUES
('mbx-001', 'ibshi@ibs.com.vn', 'IBS HI Sales', 'SALE', 'Sales Team', 0, 1, 1),
('mbx-002', 'hieunh@ibs.com.vn', 'Hiệu NH', 'SALE', 'Hiệu Ngô Hồng', 0, 1, 1);

-- User Roles (5 initial users)
INSERT OR IGNORE INTO sale_user_roles (id, user_name, email, department, role, is_active) VALUES
('usr-001', 'Chairman', 'chairman@ibs.com.vn', 'SALE', 'ADMIN', 1),
('usr-002', 'Hiệu', 'hieunh@ibs.com.vn', 'SALE', 'MANAGER', 1),
('usr-003', 'Hùng', 'hungbt@ibs.com.vn', 'KTKH', 'MEMBER', 1),
('usr-004', 'Paul', 'paul@ibs.com.vn', 'SALE', 'MEMBER', 1),
('usr-005', 'Ngoãn', 'ngoan@ibs.com.vn', 'SALE', 'MEMBER', 1);


-- ═══════════════════════════════════════════════════════════════
-- END OF CONSOLIDATED SCHEMA
-- 32 tables + 2 views + seed data
-- ═══════════════════════════════════════════════════════════════
