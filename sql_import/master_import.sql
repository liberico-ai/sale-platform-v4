-- ═══════════════════════════════════════════════════════════════
-- IBS HI SALE PLATFORM - MASTER IMPORT SCRIPT
-- Generated: 2026-04-28 16:09:36
-- Run: sqlite3 sale.db < master_import.sql
-- ═══════════════════════════════════════════════════════════════

-- Create all 32 tables + 2 views + seed data
.read schema_all.sql

BEGIN TRANSACTION;

-- ═══ 01_customers.sql ═══
.read 01_customers.sql

-- ═══ 02_opportunities.sql ═══
.read 02_opportunities.sql

-- ═══ 02b_active_contracts.sql ═══
.read 02b_active_contracts.sql

-- ═══ 03_contract_milestones.sql ═══
.read 03_contract_milestones.sql

-- ═══ 04_settlements.sql ═══
.read 04_settlements.sql

-- ═══ 05_vogt_pipeline.sql ═══
.read 05_vogt_pipeline.sql

-- ═══ 06_nas_file_links.sql ═══
.read 06_nas_file_links.sql

-- ═══ 07_quotation_revisions.sql ═══
.read 07_quotation_revisions.sql

-- ═══ 08_contract_files.sql ═══
.read 08_contract_files.sql

-- ═══ 09_digital_content.sql ═══
.read 09_digital_content.sql

-- ═══ 10_product_opportunities.sql ═══
.read 10_product_opportunities.sql

-- ═══ 11_emails.sql (from ibshi@ibs.com.vn scan) ═══
.read 11_emails.sql

-- ═══ 12_customer_interactions.sql (from email analysis) ═══
.read 12_customer_interactions.sql

-- ═══ 13_market_signals.sql (from email pattern analysis) ═══
.read 13_market_signals.sql

-- ═══ 14_mbox_customers.sql (from 218MB mbox historical email extract) ═══
.read 14_mbox_customers.sql

-- ═══ 15_customer_contacts.sql (from mbox - all external contacts) ═══
.read 15_customer_contacts.sql

-- ═══ 16_email_stats.sql (enrich existing customers with mbox stats) ═══
.read 16_email_stats.sql

-- ═══ 17_quotation_enrichment.sql (from Quotation Record xlsx - 1,007 records) ═══
.read 17_quotation_enrichment.sql

-- ═══ 18_qr_customers.sql (new customers from Quotation Record Cus-Code) ═══
.read 18_qr_customers.sql

-- ═══ 19_won_contracts.sql (185 won contracts from Quotation Record Contract sheet) ═══
.read 19_won_contracts.sql

-- ═══ 20_email_2026_quotations.sql (from ibshi@ Chrome scan - 14 quotations + 17 RFQs) ═══
.read 20_email_2026_quotations.sql

-- ═══ 21_email_active_contracts.sql (14 active/ongoing contracts as of Apr 2026) ═══
.read 21_email_active_contracts.sql

-- ═══ 22_email_customer_labels.sql (47 Gmail customer labels) ═══
.read 22_email_customer_labels.sql

-- ═══ 23_full_email_mapping.sql (108 emails Jan-Apr 2026, full business mapping) ═══
.read 23_full_email_mapping.sql

-- ═══ 24_client_database.sql (172 customers + 164 contacts from Client_Data_Base GSheet) ═══
.read 24_client_database.sql

-- ═══ 25_client_visits.sql (142 client visits Oct 2022 – Apr 2026 from Client_Data_Base) ═══
.read 25_client_visits.sql

-- ═══ 99_import_log.sql ═══
.read 99_import_log.sql

COMMIT;

-- ═══ POST-IMPORT VALIDATION ═══
SELECT '=== RECORD COUNTS ===';
SELECT 'Customers: ' || COUNT(*) FROM sale_customers;
SELECT 'Customer Contacts: ' || COUNT(*) FROM sale_customer_contacts;
SELECT 'Opportunities: ' || COUNT(*) FROM sale_opportunities;
SELECT 'Contract Milestones: ' || COUNT(*) FROM sale_contract_milestones;
SELECT 'Settlements: ' || COUNT(*) FROM sale_settlements;
SELECT 'NAS File Links: ' || COUNT(*) FROM sale_nas_file_links;
SELECT 'Quotation Revisions: ' || COUNT(*) FROM sale_quotation_revisions;
SELECT 'Digital Content: ' || COUNT(*) FROM sale_digital_content;
SELECT 'Emails: ' || COUNT(*) FROM sale_emails;
SELECT 'Customer Interactions: ' || COUNT(*) FROM sale_customer_interactions;
SELECT 'Market Signals: ' || COUNT(*) FROM sale_market_signals;
SELECT 'Product Opportunities: ' || COUNT(*) FROM sale_product_opportunities;
SELECT 'Import Log: ' || COUNT(*) FROM sale_import_log;
SELECT 'Quotation History: ' || COUNT(*) FROM sale_quotation_history;
SELECT 'Active Contracts: ' || COUNT(*) FROM sale_active_contracts;
SELECT 'Email Labels: ' || COUNT(*) FROM sale_email_labels;
SELECT 'Email Full Map: ' || COUNT(*) FROM sale_email_full;
SELECT '--- TOTAL: ' || (SELECT COUNT(*) FROM sale_customers) + (SELECT COUNT(*) FROM sale_customer_contacts) + (SELECT COUNT(*) FROM sale_opportunities) + (SELECT COUNT(*) FROM sale_contract_milestones) + (SELECT COUNT(*) FROM sale_settlements) + (SELECT COUNT(*) FROM sale_nas_file_links) + (SELECT COUNT(*) FROM sale_quotation_revisions) + (SELECT COUNT(*) FROM sale_digital_content) + (SELECT COUNT(*) FROM sale_emails) + (SELECT COUNT(*) FROM sale_customer_interactions) + (SELECT COUNT(*) FROM sale_market_signals) + (SELECT COUNT(*) FROM sale_product_opportunities) + (SELECT COUNT(*) FROM sale_quotation_history) + (SELECT COUNT(*) FROM sale_active_contracts) + (SELECT COUNT(*) FROM sale_email_labels) + (SELECT COUNT(*) FROM sale_email_full) || ' records across all tables ---';

-- ═══ INTEGRITY CHECKS ═══
SELECT '=== INTEGRITY CHECKS ===';
SELECT 'Orphan opportunities (no customer): ' || COUNT(*) FROM sale_opportunities WHERE customer_id IS NOT NULL AND customer_id NOT IN (SELECT id FROM sale_customers);
SELECT 'Orphan emails (no customer): ' || COUNT(*) FROM sale_emails WHERE customer_id IS NOT NULL AND customer_id NOT IN (SELECT id FROM sale_customers);
SELECT 'Orphan interactions (no customer): ' || COUNT(*) FROM sale_customer_interactions WHERE customer_id NOT IN (SELECT id FROM sale_customers);
SELECT 'Orphan contacts (no customer): ' || COUNT(*) FROM sale_customer_contacts WHERE customer_id NOT IN (SELECT id FROM sale_customers);
SELECT 'Product groups: ' || GROUP_CONCAT(DISTINCT product_group) FROM sale_opportunities;
SELECT 'Stages: ' || GROUP_CONCAT(DISTINCT stage) FROM sale_opportunities;
SELECT 'Email types: ' || GROUP_CONCAT(DISTINCT email_type) FROM sale_emails;
SELECT 'Interaction types: ' || GROUP_CONCAT(DISTINCT interaction_type) FROM sale_customer_interactions;
SELECT 'Signal impacts: ' || GROUP_CONCAT(DISTINCT impact_level) FROM sale_market_signals;

-- ═══ MARKETING DATABASE STATS ═══
SELECT '=== MARKETING DATABASE (from mbox) ===';
SELECT 'Customers with contacts: ' || COUNT(DISTINCT customer_id) FROM sale_customer_contacts;
SELECT 'Total contacts: ' || COUNT(*) FROM sale_customer_contacts;
SELECT 'Primary contacts: ' || COUNT(*) FROM sale_customer_contacts WHERE is_primary = 1;
SELECT 'Customers with business_description containing MBOX: ' || COUNT(*) FROM sale_customers WHERE business_description LIKE '%MBOX%';