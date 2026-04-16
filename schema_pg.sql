-- ═══════════════════════════════════════════════════════════════════════════════
-- IBS HI SALE PLATFORM v4 - PostgreSQL Schema
-- Phase 1: Email + Task + Pipeline Management
-- Schema: "sale" in ibshi1 database
-- Generated: 2026-04-15
-- ═══════════════════════════════════════════════════════════════════════════════

-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS sale;
SET search_path TO sale, public;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ═══════════════════════════════════════════════════════════════
-- TABLE 1: sale.customers
-- Source: Workflow 2026 (988 records) + khach_hang (63 records)
-- Tracks all customers with contact info, status, and legacy links
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.customers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code            TEXT UNIQUE,
    name            TEXT NOT NULL,
    country         TEXT,
    region          TEXT,
    address         TEXT,
    website         TEXT,
    business_description TEXT,
    status          TEXT DEFAULT 'ACTIVE',
    legacy_id       INTEGER,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_sc_code ON sale.customers(code);
CREATE INDEX IF NOT EXISTS idx_sc_region ON sale.customers(region);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 2: sale.customer_contacts
-- Individual contacts within customer organizations
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.customer_contacts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id     UUID NOT NULL REFERENCES sale.customers(id),
    name            TEXT NOT NULL,
    email           TEXT,
    phone           TEXT,
    position        TEXT,
    linkedin        TEXT,
    is_primary      BOOLEAN DEFAULT false,
    created_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_scc_customer ON sale.customer_contacts(customer_id);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 3: sale.product_categories
-- KHKD product groups and revenue targets
-- 7 categories: HRSG, DIVERTER, SHIP, PV, HANDLING, DUCT, OTHER
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.product_categories (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code            TEXT UNIQUE NOT NULL,
    name_en         TEXT NOT NULL,
    name_vn         TEXT,
    target_tons     REAL,
    target_unit_price NUMERIC(15,2),
    target_revenue  NUMERIC(15,2),
    target_gm_pct   REAL,
    target_gm_value NUMERIC(15,2),
    created_at      TIMESTAMPTZ DEFAULT now()
);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 4: sale.opportunities
-- Central pipeline table: links emails, tasks, and deals
-- Tracks stage progression, financial metrics, and NAS references
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.opportunities (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pl_hd                   TEXT,
    product_group           TEXT NOT NULL,
    customer_id             UUID REFERENCES sale.customers(id),
    customer_name           TEXT,
    project_name            TEXT NOT NULL,
    scope_en                TEXT,
    scope_vn                TEXT,
    stage                   TEXT NOT NULL DEFAULT 'PROSPECT',
    win_probability         INTEGER DEFAULT 50,
    weight_ton              REAL,
    contract_value_vnd      NUMERIC(15,2),
    contract_value_usd      NUMERIC(15,2),
    unit_price_usd          NUMERIC(15,2),
    gm_percent              REAL,
    gm_value_usd            NUMERIC(15,2),
    material_cost_usd       NUMERIC(15,2),
    labor_cost_usd          NUMERIC(15,2),
    subcontractor_cost_usd  NUMERIC(15,2),
    profit_usd              NUMERIC(15,2),
    estimated_signing       DATE,
    start_date              DATE,
    duration_months         INTEGER,
    end_date                DATE,
    quotation_date          DATE,
    qty_2025                REAL,
    value_2025              NUMERIC(15,2),
    gp_2025                 NUMERIC(15,2),
    qty_2026                REAL,
    value_2026              NUMERIC(15,2),
    gp_2026                 NUMERIC(15,2),
    milestones              JSONB,
    assigned_to             TEXT,
    nas_quotation_path      TEXT,
    nas_contract_path       TEXT,
    notes                   TEXT,
    last_activity_date      TIMESTAMPTZ DEFAULT now(),
    stale_flag              BOOLEAN DEFAULT false,
    loss_reason             TEXT,
    competitor              TEXT,
    created_at              TIMESTAMPTZ DEFAULT now(),
    updated_at              TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_so_stage ON sale.opportunities(stage);
CREATE INDEX IF NOT EXISTS idx_so_customer ON sale.opportunities(customer_id);
CREATE INDEX IF NOT EXISTS idx_so_assigned ON sale.opportunities(assigned_to);
CREATE INDEX IF NOT EXISTS idx_so_product ON sale.opportunities(product_group);
CREATE INDEX IF NOT EXISTS idx_so_stale ON sale.opportunities(stale_flag);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 5: sale.emails
-- Synced from Gmail via API
-- Classifies email type, links to opportunities and customers
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.emails (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gmail_id        TEXT UNIQUE,
    thread_id       TEXT,
    mailbox_id      UUID REFERENCES sale.monitored_mailboxes(id),
    source_dept     TEXT,
    email_type      TEXT,
    confidence      REAL,
    from_address    TEXT,
    from_name       TEXT,
    to_addresses    JSONB,
    cc_addresses    JSONB,
    subject         TEXT,
    snippet         TEXT,
    body_text       TEXT,
    has_attachments BOOLEAN DEFAULT false,
    attachment_names JSONB,
    received_at     TIMESTAMPTZ,
    processed_at    TIMESTAMPTZ,
    opportunity_id  UUID REFERENCES sale.opportunities(id),
    customer_id     UUID REFERENCES sale.customers(id),
    is_read         BOOLEAN DEFAULT false,
    is_actioned     BOOLEAN DEFAULT false,
    actioned_by     TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_se_type ON sale.emails(email_type);
CREATE INDEX IF NOT EXISTS idx_se_thread ON sale.emails(thread_id);
CREATE INDEX IF NOT EXISTS idx_se_opp ON sale.emails(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_se_received ON sale.emails(received_at);
CREATE INDEX IF NOT EXISTS idx_se_gmail ON sale.emails(gmail_id);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 6: sale.tasks
-- Unified task engine for all work types
-- Routes between SALE, KTKH, KT, SX, TM, QLDA, TCKT, QAQC departments
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.tasks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id  UUID REFERENCES sale.opportunities(id),
    email_id        UUID REFERENCES sale.emails(id),
    parent_task_id  UUID REFERENCES sale.tasks(id),
    task_type       TEXT NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT,
    from_dept       TEXT NOT NULL,
    to_dept         TEXT NOT NULL,
    assigned_to     TEXT,
    assigned_by     TEXT,
    sla_hours       INTEGER,
    due_date        DATE,
    status          TEXT NOT NULL DEFAULT 'PENDING',
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    result          TEXT,
    is_escalated    BOOLEAN DEFAULT false,
    escalated_to    TEXT,
    escalated_at    TIMESTAMPTZ,
    escalation_count INTEGER DEFAULT 0,
    nas_file_path   TEXT,
    attachments     JSONB,
    priority        TEXT DEFAULT 'NORMAL',
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_st_status ON sale.tasks(status);
CREATE INDEX IF NOT EXISTS idx_st_assigned ON sale.tasks(assigned_to);
CREATE INDEX IF NOT EXISTS idx_st_opp ON sale.tasks(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_st_due ON sale.tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_st_type ON sale.tasks(task_type);
CREATE INDEX IF NOT EXISTS idx_st_dept ON sale.tasks(to_dept);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 7: sale.follow_up_schedules
-- Automated reminder engine for quotations and negotiations
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.follow_up_schedules (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id  UUID NOT NULL REFERENCES sale.opportunities(id),
    schedule_type   TEXT NOT NULL,
    reminder_days   JSONB,
    next_follow_up  DATE,
    last_follow_up  DATE,
    follow_up_count INTEGER DEFAULT 0,
    is_active       BOOLEAN DEFAULT true,
    created_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_sfu_next ON sale.follow_up_schedules(next_follow_up);
CREATE INDEX IF NOT EXISTS idx_sfu_opp ON sale.follow_up_schedules(opportunity_id);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 8: sale.email_templates
-- Pre-built email templates for standard communications
-- Supports RFQ ack, follow-ups at 3/7/14/30 days, quotation covers
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.email_templates (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_type   TEXT NOT NULL UNIQUE,
    subject         TEXT,
    body            TEXT,
    language        TEXT DEFAULT 'en',
    variables       JSONB,
    is_active       BOOLEAN DEFAULT true,
    created_at      TIMESTAMPTZ DEFAULT now()
);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 9: sale.email_activity_log
-- Audit trail for all email actions
-- Tracks classification, task creation, linking, and escalation
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.email_activity_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_id        UUID REFERENCES sale.emails(id),
    opportunity_id  UUID REFERENCES sale.opportunities(id),
    task_id         UUID REFERENCES sale.tasks(id),
    action_type     TEXT NOT NULL,
    action_by       TEXT,
    details         JSONB,
    created_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_seal_email ON sale.email_activity_log(email_id);
CREATE INDEX IF NOT EXISTS idx_seal_opp ON sale.email_activity_log(opportunity_id);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 10: sale.khkd_targets
-- Business plan tracking for FY2026-2027
-- Total: $19.1M revenue, 7000 tons, 21% GM, 25 POs
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.khkd_targets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fiscal_year     TEXT NOT NULL,
    total_revenue_target    NUMERIC(15,2),
    total_tons_target       REAL,
    total_gm_pct_target     REAL,
    total_gm_value_target   NUMERIC(15,2),
    total_po_target         INTEGER,
    backlog_tons            REAL,
    workload_to_find        REAL,
    min_monthly_capacity    REAL,
    created_at      TIMESTAMPTZ DEFAULT now()
);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 11: sale.nas_file_links
-- References to NAS file storage
-- Files stay on NAS; paths indexed here for quick lookup
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.nas_file_links (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type     TEXT NOT NULL,
    entity_id       UUID NOT NULL,
    nas_path        TEXT NOT NULL,
    file_name       TEXT,
    file_type       TEXT,
    description     TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_snfl_entity ON sale.nas_file_links(entity_type, entity_id);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 12: sale.monitored_mailboxes
-- Gmail mailboxes synced with the platform
-- Supports add/remove as employees join/leave
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.monitored_mailboxes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_address   TEXT UNIQUE NOT NULL,
    display_name    TEXT,
    department      TEXT NOT NULL,
    owner_name      TEXT,
    oauth_token     JSONB,
    token_valid     BOOLEAN DEFAULT false,
    sync_enabled    BOOLEAN DEFAULT true,
    sync_from_date  DATE,
    last_sync_at    TIMESTAMPTZ,
    last_sync_count INTEGER DEFAULT 0,
    is_active       BOOLEAN DEFAULT true,
    deactivated_at  TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_smm_email ON sale.monitored_mailboxes(email_address);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 13: sale.user_roles
-- Platform access control and department assignments
-- 5 levels: ADMIN, MANAGER, MEMBER, VIEWER
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.user_roles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_name       TEXT NOT NULL,
    email           TEXT UNIQUE,
    department      TEXT NOT NULL,
    role            TEXT NOT NULL DEFAULT 'MEMBER',
    permissions     JSONB,
    is_active       BOOLEAN DEFAULT true,
    joined_at       TIMESTAMPTZ DEFAULT now(),
    deactivated_at  TIMESTAMPTZ,
    l1_user_id      UUID,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_sur_dept ON sale.user_roles(department);
CREATE INDEX IF NOT EXISTS idx_sur_active ON sale.user_roles(is_active);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 14: sale.pm_sync_log
-- 2-way sync audit: Sale (L2) ↔ PM/Workflow (L1)
-- Tracks all data exchanges, drafts awaiting review
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.pm_sync_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    direction       TEXT NOT NULL,
    source_entity   TEXT NOT NULL,
    source_id       UUID NOT NULL,
    target_entity   TEXT NOT NULL,
    target_id       UUID,
    opportunity_id  UUID REFERENCES sale.opportunities(id),
    project_code    TEXT,
    sync_type       TEXT NOT NULL,
    action          TEXT NOT NULL,
    payload         JSONB,
    status          TEXT NOT NULL DEFAULT 'PENDING',
    error_message   TEXT,
    triggered_by    TEXT,
    reviewed_by     TEXT,
    reviewed_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_spsl_direction ON sale.pm_sync_log(direction);
CREATE INDEX IF NOT EXISTS idx_spsl_project ON sale.pm_sync_log(project_code);
CREATE INDEX IF NOT EXISTS idx_spsl_opp ON sale.pm_sync_log(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_spsl_status ON sale.pm_sync_log(status);


-- ═══════════════════════════════════════════════════════════════
-- TABLE 15: sale.import_log
-- Mandatory audit log for all data imports
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.import_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    import_type     TEXT NOT NULL,
    source_file     TEXT,
    records_total   INTEGER,
    records_imported INTEGER,
    records_failed  INTEGER,
    errors          JSONB,
    imported_by     TEXT,
    started_at      TIMESTAMPTZ DEFAULT now(),
    completed_at    TIMESTAMPTZ
);


-- ═══════════════════════════════════════════════════════════════
-- 16. AUDIT LOG (S1.7)
-- Tracks changes to financial fields, status transitions, role changes
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS sale.audit_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type     TEXT NOT NULL,
    entity_id       UUID NOT NULL,
    action          TEXT NOT NULL,
    field_name      TEXT,
    old_value       TEXT,
    new_value       TEXT,
    changed_by      TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_audit_entity
    ON sale.audit_log(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_created
    ON sale.audit_log(created_at);


-- ═══════════════════════════════════════════════════════════════
-- SEED DATA
-- ═══════════════════════════════════════════════════════════════

-- Product Categories (7 KHKD groups with FY2026 targets)
INSERT INTO sale.product_categories (id, code, name_en, name_vn, target_tons, target_unit_price, target_revenue, target_gm_pct, target_gm_value)
VALUES
('a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d'::uuid, 'HRSG', 'Heat Recovery Steam Generator', 'Nồi hơi tái tạo', 1200.0, 15920.83, 19095000, 21, 3976050),
('b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e'::uuid, 'DIVERTER', 'Diverter Valve', 'Van chuyển hướng', 800.0, 23887.5, 19110000, 21, 4013100),
('c3d4e5f6-a7b8-4c9d-ae1f-2a3b4c5d6e7f'::uuid, 'SHIP', 'Ship Breaking', 'Cắt tàu', 1500.0, 12730.0, 19095000, 21, 4009950),
('d4e5f6a7-b8c9-4d0e-bf2a-3b4c5d6e7f8a'::uuid, 'PV', 'Photovoltaic', 'Năng lượng mặt trời', 900.0, 21216.67, 19095000, 21, 4009950),
('e5f6a7b8-c9d0-4e1f-8a3b-4c5d6e7f8a9b'::uuid, 'HANDLING', 'Material Handling', 'Vận chuyển vật liệu', 1100.0, 17359.09, 19095000, 21, 4009950),
('f6a7b8c9-d0e1-4f2a-8b4c-5d6e7f8a9b0c'::uuid, 'DUCT', 'Ductwork', 'Ống dẫn khí', 700.0, 27278.57, 19095000, 21, 4009950),
('a7b8c9d0-e1f2-4a3b-8c5d-6e7f8a9b0c1d'::uuid, 'OTHER', 'Other Products', 'Sản phẩm khác', 800.0, 23868.75, 19095000, 21, 4009950)
ON CONFLICT (code) DO NOTHING;

-- KHKD Targets (FY2026-2027)
INSERT INTO sale.khkd_targets (id, fiscal_year, total_revenue_target, total_tons_target, total_gm_pct_target, total_gm_value_target, total_po_target, backlog_tons, workload_to_find, min_monthly_capacity)
VALUES
('b8c9d0e1-f2a3-4b4c-8d6e-7f8a9b0c1d2e'::uuid, '2026-2027', 19095000, 7000, 21, 3976050, 25, 2667, 6333, 750)
ON CONFLICT DO NOTHING;

-- Email Templates (6 standard templates)
INSERT INTO sale.email_templates (id, template_type, subject, body, language, variables)
VALUES
('c9d0e1f2-a3b4-4c5d-8e7f-8a9b0c1d2e3f'::uuid, 'RFQ_ACK', 'Re: RFQ Acknowledgment', 'Dear {{customer_name}},

Thank you for your RFQ. We have received your request and will provide a quotation within 5 business days.

Best regards,
{{sender_name}}', 'en', '["customer_name", "sender_name"]'::jsonb),
('d0e1f2a3-b4c5-4d6e-8f8a-9b0c1d2e3f4a'::uuid, 'FOLLOWUP_3D', 'Quotation Status - 3 Day Follow-up', 'Dear {{customer_name}},

Following up on your RFQ from {{rfq_date}}. We are finalizing your quotation and will send it shortly.

Best regards,
{{sender_name}}', 'en', '["customer_name", "rfq_date", "sender_name"]'::jsonb),
('e1f2a3b4-c5d6-4e7f-8a9b-0c1d2e3f4a5b'::uuid, 'FOLLOWUP_7D', 'Quotation Status - 7 Day Follow-up', 'Dear {{customer_name}},

We are pleased to inform you that your quotation is being prepared. Please expect it within 2 business days.

Best regards,
{{sender_name}}', 'en', '["customer_name", "sender_name"]'::jsonb),
('f2a3b4c5-d6e7-4f8a-8b0c-1d2e3f4a5b6c'::uuid, 'FOLLOWUP_14D', 'Quotation Status - 14 Day Follow-up', 'Dear {{customer_name}},

We have sent you a detailed quotation on {{quote_date}}. Please review and let us know if you have any questions.

Best regards,
{{sender_name}}', 'en', '["customer_name", "quote_date", "sender_name"]'::jsonb),
('a3b4c5d6-e7f8-4a9b-8c1d-2e3f4a5b6c7d'::uuid, 'FOLLOWUP_30D', 'Quotation Review - 30 Day Follow-up', 'Dear {{customer_name}},

We would like to follow up on the quotation we provided on {{quote_date}}. We are interested in discussing next steps.

Best regards,
{{sender_name}}', 'en', '["customer_name", "quote_date", "sender_name"]'::jsonb),
('b4c5d6e7-f8a9-4b0c-8d2e-3f4a5b6c7d8e'::uuid, 'QUOTATION_COVER', 'Quotation Transmittal', 'Dear {{customer_name}},

Please find attached our quotation for {{project_name}}. We look forward to your feedback.

Best regards,
{{sender_name}}', 'en', '["customer_name", "project_name", "sender_name"]'::jsonb)
ON CONFLICT (template_type) DO NOTHING;

-- Monitored Mailboxes (2 initial mailboxes)
INSERT INTO sale.monitored_mailboxes (id, email_address, display_name, department, owner_name, token_valid, sync_enabled, is_active)
VALUES
('c5d6e7f8-a9b0-4c1d-8e3f-4a5b6c7d8e9f'::uuid, 'ibshi@ibs.com.vn', 'IBS HI Sales', 'SALE', 'Sales Team', false, true, true),
('d6e7f8a9-b0c1-4d2e-8f4a-5b6c7d8e9f0a'::uuid, 'hieunh@ibs.com.vn', 'Hiệu NH', 'SALE', 'Hiệu Ngô Hồng', false, true, true)
ON CONFLICT (email_address) DO NOTHING;

-- User Roles (5 initial users)
INSERT INTO sale.user_roles (id, user_name, email, department, role, is_active)
VALUES
('e7f8a9b0-c1d2-4e3f-8a5b-6c7d8e9f0a1b'::uuid, 'Chairman', 'chairman@ibs.com.vn', 'SALE', 'ADMIN', true),
('f8a9b0c1-d2e3-4f4a-8b6c-7d8e9f0a1b2c'::uuid, 'Hiệu', 'hieunh@ibs.com.vn', 'SALE', 'MANAGER', true),
('a9b0c1d2-e3f4-4a5b-8c7d-8e9f0a1b2c3d'::uuid, 'Hùng', 'hungbt@ibs.com.vn', 'KTKH', 'MEMBER', true),
('b0c1d2e3-f4a5-4b6c-8d8e-9f0a1b2c3d4e'::uuid, 'Paul', 'paul@ibs.com.vn', 'SALE', 'MEMBER', true),
('c1d2e3f4-a5b6-4c7d-8e9f-0a1b2c3d4e5f'::uuid, 'Ngoãn', 'ngoan@ibs.com.vn', 'SALE', 'MEMBER', true)
ON CONFLICT (email) DO NOTHING;
