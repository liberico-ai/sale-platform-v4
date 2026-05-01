-- ═══════════════════════════════════════════════════════════
-- 21_email_active_contracts.sql
-- Source: ibshi@ibs.com.vn Chrome scan 2026-04-29 10:11:33
-- Active/ongoing contracts and POs as of April 29, 2026
-- ═══════════════════════════════════════════════════════════

-- === ACTIVE CONTRACTS TABLE ===
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

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-f7878c43', 'V000016698', 'Vogt Power International (VPI)', 'V17565 Bison Generation Station', 'Duct/HRSG/ER/S-B/PS-PK', 'ACTIVE_FABRICATION', '2024-01', '2026-04-29', 'Multiple scopes: Ductwork Inlet, ER, S/B, PS PK. Daily transmittals. V17565-DTNG-1422', 'DoTrongLuu', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-de284aa5', 'V000016274', 'Vogt Power International (VPI)', 'V17556', 'NPP/Storage', 'ACTIVE_STORAGE', '2024-01', '2026-03-31', 'Storage cost fixed cost. Milestone 4 paid. PO Change Order 3 signed Feb 2026', 'Tony', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-fe8fa828', '70923356', 'Wendt Noise Control (WNC)', '325021 Wisconsin', 'Silencer/Acoustic', 'ACTIVE_SHIPPING', '2025-01', '2026-04-29', 'Shipment 3 final weight done. Milestone 4 invoice EUR 43,170.23 sent today. Rev 5 PO.', 'Pham Huy', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-a0668029', '70924364', 'Wendt Noise Control (WNC)', '325072 Dominion Urquhart', 'Silencer/Acoustic', 'ACTIVE_FABRICATION', '2026-02', '2026-04-28', 'New PO Feb 2026. Milestones 1-3 done. Material procurement inspection report submitted.', 'Hải TQ', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-88aacad7', '70923693', 'Wendt Noise Control (WNC)', 'NIPSCO', 'Silencer/Acoustic', 'ACTIVE_FABRICATION', '2026-02', '2026-04-28', 'Milestones 1-3 done. EUR 20,203.20 milestone 3 invoice. Performance bond issued.', 'Hải TQ', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-f982e7ec', '219864', 'Braden Europe (Braden)', '13164 HAJR Units 81-83', 'Duct/Damper/HRSG/EJ', 'FINAL_SETTLEMENT', '2023-01', '2026-04-28', 'Units 81/82/83 final weight done. 20% late delivery penalty retention dispute. Change Order 1 V1.', 'Tony/Mạnh', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-ec690289', '219861', 'Braden Europe (Braden)', '13105 Ghazlan NE Units 1-2', 'Duct/Damper/HRSG/EJ', 'FINAL_SETTLEMENT', '2023-01', '2026-03-27', 'Units 1&2 final settlement. Change 2 signed. Milestone 5 invoices sent. Preservation painting.', 'Tony', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-2a3cb306', '220330', 'Braden Europe (Braden)', '12942 NEOM SE', 'Tarpaulin/Storage/Insurance', 'ACTIVE_STORAGE', '2024-01', '2026-04-29', 'Storage milestone 9 = $8,100. PO 221074 new insurance PO. Extend May-Jul 2026.', 'Tony', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-bdfd675b', 'BO000354', 'Siempelkamp/Büttner', '4.00256 Allendale Phase 1c', 'Duct', 'ACTIVE_FABRICATION', '2026-04', '2026-04-29', 'NEW PO Apr 2026! PO E120 Rev 1 signed. 50% down payment $11,920.25. Conversion table, quality docs.', 'DoTrongLuu/Thu', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-ed6f79e6', 'BN001326', 'Büttner', '1.00440 Bemidji', 'Duct/Stack', 'ACTIVE_FABRICATION', '2025-08', '2026-03-12', 'Milestone 4 invoiced. Quotation BN000959_E120 final settlement discussion.', 'Tony', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-faae44e2', 'BN001246', 'Büttner/Siempelkamp', 'Project (unknown)', 'Duct', 'ACTIVE', '2025-01', '2026-03-12', 'Milestones 3-4 invoiced. Payment confirmed.', 'Tony', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-a58caf35', '251623', 'Bruk(?)', 'Project 35062', 'Structure/Equipment', 'ACTIVE', '2025-01', '2026-03-03', 'Milestone 4 invoice. Payment follow-up.', 'Tony', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-ffcd5ae5', 'JC-24527', 'John Cockerill Energy (JCE)/Braden', 'NPP Non-Pressure Parts', 'NPP/Structure', 'ACTIVE_FABRICATION', '2024-12', '2026-06-26', '43+ message thread. Very active. GUIDI Laurence main contact.', 'Paul/Tony', 'Email scan ibshi@ 2026-04-29');

INSERT OR IGNORE INTO sale_active_contracts (id, po_number, customer_name, project_name, product_type, contract_status, start_date, latest_activity, value_notes, project_manager, source)
  VALUES ('contract-c115a7e3', 'OAK-CREEK', 'Wendt Noise Control (WNC)', 'Oak Creek 294831', 'Silencer/Acoustic', 'ACTIVE_SHIPPING', '2025-01', '2026-04-20', 'POs 4102689975/83/90. S06601043395 RFQ awarded. 06 packages received at yard Apr 18.', 'Felisha/Hoang', 'Email scan ibshi@ 2026-04-29');
