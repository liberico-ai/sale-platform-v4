-- ═══════════════════════════════════════════════════════════════════════════════
-- IBS HI SALE PLATFORM v4 - SQLite Schema
-- Phase 1: Email + Task + Pipeline Management
-- Generated: 2026-04-15
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════
-- TABLE 1: sale_customers
-- Source: Workflow 2026 (988 records) + khach_hang (63 records)
-- Tracks all customers with contact info, status, and legacy links
-- ═══════════════════════════════════════════════════════════════
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


-- ═══════════════════════════════════════════════════════════════
-- TABLE 2: sale_customer_contacts
-- Individual contacts within customer organizations
-- ═══════════════════════════════════════════════════════════════
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


-- ═══════════════════════════════════════════════════════════════
-- TABLE 3: sale_product_categories
-- KHKD product groups and revenue targets
-- 7 categories: HRSG, DIVERTER, SHIP, PV, HANDLING, DUCT, OTHER
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_product_categories (
    id              TEXT PRIMARY KEY,
    code            TEXT UNIQUE NOT NULL,
    name_en         TEXT NOT NULL,
    name_vn         TEXT,
    target_tons     REAL,
    target_unit_price REAL,  -- NUMERIC(15,2) in PostgreSQL
    target_revenue  REAL,    -- NUMERIC(15,2) in PostgreSQL
    target_gm_pct   REAL,
    target_gm_value REAL,    -- NUMERIC(15,2) in PostgreSQL
    created_at      TEXT DEFAULT (datetime('now'))
);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 4: sale_opportunities
-- Central pipeline table: links emails, tasks, and deals
-- Tracks stage progression, financial metrics, and NAS references
-- ═══════════════════════════════════════════════════════════════
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
    contract_value_vnd      REAL,    -- NUMERIC(15,2) in PostgreSQL
    contract_value_usd      REAL,    -- NUMERIC(15,2) in PostgreSQL
    unit_price_usd          REAL,    -- NUMERIC(15,2) in PostgreSQL
    gm_percent              REAL,
    gm_value_usd            REAL,    -- NUMERIC(15,2) in PostgreSQL
    material_cost_usd       REAL,    -- NUMERIC(15,2) in PostgreSQL
    labor_cost_usd          REAL,    -- NUMERIC(15,2) in PostgreSQL
    subcontractor_cost_usd  REAL,    -- NUMERIC(15,2) in PostgreSQL
    profit_usd              REAL,    -- NUMERIC(15,2) in PostgreSQL
    estimated_signing       TEXT,
    start_date              TEXT,
    duration_months         INTEGER,
    end_date                TEXT,
    quotation_date          TEXT,
    qty_2025                REAL,
    value_2025              REAL,    -- NUMERIC(15,2) in PostgreSQL
    gp_2025                 REAL,    -- NUMERIC(15,2) in PostgreSQL
    qty_2026                REAL,
    value_2026              REAL,    -- NUMERIC(15,2) in PostgreSQL
    gp_2026                 REAL,    -- NUMERIC(15,2) in PostgreSQL
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


-- ═══════════════════════════════════════════════════════════════
-- TABLE 5: sale_emails
-- Synced from Gmail via API
-- Classifies email type, links to opportunities and customers
-- ═══════════════════════════════════════════════════════════════
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


-- ═══════════════════════════════════════════════════════════════
-- TABLE 6: sale_tasks
-- Unified task engine for all work types
-- Routes between SALE, KTKH, KT, SX, TM, QLDA, TCKT, QAQC departments
-- ═══════════════════════════════════════════════════════════════
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


-- ═══════════════════════════════════════════════════════════════
-- TABLE 7: sale_follow_up_schedules
-- Automated reminder engine for quotations and negotiations
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_follow_up_schedules (
    id              TEXT PRIMARY KEY,
    opportunity_id  TEXT NOT NULL REFERENCES sale_opportunities(id),
    schedule_type   TEXT NOT NULL,
    reminder_days   TEXT,
    next_follow_up  TEXT,
    last_follow_up  TEXT,
    follow_up_count INTEGER DEFAULT 0,
    is_active       INTEGER DEFAULT 1,
    created_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_sfu_next ON sale_follow_up_schedules(next_follow_up);
CREATE INDEX IF NOT EXISTS idx_sfu_opp ON sale_follow_up_schedules(opportunity_id);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 8: sale_email_templates
-- Pre-built email templates for standard communications
-- Supports RFQ ack, follow-ups at 3/7/14/30 days, quotation covers
-- ═══════════════════════════════════════════════════════════════
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


-- ═══════════════════════════════════════════════════════════════
-- TABLE 9: sale_email_activity_log
-- Audit trail for all email actions
-- Tracks classification, task creation, linking, and escalation
-- ═══════════════════════════════════════════════════════════════
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


-- ═══════════════════════════════════════════════════════════════
-- TABLE 10: sale_khkd_targets
-- Business plan tracking for FY2026-2027
-- Total: $19.1M revenue, 7000 tons, 21% GM, 25 POs
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale_khkd_targets (
    id              TEXT PRIMARY KEY,
    fiscal_year     TEXT NOT NULL,
    total_revenue_target    REAL,    -- NUMERIC(15,2) in PostgreSQL
    total_tons_target       REAL,
    total_gm_pct_target     REAL,
    total_gm_value_target   REAL,    -- NUMERIC(15,2) in PostgreSQL
    total_po_target         INTEGER,
    backlog_tons            REAL,
    workload_to_find        REAL,
    min_monthly_capacity    REAL,
    created_at      TEXT DEFAULT (datetime('now'))
);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 11: sale_nas_file_links
-- References to NAS file storage
-- Files stay on NAS; paths indexed here for quick lookup
-- ═══════════════════════════════════════════════════════════════
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


-- ═══════════════════════════════════════════════════════════════
-- TABLE 12: sale_monitored_mailboxes
-- Gmail mailboxes synced with the platform
-- Supports add/remove as employees join/leave
-- ═══════════════════════════════════════════════════════════════
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


-- ═══════════════════════════════════════════════════════════════
-- TABLE 13: sale_user_roles
-- Platform access control and department assignments
-- 5 levels: ADMIN, MANAGER, MEMBER, VIEWER
-- ═══════════════════════════════════════════════════════════════
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


-- ═══════════════════════════════════════════════════════════════
-- TABLE 14: sale_pm_sync_log
-- 2-way sync audit: Sale (L2) ↔ PM/Workflow (L1)
-- Tracks all data exchanges, drafts awaiting review
-- ═══════════════════════════════════════════════════════════════
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


-- ═══════════════════════════════════════════════════════════════
-- TABLE 15: sale_import_log
-- Mandatory audit log for all data imports
-- ═══════════════════════════════════════════════════════════════
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


-- ═══════════════════════════════════════════════════════════════
-- 16. AUDIT LOG (S1.7)
-- Tracks changes to financial fields, status transitions, role changes
-- ═══════════════════════════════════════════════════════════════
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

CREATE INDEX IF NOT EXISTS idx_audit_entity
    ON sale_audit_log(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_created
    ON sale_audit_log(created_at);

-- ═══════════════════════════════════════════════════════════════
-- SEED DATA
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
