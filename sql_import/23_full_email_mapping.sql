-- ═══════════════════════════════════════════════════════════
-- 23_full_email_mapping.sql
-- Source: ibshi@ibs.com.vn FULL Chrome scan 2026-04-29 10:22:12
-- Complete mapping of ALL business emails Jan-Apr 2026
-- ═══════════════════════════════════════════════════════════

-- === COMPREHENSIVE EMAIL MAPPING TABLE ===
CREATE TABLE IF NOT EXISTS sale_email_full (
    id              TEXT PRIMARY KEY,
    email_date      TEXT NOT NULL,
    subject_summary TEXT NOT NULL,
    direction       TEXT,  -- IBS→Client, Client→IBS, Internal
    customer_name   TEXT,
    project_code    TEXT,
    email_type      TEXT,  -- QUOTATION|INVOICE|SHIPPING|QC_INSPECTION|TRANSMITTAL|CONTRACT|CUSTOMER_BD|INTERNAL|DISPUTE|FOLLOW_UP
    action_required TEXT,  -- NONE|FOLLOW_UP|URGENT|PENDING_PAYMENT|PENDING_APPROVAL|ACTION_IBS|ACTION_CLIENT
    priority        TEXT,  -- HIGH|MEDIUM|LOW
    details         TEXT,
    customer_id     TEXT REFERENCES sale_customers(id),
    source          TEXT DEFAULT 'Email scan ibshi@ full',
    created_at      TEXT DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-4149f8c8', '2026-04-29', 'INVOICE PO 70923356 Milestone 4 Shipment 3', 'IBS→WNC', 'Wendt Noise Control', '70923356-WISCONSIN', 'INVOICE', 'PENDING_PAYMENT', 'HIGH', 'Invoice WNC-70923356-04.03, EUR 43,170.23. Milestone 4 upon readiness for shipping.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-861cfded', '2026-04-29', 'V17565 PK Pipe Rack member Sizing Change', 'VPI→IBS', 'Vogt Power International', 'V17565-BISON', 'TRANSMITTAL', 'ACTION_IBS', 'HIGH', 'Build-up beam proposal to catch-up schedule. Need VPI advice. 9 participants.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-cf28f385', '2026-04-29', 'Staffing Update / Contact Change', 'GEA/Jutta→Paul', 'GEA', 'GEA-GENERAL', 'CUSTOMER_BD', 'FOLLOW_UP', 'MEDIUM', 'Key contact Jutta appreciation + farewell. Account contact change at GEA.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-8c06aacb', '2026-04-29', 'Braden Capacity Tracker March 2025', 'IBS→Hung', 'Braden', 'BRADEN-CAPACITY', 'INTERNAL', 'NONE', 'LOW', 'FYI forward of capacity tracker to Hung Do.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-717f26f4', '2026-04-29', 'Transmittal V17565-DTNG-1422-00', 'VPI→IBS', 'Vogt Power International', 'V17565-BISON', 'TRANSMITTAL', 'ACTION_IBS', 'MEDIUM', 'Transmitted by Varakorn Onlamai.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-61784ce9', '2026-04-29', 'V17565.SDR.0227 GLT Tempmat insulation update', 'VPI/Aum→IBS/Luu', 'Vogt Power International', 'V17565-BISON', 'FOLLOW_UP', 'ACTION_IBS', 'HIGH', 'URGENT: GLT Tempmat insulation from USA. Has PO been issued? Update requested.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-16c1bf5d', '2026-04-29', 'Transmittal V17565-DTNG-1421-00', 'VPI→IBS', 'Vogt Power International', 'V17565-BISON', 'TRANSMITTAL', 'ACTION_IBS', 'MEDIUM', 'Transmitted by Sukanya Phimthong.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-a1d35378', '2026-04-28', 'NEOM PO 220330 storage May-Jul 2026 + PO 221074 insurance', 'Braden→IBS', 'Braden Europe', '12942-NEOM', 'CONTRACT', 'NONE', 'MEDIUM', 'PO signed by IBS. New insurance PO 221074. Extend storage May-Jul 2026.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-57db8578', '2026-04-28', 'HAJR PO 219864 late delivery penalty retention 20%', 'IBS→Braden/Ivan', 'Braden Europe', '13164-HAJR', 'DISPUTE', 'URGENT', 'HIGH', 'IBS disagrees with 20% suspension. 3 invoices (mốc 45%) Braden giữ 20% Final value. Need resolution.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-7976135d', '2026-04-28', 'SCCD Slab Cebu Q26.041 quotation sent', 'IBS/Paul→Naoki/YBC', 'Yokogawa Bridge Corp', 'CEBU-MACTAN', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Q26.041 Steel-Concrete Composite Deck Slab quotation sent to Naoki-san.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-97044019', '2026-04-28', 'Invoice PO 70924364 Milestone 3 Dominion Urquhart', 'IBS→WNC', 'Wendt Noise Control', '70924364-DOMINION', 'INVOICE', 'PENDING_PAYMENT', 'HIGH', 'Invoice WNC-70924364-03, EUR 25,954.23. Material procurement report attached.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-8b66137f', '2026-04-28', 'Invoice PO 70923693 Milestone 3 NIPSCO', 'IBS→WNC', 'Wendt Noise Control', '70923693-NIPSCO', 'INVOICE', 'PENDING_PAYMENT', 'HIGH', 'Invoice WNC-70923693-03, EUR 20,203.20. Material procurement report attached.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-02edf202', '2026-04-28', 'VPI IBS HI Capacity Available + Upcoming Projects', 'IBS/Tony→VPI/Matt', 'Vogt Power International', 'VPI-UPCOMING', 'CUSTOMER_BD', 'FOLLOW_UP', 'HIGH', 'IBS has available capacity. Response to Matt Henning about upcoming projects.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-60017340', '2026-04-28', 'M/V AAL BRISBANE Voy.26006 Hai Phong NOA', 'AAL→IBS/Giang', 'AAL Shipping', 'SHIPPING-GENERAL', 'SHIPPING', 'ACTION_IBS', 'MEDIUM', 'Vessel AAL Brisbane calling Hai Phong. Notice of Arrival to IBS.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-956f6432', '2026-04-28', 'Barge Construction update request', 'IBS→Capt.John', 'Barge Client', 'BARGE-176X44', 'CUSTOMER_BD', 'FOLLOW_UP', 'HIGH', 'IBS sent company profile + specs. Requesting project status update. 10-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-af57aac0', '2026-04-28', 'Tecnimont Vietnam scouting 2nd campaign', 'IBS/Bằng→Nugroho', 'Tecnimont', 'TECNIMONT-SCOUTING', 'CUSTOMER_BD', 'FOLLOW_UP', 'HIGH', 'Visit confirmed May 18, 2026. Supplier qualification docs shared.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-8c5fb3f5', '2026-04-28', 'GHAZLAN Project Suspension letter no penalty U1 U2', 'IBS→internal', 'Braden Europe', '13105-GHAZLAN', 'CONTRACT', 'NONE', 'MEDIUM', 'Confirmation letter: no late delivery penalty for U1, U2. 27-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-f31508d8', '2026-04-28', 'IBS financial information 2025 request', 'Braden/Ivan→Paul', 'Braden Europe', 'BRADEN-ADMIN', 'CUSTOMER_BD', 'ACTION_IBS', 'MEDIUM', 'Annual finance report submission required by Braden. Compliance item.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-0454215d', '2026-04-28', 'Dominion Urquhart weekly photo reports request', 'WNC/Christian→IBS/Hai', 'Wendt Noise Control', '70924364-DOMINION', 'QC_INSPECTION', 'ACTION_IBS', 'HIGH', 'Wendt requests WEEKLY detailed photo reports for Dominion Urquhart going forward.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-b9b87166', '2026-04-28', 'Supplier Capability Questionnaire (Quang)', 'IBS→Quang', 'New prospect (Quang)', 'NEW-PROSPECT', 'CUSTOMER_BD', 'FOLLOW_UP', 'MEDIUM', 'IBS sent company profile. Name change notification. New customer approach.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-19018d4d', '2026-04-27', 'Strategic Fabrication Partnership Vietnam/Asia', 'Stein→Tony', 'Stein (Prospect)', 'STEIN-PARTNERSHIP', 'CUSTOMER_BD', 'ACTION_IBS', 'HIGH', 'Follow-up: NDA + Supplier Qualification Questionnaire still pending IBS feedback. Must respond.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-d29b1f50', '2026-04-27', 'V17565 Packing list shipment 565-16698-02 REJECTED', 'VPI/Babcock→IBS', 'Vogt Power International', 'V17565-BISON', 'QC_INSPECTION', 'URGENT', 'HIGH', 'Packing list for Ductwork Inlet REJECTED by David Hardison. Need correction.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-094efad7', '2026-04-27', 'Transmittals V17565-DTNG-1401/1399', 'VPI→IBS', 'Vogt Power International', 'V17565-BISON', 'TRANSMITTAL', 'ACTION_IBS', 'MEDIUM', 'Two transmittals from VPI.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-a03e6320', '2026-04-27', 'NIPSCO Material Procurement Inspection Report', 'IBS/Hai→WNC', 'Wendt Noise Control', '70923693-NIPSCO', 'QC_INSPECTION', 'NONE', 'MEDIUM', 'Inspection report submitted for review.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-0d013e79', '2026-04-25', 'Bison Packages Tarpping work - price too high', 'VPI/John→Paul', 'Vogt Power International', 'V17565-BISON', 'DISPUTE', 'ACTION_IBS', 'HIGH', 'John says IBS quote is TWICE what another vendor charged in November. Must re-quote or justify.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-44b133e3', '2026-04-24', 'V17565 Transmittal DDTS-0113 revision drawings', 'IBS/Luu→VPI/Aum', 'Vogt Power International', 'V17565-BISON', 'TRANSMITTAL', 'PENDING_APPROVAL', 'MEDIUM', 'Revision drawings submitted to VPI system. Awaiting advice.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-e9f87ebb', '2026-04-24', 'Deaerator Vessel Q26.061 SUWTE Malaysia', 'IBS/Paul→Client', 'SUWTE Project', 'SUWTE-DEAERATOR', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Q26.061 Deaerator PV with U-stamp sent. Malaysia project.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-947f3088', '2026-04-24', 'Transmittals V17565-DTNG-1394/1393', 'VPI→IBS', 'Vogt Power International', 'V17565-BISON', 'TRANSMITTAL', 'ACTION_IBS', 'MEDIUM', 'Two transmittals by Nattapon Chaipromma.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-5e840e17', '2026-04-23', 'HAJR PO 219864 Milestone 4 Unit 4 invoice overdue', 'IBS→Braden/Ivan', 'Braden Europe', '13164-HAJR', 'INVOICE', 'URGENT', 'HIGH', 'BRA-219864-04.01 (Unit 81) OVERDUE since Apr 18. BRA-219864-04.02 (Unit 82) due Apr 24. Payment follow-up.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-94b11335', '2026-04-23', 'Wisconsin PO 70923356 Shipment 3 Final Weight signed', 'IBS→WNC', 'Wendt Noise Control', '70923356-WISCONSIN', 'CONTRACT', 'NONE', 'MEDIUM', 'Acceptance of work Shipment 3 signed by IBS.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-80ce3eaa', '2026-04-23', 'Wendt/IBS HI forward to Huy Nguyen', 'WNC/Schneider→Huy', 'Wendt Noise Control', 'WNC-GENERAL', 'INTERNAL', 'NONE', 'LOW', 'FYI forward from Marcel Schneider to Huy Nguyen.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-b9cfd982', '2026-04-23', 'Bison Inspection notification Outlet Duct Unit 2', 'IBS/Hai→VPI', 'Vogt Power International', 'V17565-BISON', 'QC_INSPECTION', 'PENDING_APPROVAL', 'HIGH', 'V17565-NFI-008 Notice of Inspection submitted for Outlet Duct Unit 2.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-a371b5a4', '2026-04-22', 'Commercial Invoice Revisions Wendt POs for customs', 'IBS/Pham→Natalie/WNC', 'Wendt Noise Control', 'WNC-SHIPPING', 'SHIPPING', 'FOLLOW_UP', 'HIGH', 'Customs clearance issue. POs 4102689975/83/90. 22-msg thread. Piece count needed per PO line.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-ec1fef09', '2026-04-22', 'V17565 Transmittal DDTS-0111 Burner Duct', 'IBS/Luu→VPI/Aum', 'Vogt Power International', 'V17565-BISON', 'TRANSMITTAL', 'PENDING_APPROVAL', 'MEDIUM', 'Burner Duct drawings submitted to VPI system.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-6b5a115f', '2026-04-22', 'NEOM PO 220330 Storage Milestone 9', 'IBS→Braden', 'Braden Europe', '12942-NEOM', 'INVOICE', 'PENDING_PAYMENT', 'MEDIUM', 'Invoice BRA-220330-09, USD 8,100.00. Monthly storage.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-732669ba', '2026-04-22', 'Weekly Discussion Wisconsin cancelled', 'WNC/Schneider→IBS', 'Wendt Noise Control', '70923356-WISCONSIN', 'INTERNAL', 'NONE', 'LOW', 'Teams meeting cancelled then re-scheduled.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-01ae29b2', '2026-04-21', 'HAJR PO 219864 Change 1 V1 with IBS comments', 'IBS→Braden', 'Braden Europe', '13164-HAJR', 'CONTRACT', 'PENDING_APPROVAL', 'HIGH', 'Change Order with IBS comments. Reference docs: use date from each signed Acceptance of Work.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-62b9fa15', '2026-04-21', 'Gonnix FWS vessels Q26.038 báo giá sent', 'IBS/Paul→Nhat/Gonnix', 'Gonnix', 'GONNIX-FWS', 'QUOTATION', 'FOLLOW_UP', 'MEDIUM', 'Q26.038 Báo giá 03 bầu lọc FWS vessels Rev.0.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-3ca9f59b', '2026-04-20', 'Oak Creek S06601043395 6 packages received at yard', 'Felisha→IBS', 'Wendt Noise Control', 'OAK-CREEK', 'SHIPPING', 'FOLLOW_UP', 'MEDIUM', '06 packages received at yard Apr 18. Will update booking details. 30-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-9c0f9aa9', '2026-04-18', 'Đơn đề nghị điều chỉnh hóa đơn đấu thầu QG', 'IBS→dauthauquamang', 'Internal/Admin', 'ADMIN', 'INTERNAL', 'FOLLOW_UP', 'MEDIUM', 'Company name change from IBS LISEMCO to IBS Heavy Industry in national procurement system.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-9241334e', '2026-04-17', 'NEOM storage insurance 1-year extension', 'IBS→Braden/Ivan', 'Braden Europe', '12942-NEOM', 'CONTRACT', 'NONE', 'LOW', 'Insurance extension certificate attached. 12-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-f29cb368', '2026-04-17', 'WNC construction straps inquiry', 'IBS→WNC', 'Wendt Noise Control', 'WNC-SUPPLY', 'CUSTOMER_BD', 'ACTION_IBS', 'MEDIUM', 'Khách hàng WNC hỏi IBS/nhà cung cấp VN có cung cấp construction straps không.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-f5d7c7da', '2026-04-17', 'Metso 8 ton column RFQ Australia', 'Tony→Team', 'Metso', 'METSO-COLUMNS', 'QUOTATION', 'ACTION_IBS', 'HIGH', 'Q26.040 Acid & Elution Columns Mt Bundy Gold. Urgent delivery needed.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-5d87785c', '2026-04-16', 'HAJR Milestone 4 Unit 3 invoice', 'IBS→Braden', 'Braden Europe', '13164-HAJR', 'INVOICE', 'PENDING_PAYMENT', 'HIGH', 'Payment calculation + Acceptance of Work for Unit 3. Final weight and value.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-99c7bae3', '2026-04-15', 'HAJR Final Weight Units 82+83 follow-up', 'IBS→Braden/Ivan', 'Braden Europe', '13164-HAJR', 'FOLLOW_UP', 'PENDING_APPROVAL', 'HIGH', 'Change order for Final settlement U81/82/83 - has it been made? 13-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-54ea804f', '2026-04-15', 'Broadwing V6C899 Q26.011 Rev.1 sent', 'IBS/Paul→VPI/Kyle', 'Vogt Power International', 'V6C899-BROADWING', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Q26.011 Rev.1 Carbon Capture Ductwork quotation. 7-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-2ba6c983', '2026-04-15', 'WNC PO 70923693 Milestone 1 payment confirmed', 'IBS→WNC', 'Wendt Noise Control', '70923693-NIPSCO', 'INVOICE', 'NONE', 'LOW', 'Payment receipt confirmed.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-f47dcee8', '2026-04-15', 'WNC PO 70924364 Milestone 1 payment confirmed', 'IBS→WNC', 'Wendt Noise Control', '70924364-DOMINION', 'INVOICE', 'NONE', 'LOW', 'Payment receipt confirmed.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-ed1930eb', '2026-04-15', 'Allendale PO BO000354 Painting Position clarification', 'IBS/DoTrongLuu→Büttner/Bernhard', 'Siempelkamp/Büttner', 'BO000354-ALLENDALE', 'QC_INSPECTION', 'NONE', 'MEDIUM', 'Painting position clarification. 8-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-e39a99e9', '2026-04-14', 'Bachmann Goodrich-TX Q26.037 quotation sent', 'IBS/Paul→Bachmann/Mark/Matt', 'Bachmann Industries', 'BACHMANN-GOODRICH', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Q26.037 Bypass Exhaust Systems Rev.0.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-623518a0', '2026-04-14', 'Wisconsin PO 70923356 Revised order agree', 'IBS→WNC', 'Wendt Noise Control', '70923356-WISCONSIN', 'CONTRACT', 'NONE', 'MEDIUM', 'PO Rev 5 IBS comments. Weights approximate, don''t affect total. 6-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-78179d0f', '2026-04-14', 'KIỂM TRA CHỨNG TỪ shipping docs', 'IBS/Pham→Huy+Đoan', 'Wendt Noise Control', 'WNC-SHIPPING', 'SHIPPING', 'ACTION_IBS', 'HIGH', 'Shipping document verification. 2.70 EUR/kg average price for customs declaration. 75-msg thread!');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-9519cdb4', '2026-04-10', 'DTTC Rev 2 Vogt 095', 'IBS→internal', 'Internal', '25-VPI-I-095', 'INTERNAL', 'NONE', 'MEDIUM', 'Dự toán thi công bản sửa đổi Rev 2 project 25-VPI-I-095.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-1ac1a876', '2026-04-10', 'DTTC 26-SED-I-110 Duct + 25-WNC-I-104', 'IBS→internal', 'Internal', '26-SED-I-110', 'INTERNAL', 'NONE', 'MEDIUM', 'Construction estimates for Siempelkamp duct + WNC project.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-d79ee990', '2026-04-10', 'Allendale Quality Document Submission', 'IBS/Toan→Büttner/Bernhard', 'Siempelkamp/Büttner', 'BO000354-ALLENDALE', 'QC_INSPECTION', 'PENDING_APPROVAL', 'HIGH', 'Documents uploaded to Büttner system. Awaiting comments.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-c0469871', '2026-04-10', 'WNC Order 70923693 welding book', 'IBS→WNC/Jose', 'Wendt Noise Control', '70923693-NIPSCO', 'QC_INSPECTION', 'NONE', 'MEDIUM', 'Welding book for 4 items: MLI 1634, 1652, 1645, 1617.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-7ed81aea', '2026-04-08', 'Metso 6t columns Australia lead time 24-26wk', 'IBS/Tony→Metso/Igor', 'Metso', 'METSO-6T-COLUMNS', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Lead time reduction to 24-26 weeks possible. Need further evaluation. 13-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-10a6e3e1', '2026-04-06', 'Qatar Energy Urea Q26.060 duct work', 'IBS/Paul→KHPT/Lee', 'KHPT', 'KHPT-QATAR', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Q26.060 Rev.0. Validity 15 days.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-ccdfb892', '2026-04-04', 'Allendale PO BO000354 signed + invoice', 'IBS→Büttner/Bernhard', 'Siempelkamp/Büttner', 'BO000354-ALLENDALE', 'CONTRACT', 'NONE', 'HIGH', 'PO Rev 1 signed. Invoice BNE-BO000354-01 = $11,920.25 (50% down payment).');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-96bbde35', '2026-04-04', 'Hợp đồng Siempelkamp PO BO000354 Ducting internal', 'IBS→internal', 'Siempelkamp/Büttner', 'BO000354-ALLENDALE', 'INTERNAL', 'NONE', 'MEDIUM', 'PO revised: payment terms adjusted, fabrication item 5 added. 9-msg internal thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-9cfd5b6c', '2026-04-04', 'GHAZLAN preservation painting procedure', 'IBS/Toan→Braden/Huy', 'Braden Europe', '13105-GHAZLAN', 'QC_INSPECTION', 'ACTION_IBS', 'MEDIUM', 'Paint material arrived. Painting next week. Invite inspection.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-8c7f0232', '2026-04-02', 'Kanadevia VN Contact Steel Structure', 'IBS→Phuong/Kanadevia', 'Kanadevia', 'KANADEVIA', 'CUSTOMER_BD', 'FOLLOW_UP', 'MEDIUM', 'Vendor Information Card sent. New customer approach from Japan.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-c3e952c0', '2026-04-02', 'UAE Pressure Vessel inquiry ASME/ABS', 'IBS→Praphulla/UAE', 'UAE Client', 'UAE-PV', 'CUSTOMER_BD', 'FOLLOW_UP', 'HIGH', 'Inquiry for ASME U-stamped & ABS certified PVs for offshore/marine. FYI to Paul/Tony.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-6c49b915', '2026-04-02', 'HAJR Milestone 4 Unit 5 invoice + warranty', 'IBS→Braden', 'Braden Europe', '13164-HAJR', 'INVOICE', 'PENDING_PAYMENT', 'HIGH', 'BRA-219864-04.03 + Warranty Bond 36 months for Unit 5.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-385e9713', '2026-04-01', 'Đơn giá giao khoán 25-WNC-I-104 + others', 'IBS→internal', 'Internal', 'INTERNAL-DGKK', 'INTERNAL', 'NONE', 'LOW', 'Unit prices for WNC-104, LSC5-107, GON-108 projects.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-b7c60347', '2026-04-01', 'NEOM PO 220330 Milestone 7 payment confirmed', 'IBS→Braden/BE', 'Braden Europe', '12942-NEOM', 'INVOICE', 'NONE', 'LOW', 'Payment confirmed. 7-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-b7d69eb6', '2026-03-27', 'BASTROP HRSG NPP RFQ answered - HOT PROJECT', 'IBS/Paul→JCE/GUIDI', 'John Cockerill Energy', 'JCE-BASTROP', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Very hot Bastrop project. Manufacturing area plan + schedule sent. Teams meeting held.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-b4cf901a', '2026-03-27', 'HAJR Warranty Bond Unit 83 MOA signed', 'IBS→Braden/Ivan', 'Braden Europe', '13164-HAJR', 'CONTRACT', 'NONE', 'MEDIUM', 'Memorandum of Agreement signed by IBS for warranty. 4-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-f21543d0', '2026-03-27', 'HAJR Milestone 5 Unit 1+2 invoices sent', 'IBS→Braden', 'Braden Europe', '13105-GHAZLAN', 'INVOICE', 'PENDING_PAYMENT', 'HIGH', 'BRA-219861-05.01 = $25,137.00 (Unit 1), BRA-219861-05.02 = $24,952.50 (Unit 2). With Certificate of Origin.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-eebcbe29', '2026-03-27', 'WNC PO 70924364/70923693 Milestone 2 invoices', 'IBS→WNC', 'Wendt Noise Control', 'WNC-INVOICES', 'INVOICE', 'PENDING_PAYMENT', 'MEDIUM', 'WNC-70924364-02 = EUR 5,190.85, WNC-70923693-02 = EUR 4,040.64.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-1cd8c2c7', '2026-03-27', 'Braden invoice status payment shortfall', 'IBS→Braden/BE', 'Braden Europe', '13105-GHAZLAN', 'DISPUTE', 'FOLLOW_UP', 'HIGH', 'Received $491,896 vs expected $574,179.14. Shortfall $82,283.14. Need explanation.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-a78832e6', '2026-03-26', 'GEA RFQ 2 projects updated price requested', 'GEA/Jutta→Paul', 'GEA', 'GEA-PROJECTS', 'QUOTATION', 'ACTION_IBS', 'HIGH', 'Times difficult. Updated price requested. 73-msg thread!');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-da4ce759', '2026-03-24', 'GHAZLAN PO 219861 Change 2 signed', 'IBS→Braden/Lizette', 'Braden Europe', '13105-GHAZLAN', 'CONTRACT', 'NONE', 'MEDIUM', 'Change 2 signed by IBS. Final settlement.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-c7cfe468', '2026-03-21', 'NEOM PO 220330 Milestone 8 invoice', 'IBS→Braden', 'Braden Europe', '12942-NEOM', 'INVOICE', 'PENDING_PAYMENT', 'MEDIUM', 'Monthly storage invoice milestone 8.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-042d5f38', '2026-03-20', 'GHAZLAN PO 219861/219864 settlement proposal + invoices', 'IBS→Braden/Ivan', 'Braden Europe', '13105-GHAZLAN', 'DISPUTE', 'FOLLOW_UP', 'HIGH', 'Completed value + suspension cost. Advance payment clarification. Payment shortfall. 12-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-6bf2c58e', '2026-03-20', 'WNC PO 70924364 Advance+Performance Bonds', 'IBS→WNC', 'Wendt Noise Control', '70924364-DOMINION', 'CONTRACT', 'NONE', 'HIGH', 'Bond drafts sent. EUR 190/guarantee from Commerzbank discussion. 4-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-28cfe2bb', '2026-03-18', 'V17565 PO V000016698 ER + S/B Advance Payment invoices', 'IBS→VPI', 'Vogt Power International', 'V17565-BISON', 'INVOICE', 'PENDING_PAYMENT', 'HIGH', 'Two advance payment invoices for additional scopes ER and S/B.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-26ae200d', '2026-03-18', 'TD Platform Fabrication/Assembly RFQ', 'Jorge→IBS/Paul', 'TD Platform', 'TD-PLATFORM', 'CUSTOMER_BD', 'FOLLOW_UP', 'MEDIUM', 'RFQ for platform fabrication. Coating spec + fabrication scope + BOM attached.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-79cc225e', '2026-03-17', 'V17565 S/B bulk materials Change Order 8 signed', 'IBS→VPI/Aum', 'Vogt Power International', 'V17565-BISON', 'CONTRACT', 'NONE', 'HIGH', 'Change Order 8 for S/B bulk materials signed by IBS. 11-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-96484d61', '2026-03-16', 'YBC Cebu-Mactan Bridge Temporary Structures RFQ', 'YBC/Hiep→IBS/Tony', 'Yokogawa Bridge Corp', 'YBC-CEBU', 'QUOTATION', 'ACTION_IBS', 'HIGH', 'RFQ for temporary structures. Container or break bulk packaging. 2 PDF attachments.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-89c71018', '2026-03-12', 'Büttner PO BN001246 Milestone 4 payment confirmed', 'IBS→Büttner/Sandra', 'Siempelkamp/Büttner', 'BN001246', 'INVOICE', 'NONE', 'LOW', 'Payment receipt confirmed. 6-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-7fe49839', '2026-03-11', 'HAJR PO 219864 Unit 81 Final Weight', 'IBS→Braden/Ivan', 'Braden Europe', '13164-HAJR', 'CONTRACT', 'FOLLOW_UP', 'HIGH', 'RTS date proposal: Mar 10, 2026. 12-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-256c7984', '2026-03-11', 'Büttner Quotation BN000959 Final Settlement', 'IBS/Tony→Büttner/Bernhard', 'Siempelkamp/Büttner', 'BN000959-BUETTNER', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'IBS at ~80% workload capacity. Can accept. Duct+transition piece calculation sent.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-f25e261e', '2026-03-09', 'NEOM PO 220330 Change 2 storage extension', 'Tony→IBS', 'Braden Europe', '12942-NEOM', 'CONTRACT', 'NONE', 'MEDIUM', 'PO gia hạn lưu kho from Braden purchasing directly. Feb-Apr 2026.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-f68adfe5', '2026-03-04', 'WNC PO 70923693 Advance+Performance Bonds', 'IBS→WNC', 'Wendt Noise Control', '70923693-NIPSCO', 'CONTRACT', 'NONE', 'HIGH', 'Full signed PO + bond drafts. 3-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-4e3c1ad4', '2026-03-04', 'VPI Bison AIG Lances RFQ status update', 'IBS/Paul→VPI/Aum', 'Vogt Power International', 'V17565-BISON', 'FOLLOW_UP', 'FOLLOW_UP', 'MEDIUM', 'Package status update requested. 6-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-0d92f315', '2026-02-28', 'Wisconsin PO 70923356 Final Payment Shipment 2 + Milestone 3', 'IBS→WNC', 'Wendt Noise Control', '70923356-WISCONSIN', 'INVOICE', 'PENDING_PAYMENT', 'HIGH', 'Final payment shipment 1 invoice + Milestone 3 invoice. Revised bank account. 7-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-08ca79b9', '2026-02-25', 'Bachmann Q26.019 Outlet Duct Damper (Corten)', 'IBS/Paul→Bachmann/Matt', 'Bachmann Industries', 'BACHMANN-DAMPER', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Important confirmation acknowledged by Matt. 8-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-d62a4596', '2026-02-24', 'VPI V38000 Urquhart LB Pipe Support Steel RFQ', 'VPI/Sam→IBS/Tony', 'Vogt Power International', 'V38000-URQUHART', 'QUOTATION', 'ACTION_IBS', 'HIGH', 'Quotation due: Mar 13. Order date: Mar 20. Required RTS FCA.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-76acc224', '2026-02-23', 'WNC PO 70924364 Dominion Urquhart PO + timeline', 'WNC→IBS', 'Wendt Noise Control', '70924364-DOMINION', 'CONTRACT', 'NONE', 'HIGH', 'Purchase Order issued. IBS comments + Excel proposal. Time schedule. 7-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-9d31d8e1', '2026-02-23', 'V17565 PO V000016698 PS PK Advance Payment', 'IBS→VPI/Aum', 'Vogt Power International', 'V17565-BISON', 'INVOICE', 'PENDING_PAYMENT', 'HIGH', 'Partial Lien Waiver for PS PK advance payment invoice.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-54590d91', '2026-02-14', 'V17556 NPP IBS RFQ storage cost PO Change 3', 'IBS→VPI/Pawat', 'Vogt Power International', 'V17556', 'CONTRACT', 'NONE', 'MEDIUM', 'PO Change Order 3 signed. Storage cost. 23-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-3d9eea0b', '2026-02-13', 'V17556 PO V000016274 Milestone 4 invoice revised', 'IBS→VPI/Pawat', 'Vogt Power International', 'V17556', 'INVOICE', 'PENDING_PAYMENT', 'HIGH', 'Revised invoice $203,682.77. 7-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-e5e38a05', '2026-02-05', 'BEUMER Conveyor Q25.138 + RFQ Optional Scope B', 'BEUMER/Klaus→IBS/Tony', 'BEUMER Group', 'BEUMER-CONVEYOR', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Project ongoing. Fabrication of conveyor frames requested. Clarification + audit docs. 4-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-70fbea93', '2026-01-29', 'Berg Process Iraq Fuel Gas Q26.101', 'IBS/Paul→Berg/Hanas', 'Berg Process', 'BERG-IRAQ', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Q26.101 2 identical Inlet Filter Coalescer Vessels.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-0c5c6b33', '2026-01-29', 'Berg Process Oxy Oman Q26.100', 'IBS/Paul→Berg/Hanas', 'Berg Process', 'BERG-OMAN', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Q26.100 VRU Mukhaizna Flare Recovery PVs.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-290357df', '2026-01-29', 'Broadwing V6C899 Q26.011 Carbon Capture Ductwork', 'IBS/Paul→VPI', 'Vogt Power International', 'V6C899-BROADWING', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Q26.011 Rev.0 sent.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-7b36849d', '2026-01-26', 'SAI Bali Project Q26.015 Exhaust line', 'IBS/Paul→SAI/Vasyl', 'SAI', 'SAI-BALI', 'QUOTATION', 'FOLLOW_UP', 'MEDIUM', 'Q26.015 Exhaust line for Bali project 25071.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-145a2a35', '2026-01-26', 'Ferryboat Q25.xxx Rev update to TBA Korea', 'IBS/Paul→TBA/Muhammad', 'TBA Korea', 'TBA-FERRYBOAT', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Rev.1 GA drawing. 14-msg thread. Boss needs more relevant design.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-5e66e162', '2026-01-19', 'Gonnix Q25.160 painting 28 bầu lọc', 'IBS/Paul→Gonnix/Nhat', 'Gonnix', 'GONNIX-PAINTING', 'QUOTATION', 'FOLLOW_UP', 'MEDIUM', 'Painting procedure sent. Thickness reduction proposal.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-4d3f93d1', '2026-01-15', 'VPI Duke Caryugar V17571 Q26.003 NPP', 'IBS/Paul→VPI/Aum', 'Vogt Power International', 'V17571-CARYUGAR', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Q26.003 Rev.0 NPP quotation.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-eb4be4de', '2026-01-14', 'SAI Bali Project Q26.015 Exhaust line', 'IBS/Paul→SAI/Vasyl', 'SAI', 'SAI-BALI', 'QUOTATION', 'FOLLOW_UP', 'MEDIUM', 'Q26.015 with drawings. 5-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-c996014e', '2026-01-14', 'VPI Wabash V28779 Stack Support Brackets', 'IBS/Paul→VPI/Pawat', 'Vogt Power International', 'V28779-WABASH', 'QUOTATION', 'FOLLOW_UP', 'MEDIUM', 'Declined? Thank for trust but...');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-c326d35b', '2026-01-12', '25146T Steel Package RFQ', 'Iman/Charlotte→IBS', 'Client (Iman)', '25146T-STEEL', 'QUOTATION', 'ACTION_IBS', 'MEDIUM', 'Steel package RFQ. 7-msg thread.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-177b05ec', '2026-01-09', 'HAJR PO 219861 Unit 1 Final Weight signed', 'IBS→Braden/Ivan', 'Braden Europe', '13105-GHAZLAN', 'CONTRACT', 'NONE', 'HIGH', 'Final weight & value returned with IBS signature.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-b5141326', '2026-01-07', 'Berg Process Algeria GHBR RFQ Desalter/PWT/GDU', 'Berg/Hanas→IBS', 'Berg Process', 'BERG-ALGERIA', 'QUOTATION', 'ACTION_IBS', 'HIGH', 'Firm bidding for Desalter/PWT/GDU Package. Algeria GHBR EPC Project.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-ed55ccf8', '2026-01-06', 'KHPT P2 Project Q25.158 Steam drum', 'IBS/Paul→KHPT/Cung', 'KHPT', 'KHPT-P2', 'QUOTATION', 'FOLLOW_UP', 'HIGH', 'Q25.158 Rev.0 Steam drum + Condenser/Converter.');
INSERT OR IGNORE INTO sale_email_full (id, email_date, subject_summary, direction, customer_name, project_code, email_type, action_required, priority, details)
  VALUES ('efull-c199c147', '2026-01-06', '71m Steel Arch Bridge Cost Estimate + Brochure', 'Nippon Koei/Akio→IBS', 'Nippon Koei', 'NIPPON-KOEI-BRIDGE', 'QUOTATION', 'ACTION_IBS', 'MEDIUM', 'Japanese consultant requesting cost estimate for 71m steel arch bridge.');

-- === FOLLOW-UP ACTIONS VIEW ===
CREATE VIEW IF NOT EXISTS v_sale_followups AS
SELECT email_date, customer_name, project_code, subject_summary, action_required, priority, details
FROM sale_email_full
WHERE action_required IN ('URGENT', 'ACTION_IBS', 'FOLLOW_UP', 'PENDING_PAYMENT', 'PENDING_APPROVAL')
ORDER BY
  CASE priority WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END,
  email_date DESC;

-- === PROJECT ACTIVITY SUMMARY VIEW ===
CREATE VIEW IF NOT EXISTS v_project_activity AS
SELECT project_code, customer_name, COUNT(*) as email_count,
  MIN(email_date) as first_activity, MAX(email_date) as last_activity,
  GROUP_CONCAT(DISTINCT email_type) as activity_types,
  SUM(CASE WHEN action_required != 'NONE' THEN 1 ELSE 0 END) as pending_actions
FROM sale_email_full
GROUP BY project_code, customer_name
ORDER BY last_activity DESC;