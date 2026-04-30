-- ═══════════════════════════════════════════════════════════
-- 24_client_database.sql
-- Source: Client_Data_Base Google Sheet (ibshi@ibs.com.vn)
-- Generated: 2026-04-29 13:14:50
-- 172 customers (156 overseas + 16 domestic) + contacts
-- ═══════════════════════════════════════════════════════════

-- === PART A: Customer Master — INSERT new + UPDATE existing ===
-- Uses INSERT OR IGNORE for new customers, then UPDATE for enrichment

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-f14374c2', 'Briese Schiffahrts GmbH & Co.KG', 'Germany', 'Europe', 'http://briese.de/', 'CDB Classification: Good | Scope: Supply of Tweendeck | Quotes: 1 | Won: 1 | Total Quoted: $1,519,929 | Revenue: $1,519,929', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'http://briese.de/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Supply of Tweendeck | Quotes: 1 | Won: 1 | Total Quoted: $1,519,929 | Revenue: $1,519,929' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Supply of Tweendeck | Quotes: 1 | Won: 1 | Total Quoted: $1,519,929 | Revenue: $1,519,929' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-f14374c2';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-b42568cd', 'cdb-f14374c2', 'Mr. Bernd Hartmann', 'info@briese.de', '+49 491 92520-345', 'Fleet manager & CEO', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-29661b90', 'cdb-f14374c2', 'Mr. Wilke Briese', 'fleetmanagement@briese.de', '+49 491 92520-345', 'Fleet manager & CEO', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-12f902b9', 'Buttner Energie', 'Germany', 'Europe', 'https://www.buettner-energy-dryer.com', 'CDB Classification: Follow up | Scope: Steel structure outlet box, hot gas duct | Quotes: 1 | Total Quoted: $116,377', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.buettner-energy-dryer.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure outlet box, hot gas duct | Quotes: 1 | Total Quoted: $116,377' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure outlet box, hot gas duct | Quotes: 1 | Total Quoted: $116,377' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-12f902b9';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-9fba6fb4', 'cdb-12f902b9', 'Thomas Grafen', 't.grafen@buettner-energy-dryer.com', '+49 - 172 - 236 1790', 'Purchasing Dpt', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-5a17fb21', 'Daiichi Jitsugyo Co.,Ltd.', 'Japan', 'Japan', 'https://www.djk.co.jp/en/', 'CDB Classification: Bad | Scope: Reclaimer | Quotes: 1 | Total Quoted: $703,988', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Japan'), website = COALESCE(NULLIF(website, ''), 'https://www.djk.co.jp/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Reclaimer | Quotes: 1 | Total Quoted: $703,988' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Reclaimer | Quotes: 1 | Total Quoted: $703,988' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-5a17fb21';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-0a51bf89', 'cdb-5a17fb21', 'Konishi', 'kenji.konishi@djk.co.jp', '+81-80-9020-4470', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-2b464db2', 'Danieli Co., Ltd. Thailand', 'Thailand', 'Asia & Other', 'https://www.eabc-thailand.org/member/199/', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $7,871', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Thailand'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.eabc-thailand.org/member/199/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $7,871' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $7,871' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-2b464db2';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-4da17ba9', 'cdb-2b464db2', 'Prajak Lamjuan', 'p.lamjuan@thailand.danieli.com', '+66 38 929 000', 'Procurement Department', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-a02ea110', 'Doosan Heavy Industries Co.,Ltd', 'Korea', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: Gas ducting and Air duct | Quotes: 7 | Total Quoted: $3,682,294', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Gas ducting and Air duct | Quotes: 7 | Total Quoted: $3,682,294' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Gas ducting and Air duct | Quotes: 7 | Total Quoted: $3,682,294' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-a02ea110';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6d5063de', 'cdb-a02ea110', 'Hunwoo. Lim / Manager', 'jaejun.kim@doosan.com', '', '', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-b308edeb', 'cdb-a02ea110', 'EPC BG)  EPC Overseas Sub-Contracting Team', 'dongyeol.park@doosan.com', '', '', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-695a6f3d', 'Duro Felguera.', 'Spain', 'Europe', 'https://www.durofelguera.com/', 'CDB Classification: Follow up | Scope: Shiploader and Stacker | Quotes: 4 | Total Quoted: $13,231,126', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Spain'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.durofelguera.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Shiploader and Stacker | Quotes: 4 | Total Quoted: $13,231,126' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Shiploader and Stacker | Quotes: 4 | Total Quoted: $13,231,126' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-695a6f3d';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-a7df9e3d', 'cdb-695a6f3d', 'Mr. Fernandez', 'eloycesar.fernandez@durofelguera.com', '', 'Procurement Department', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-e0087f87', 'Dyna - Mac', 'Singapore', 'Asia & Other', 'https://www.dyna-mac.com/', 'CDB Classification: Bad | Scope: Steel structure and pipe rack | Quotes: 2 | Total Quoted: $18,388,721 | Remark: Mr. Andrew contact', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Singapore'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.dyna-mac.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Steel structure and pipe rack | Quotes: 2 | Total Quoted: $18,388,721 | Remark: Mr. Andrew contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Steel structure and pipe rack | Quotes: 2 | Total Quoted: $18,388,721 | Remark: Mr. Andrew contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-e0087f87';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f41e96a8', 'cdb-e0087f87', 'Maria J Cagas', 'mariajanadel.cagas@dyna-mac.com', '+65 6415 0880', 'Subcontracts Department', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-c6b3a4a9', 'Energyen Corporation', 'Korea', 'Asia & Other', 'https://energyen.co.kr/en/main/', 'CDB Classification: Follow up | Scope: Structure and Steam duct | Quotes: 2 | Total Quoted: $3,114,949 | Remark: MR. Lee left the company', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://energyen.co.kr/en/main/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Structure and Steam duct | Quotes: 2 | Total Quoted: $3,114,949 | Remark: MR. Lee left the company' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Structure and Steam duct | Quotes: 2 | Total Quoted: $3,114,949 | Remark: MR. Lee left the company' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-c6b3a4a9';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-191d86d8', 'cdb-c6b3a4a9', 'S.Y. Lee', 'sylee@energyen.co.kr', '+82-10-6222-1025', 'Principal Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-3ffa2e19', 'Entec Solution', 'Canada', 'Americas', 'https://entecsoln.com/', 'CDB Classification: Bad | Scope: Diffuser | Quotes: 1 | Total Quoted: $291,702', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Canada'), region = COALESCE(NULLIF(region, ''), 'Americas'), website = COALESCE(NULLIF(website, ''), 'https://entecsoln.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Diffuser | Quotes: 1 | Total Quoted: $291,702' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Diffuser | Quotes: 1 | Total Quoted: $291,702' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-3ffa2e19';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6aaefb01', 'cdb-3ffa2e19', 'Iulian Ostache, P.Eng', 'iostache@entecsoln.com', '', 'Senior Project Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-c14e773a', 'Evapco-Blct Dry Cooling, Inc.', 'USA', 'Americas', 'https://www.evapcodc.com/', 'CDB Classification: Follow up | Scope: Steel structure and duct | Quotes: 2 | Total Quoted: $6,687,720', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'USA'), region = COALESCE(NULLIF(region, ''), 'Americas'), website = COALESCE(NULLIF(website, ''), 'https://www.evapcodc.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure and duct | Quotes: 2 | Total Quoted: $6,687,720' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure and duct | Quotes: 2 | Total Quoted: $6,687,720' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-c14e773a';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-2a4d552d', 'cdb-c14e773a', 'Kyu-Jung Choi', 'kchoi@evapcodc.com', '+84 903002230', 'Regional Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-8806267b', 'Finnsea', 'Vietnam', 'Asia & Other', '', 'CDB Classification: Bad | Scope: Chain conveyor, Silos | Quotes: 3 | Total Quoted: $1,590,321', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Chain conveyor, Silos | Quotes: 3 | Total Quoted: $1,590,321' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Chain conveyor, Silos | Quotes: 3 | Total Quoted: $1,590,321' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-8806267b';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-ffabde2c', 'cdb-8806267b', 'Tribhuan Verma', 'tribhuan.verma@finnsea.com', '+84901152100', 'Senior Consultant', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-fc27443a', 'Flowserve', 'Germany', 'Europe', 'https://www.flowserve.com/en/', 'CDB Classification: Bad | Scope: Pressure vessel | Quotes: 1 | Total Quoted: $4,406', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.flowserve.com/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Pressure vessel | Quotes: 1 | Total Quoted: $4,406' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Pressure vessel | Quotes: 1 | Total Quoted: $4,406' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-fc27443a';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-c55c12bf', 'Hitachi, Ltd.', 'Japan', 'Japan', 'https://www.hitachi.com/', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $29,901', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Japan'), website = COALESCE(NULLIF(website, ''), 'https://www.hitachi.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $29,901' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $29,901' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-c55c12bf';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-05f96545', 'cdb-c55c12bf', 'Go Ota', 'go.ota.ku@hitachi.com', '+81-70-2266-4816', 'Senior Manager
Global Supply Chain
Management Department', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-b1ae69c6', 'IHI INFRASTRUCTURE ASIA', 'Japan', 'Japan', 'https://www.ihi.co.jp/en/', 'CDB Classification: Follow up | Scope: Steel structure for Bridge | Quotes: 3 | Total Quoted: $3,675,512', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Japan'), website = COALESCE(NULLIF(website, ''), 'https://www.ihi.co.jp/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure for Bridge | Quotes: 3 | Total Quoted: $3,675,512' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure for Bridge | Quotes: 3 | Total Quoted: $3,675,512' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-b1ae69c6';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-9890360e', 'cdb-b1ae69c6', 'Phuong Dinh Thang', 'thang9584@ihi-g.com', '(+84) 91 285 3859', 'DPT Factory Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-dddc99a4', 'InvestNet Group Pty Ltd', 'Australia', 'Americas', '', 'CDB Classification: Bad | Scope: Steel structure | Quotes: 4 | Total Quoted: $18,192,507', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Australia'), region = COALESCE(NULLIF(region, ''), 'Americas'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Steel structure | Quotes: 4 | Total Quoted: $18,192,507' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Steel structure | Quotes: 4 | Total Quoted: $18,192,507' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-dddc99a4';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-bba83b32', 'cdb-dddc99a4', 'Neno Kević', 'neno@investnet.group', '+61 400 738 384', 'Founder & CEO', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-f98f4e7d', 'ITW Performance Polymers (Densit)', 'Denmark', 'Europe', 'https://itwperformancepolymers.com/', 'CDB Classification: Bad | Scope: Pipe | Quotes: 4 | Total Quoted: $1,027,842', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Denmark'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://itwperformancepolymers.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Pipe | Quotes: 4 | Total Quoted: $1,027,842' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Pipe | Quotes: 4 | Total Quoted: $1,027,842' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-f98f4e7d';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-2ad9a185', 'cdb-f98f4e7d', 'Henrik Gadegaard', 'hgadegaard@itwpp.com', '+45 5127 5134', 'Technical Support, Wear & Abrasion', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-beff5ee1', 'JFE Engineering India Pvt. Ltd.', 'India', 'Asia & Other', 'https://www.jfe-eng.co.jp/en/', 'CDB Classification: Bad | Scope: Steel structure | Quotes: 10 | Total Quoted: $7,115,087', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'India'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.jfe-eng.co.jp/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Steel structure | Quotes: 10 | Total Quoted: $7,115,087' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Steel structure | Quotes: 10 | Total Quoted: $7,115,087' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-beff5ee1';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-17b2a951', 'cdb-beff5ee1', 'Mr An', 'anand-marwadi@jfe-eng.co.in', '+91-78-7577-1150
+91-78-7577-5678', 'Senior Manager – Procurement
DGM Projects & Quality', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-b3c9dc81', 'cdb-beff5ee1', 'Marwadi', 'sivakumar-v@jfe-eng.co.in', '+91-78-7577-1150
+91-78-7577-5678', 'Senior Manager – Procurement
DGM Projects & Quality', 0);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-a40db90f', 'cdb-beff5ee1', 'Mr Sivakumar Veleyutham', 'anand-marwadi@jfe-eng.co.in', '+91-78-7577-1150
+91-78-7577-5678', 'Senior Manager – Procurement
DGM Projects & Quality', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-46241fe2', 'JFE Engineering Japan', 'Japan', 'Japan', 'https://www.jfe-eng.co.jp/en/', 'CDB Classification: Good | Scope: Steel structure | Quotes: 37 | Won: 8 | Total Quoted: $85,823,439 | Revenue: $5,513,510', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Japan'), website = COALESCE(NULLIF(website, ''), 'https://www.jfe-eng.co.jp/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Steel structure | Quotes: 37 | Won: 8 | Total Quoted: $85,823,439 | Revenue: $5,513,510' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Steel structure | Quotes: 37 | Won: 8 | Total Quoted: $85,823,439 | Revenue: $5,513,510' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-46241fe2';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f84bbe11', 'cdb-46241fe2', 'Takahashi', 'takahashi-f-jun@jfe-eng.co.jp', '+81-45-505-8983', 'Project Procurement Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-077d30c4', 'John Cockerill Energy (CMI)', 'Belgum', 'Europe', 'https://johncockerill.com/en/', 'CDB Classification: Good | Scope: HRSG system | Quotes: 5 | Total Quoted: $39,056,089', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Belgum'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://johncockerill.com/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: HRSG system | Quotes: 5 | Total Quoted: $39,056,089' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: HRSG system | Quotes: 5 | Total Quoted: $39,056,089' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-077d30c4';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-27836d2b', 'cdb-077d30c4', 'GRINI Habib', 'habib.grini@johncockerill.com', '+ 32 (0) 4 330 21 63
 +32 (0) 475 30 21 63', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-428648f9', 'Kirchner', 'Italy', 'Europe', 'http://www.kirchner.it/', 'CDB Classification: Follow up | Scope: Tube | Quotes: 1 | Total Quoted: $87,741', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Italy'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'http://www.kirchner.it/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Tube | Quotes: 1 | Total Quoted: $87,741' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Tube | Quotes: 1 | Total Quoted: $87,741' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-428648f9';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-bccd79e0', 'cdb-428648f9', 'Davide Dossena', 'davide.dossena@kirchner.it', '+39 02 67072002', 'Purchasing  Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-e6507ce3', 'Macgregor Norway As.', 'Finland', 'Europe', 'https://www.macgregor.com/', 'CDB Classification: Good | Scope: Gearbox housing | Quotes: 4 | Won: 2 | Total Quoted: $1,174,249 | Revenue: $995,202', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Finland'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.macgregor.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Gearbox housing | Quotes: 4 | Won: 2 | Total Quoted: $1,174,249 | Revenue: $995,202' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Gearbox housing | Quotes: 4 | Won: 2 | Total Quoted: $1,174,249 | Revenue: $995,202' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-e6507ce3';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-c5757e22', 'cdb-e6507ce3', 'Jan Erik Marvold', 'jan.erik.marvold@macgregor.com', '+4797013950', 'Manufacturing Engineering Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-93a0e996', 'Mcconnell Dowell', 'Singapore', 'Asia & Other', 'https://www.mcconnelldowell.com/where-we-work/south-east-asia/singapore', 'CDB Classification: Bad | Scope: Jacket module | Quotes: 1 | Total Quoted: $14,040,438 | Remark: Mr. Andrew contact', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Singapore'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.mcconnelldowell.com/where-we-work/south-east-asia/singapore'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Jacket module | Quotes: 1 | Total Quoted: $14,040,438 | Remark: Mr. Andrew contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Jacket module | Quotes: 1 | Total Quoted: $14,040,438 | Remark: Mr. Andrew contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-93a0e996';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-f046b60d', 'MCI', 'Korea', 'Asia & Other', '', 'CDB Classification: Bad | Scope: Steel structure | Quotes: 2 | Total Quoted: $14,933,954 | Remark: Mr. Andrew contact', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Steel structure | Quotes: 2 | Total Quoted: $14,933,954 | Remark: Mr. Andrew contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Steel structure | Quotes: 2 | Total Quoted: $14,933,954 | Remark: Mr. Andrew contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-f046b60d';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-584fd942', 'cdb-f046b60d', 'Kim, Gihong', 'kim.g.hong.vn@bestmci.co.kr', '(+84) 094 454 7166', 'Representative', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-b01a50b1', 'Milaha Offsore Services', 'Singapore', 'Asia & Other', '', 'CDB Classification: Bad | Scope: Shipbuilding | Quotes: 1 | Total Quoted: $1,500,000 | Remark: Mr. Andrew contact', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Singapore'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Shipbuilding | Quotes: 1 | Total Quoted: $1,500,000 | Remark: Mr. Andrew contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Shipbuilding | Quotes: 1 | Total Quoted: $1,500,000 | Remark: Mr. Andrew contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-b01a50b1';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-c40da0fc', 'Mitsubishi Power', 'Japan', 'Japan', 'https://power.mhi.com/about/outline', 'CDB Classification: Follow up | Scope: Gas Turbin Enclosure | Quotes: 5 | Total Quoted: $3,348,719', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Japan'), website = COALESCE(NULLIF(website, ''), 'https://power.mhi.com/about/outline'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Gas Turbin Enclosure | Quotes: 5 | Total Quoted: $3,348,719' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Gas Turbin Enclosure | Quotes: 5 | Total Quoted: $3,348,719' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-c40da0fc';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-14edc7c8', 'cdb-c40da0fc', 'Mr. Tatsuya Matsunaga', 'tatsuya.matsunaga.rx@mhi.com', '', 'Quản lý dự án', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-1c0042c8', 'Nippon Steel Engineering Co., Ltd', 'Japan', 'Japan', 'https://www.eng.nipponsteel.com/english/', 'CDB Classification: Follow up | Scope: Sheet pile | Quotes: 1 | Total Quoted: $432,976', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Japan'), website = COALESCE(NULLIF(website, ''), 'https://www.eng.nipponsteel.com/english/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Sheet pile | Quotes: 1 | Total Quoted: $432,976' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Sheet pile | Quotes: 1 | Total Quoted: $432,976' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-1c0042c8';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-935b8fec', 'cdb-1c0042c8', 'Mr. Seiki Sakaue', 'sakaue.seiki@nsc-eng.co.jp', '', 'Quản lý dự án', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-97a049fb', 'Nooter Eriksen', 'USA', 'Americas', 'https://cicgroup.com/nooter-eriksen/', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 3 | Total Quoted: $4,672,138', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'USA'), region = COALESCE(NULLIF(region, ''), 'Americas'), website = COALESCE(NULLIF(website, ''), 'https://cicgroup.com/nooter-eriksen/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 3 | Total Quoted: $4,672,138' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 3 | Total Quoted: $4,672,138' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-97a049fb';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-dc2a2bf6', 'cdb-97a049fb', 'Greg Kerwin', 'gtkerwin@ne.com', '+1-314-920-8605', 'Manager of Manufacturing & Sourcing
Global sourcing manager ( Brian)', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-b52fa1dd', 'cdb-97a049fb', 'Brian Sicking', 'bsicking@ne.com', '+1-314-920-8605', 'Manager of Manufacturing & Sourcing
Global sourcing manager ( Brian)', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-0b29992d', 'PHB', 'Spain', 'Europe', 'https://www.grupotsk.com/en/business-lines/handling-mineria/', 'CDB Classification: Good | Scope: Steel structure, Ship loader, Ship Unloader | Quotes: 16 | Won: 6 | Total Quoted: $19,885,075 | Revenue: $1,636,311', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Spain'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.grupotsk.com/en/business-lines/handling-mineria/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Steel structure, Ship loader, Ship Unloader | Quotes: 16 | Won: 6 | Total Quoted: $19,885,075 | Revenue: $1,636,311' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Steel structure, Ship loader, Ship Unloader | Quotes: 16 | Won: 6 | Total Quoted: $19,885,075 | Revenue: $1,636,311' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-0b29992d';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-39960d48', 'cdb-0b29992d', 'Antonio Miaja', 'antonio.miaja@pwh.es', '+34 984 495 500', 'Procurement Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-e4a9b48c', 'Posco E&C', 'Korea', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 3 | Total Quoted: $41,211,473', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 3 | Total Quoted: $41,211,473' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 3 | Total Quoted: $41,211,473' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-e4a9b48c';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6e6882b2', 'cdb-e4a9b48c', 'C.S.Park', 'cespark@poscoenc.com', '82 10 4855 3826', 'Equipment Procurement Group', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-7809efbd', 'Quin Right Enterprises Pte Ltd', 'Singapore', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: Tank head | Quotes: 4 | Won: 1 | Total Quoted: $274,784 | Revenue: $7,000 | Remark: Mr. Andrew contact', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Singapore'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Tank head | Quotes: 4 | Won: 1 | Total Quoted: $274,784 | Revenue: $7,000 | Remark: Mr. Andrew contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Tank head | Quotes: 4 | Won: 1 | Total Quoted: $274,784 | Revenue: $7,000 | Remark: Mr. Andrew contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-7809efbd';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-ce089c73', 'cdb-7809efbd', 'Loh Kah Lam', 'lohkl@quinrite.com', '6842 3345', '', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-3e782812', 'cdb-7809efbd', 'Tang Wei Leong', 'quinrite@singnet.com.sg', '6842 3345', '', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-ea5ae42f', 'Saskarc', 'Canada', 'Americas', 'https://saskarc.com/', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $8,414,329', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Canada'), region = COALESCE(NULLIF(region, ''), 'Americas'), website = COALESCE(NULLIF(website, ''), 'https://saskarc.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $8,414,329' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $8,414,329' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-ea5ae42f';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-31255c49', 'cdb-ea5ae42f', 'Roy Drever', 'roy.drever@saskarc.com', '(306) 483-5055 x 106', 'General Manager
 & Sales manager', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-8d206e7f', 'cdb-ea5ae42f', 'Tim Cooley', 'roy.drever@saskarc.com', '(306) 483-5055 x 106', 'General Manager
 & Sales manager', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-f03187f5', 'Siemens Gamesa Renewable Energy A/S', 'Germany', 'Europe', 'www.siemens-energy.com', 'CDB Classification: Good | Scope: Bypass system | Quotes: 5 | Total Quoted: $8,569,982', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'www.siemens-energy.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Bypass system | Quotes: 5 | Total Quoted: $8,569,982' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Bypass system | Quotes: 5 | Total Quoted: $8,569,982' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-f03187f5';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-bfb6ddf6', 'cdb-f03187f5', 'Ron van Uden', '', '+49 172 4074842', 'SGRE OF P CM NH', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-89762116', 'Siemens Gamesa Renewable Energy A/S (China)', 'China', 'Asia & Other', 'https://www.siemensgamesa.com/en-int', 'CDB Classification: Follow up | Scope: Steel structure for wind power | Quotes: 1 | Total Quoted: $680,075', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'China'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.siemensgamesa.com/en-int'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure for wind power | Quotes: 1 | Total Quoted: $680,075' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure for wind power | Quotes: 1 | Total Quoted: $680,075' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-89762116';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-1bc3cf9d', 'cdb-89762116', 'Lin Yu', 'Yu.Lin@siemensgamesa.com', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-3485e685', 'Siemen Germany', 'Germany', 'Europe', 'www.siemensgamesa.com', 'CDB Classification: Follow up | Scope: Steel structure for wind power | Quotes: 1 | Total Quoted: $5,123,255', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'www.siemensgamesa.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure for wind power | Quotes: 1 | Total Quoted: $5,123,255' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure for wind power | Quotes: 1 | Total Quoted: $5,123,255' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-3485e685';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-df50fb77', 'cdb-3485e685', 'Sergio Benítez Méndez', 'selvin.alvarez@siemensgamesa.com', '', 'Procurement Department', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-20d4c72f', 'SPG Hydrocarbon Pte. Ltd.', 'Singapore', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: Gound Flare | Quotes: 7 | Total Quoted: $7,378,539', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Singapore'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Gound Flare | Quotes: 7 | Total Quoted: $7,378,539' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Gound Flare | Quotes: 7 | Total Quoted: $7,378,539' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-20d4c72f';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-a843df14', 'cdb-20d4c72f', 'Ruediger Kunzfeld', 'Ruediger.Kunzfeld@spg-steiner.com', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-bf58d0c8', 'Stejasa', 'Spain', 'Europe', 'http://www.stejasa.es/', 'CDB Classification: Good | Scope: Bypass system | Quotes: 67 | Won: 41 | Total Quoted: $10,803,433 | Revenue: $3,970,276 | Remark: Mr. Ivan left staejasa, joined to Braden', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Spain'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'http://www.stejasa.es/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Bypass system | Quotes: 67 | Won: 41 | Total Quoted: $10,803,433 | Revenue: $3,970,276 | Remark: Mr. Ivan left staejasa, joined to Braden' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Bypass system | Quotes: 67 | Won: 41 | Total Quoted: $10,803,433 | Revenue: $3,970,276 | Remark: Mr. Ivan left staejasa, joined to Braden' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-bf58d0c8';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6cef9be7', 'cdb-bf58d0c8', 'Ivan Martinez', 'ivan.martinez@aafintl.com', '+34 666 508 538', 'Group Manufacturing Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-8fe47842', 'Taim Weser', 'Spain', 'Europe', 'https://www.taimweser.com/', 'CDB Classification: Follow up | Scope: Shiploader and Stacker | Quotes: 3 | Total Quoted: $6,681,784', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Spain'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.taimweser.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Shiploader and Stacker | Quotes: 3 | Total Quoted: $6,681,784' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Shiploader and Stacker | Quotes: 3 | Total Quoted: $6,681,784' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-8fe47842';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-b9b6c5ac', 'cdb-8fe47842', 'Raul Ruiz', 'rruiz@taimweser.com', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-6feb779d', 'Tenova Gmbh', 'Germany', 'Europe', 'https://tenova.com/', 'CDB Classification: Bad | Scope: steel structure | Quotes: 2 | Total Quoted: $9,800,088', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://tenova.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: steel structure | Quotes: 2 | Total Quoted: $9,800,088' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: steel structure | Quotes: 2 | Total Quoted: $9,800,088' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-6feb779d';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-baf33b1f', 'Tenova S.P.A (Italy).', 'Italy', 'Europe', '', 'CDB Classification: Bad | Scope: Steel structure, Ship Unloader | Quotes: 5 | Total Quoted: $5,020,227', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Italy'), region = COALESCE(NULLIF(region, ''), 'Europe'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Steel structure, Ship Unloader | Quotes: 5 | Total Quoted: $5,020,227' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Steel structure, Ship Unloader | Quotes: 5 | Total Quoted: $5,020,227' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-baf33b1f';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-c83dcbf9', 'cdb-baf33b1f', 'Corrado Leoni', 'corrado.leoni@tenova.com', '+39-010-6054.710', 'Estimates Specialist', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-37d7f541', 'Tenova Takraf (Usa)', 'USA', 'Americas', '', 'CDB Classification: Follow up | Scope: Steel structure for Conveyer | Quotes: 5 | Total Quoted: $22,729,774', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'USA'), region = COALESCE(NULLIF(region, ''), 'Americas'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure for Conveyer | Quotes: 5 | Total Quoted: $22,729,774' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure for Conveyer | Quotes: 5 | Total Quoted: $22,729,774' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-37d7f541';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-ac97f94b', 'cdb-37d7f541', 'Vinicius Fernandes', 'vinicius.fernandes@takraf.com', '+1 (303) 770-6307', 'Procurement Manager', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-2ea1cd29', 'cdb-37d7f541', 'Clancy', 'clancy.hoag@takraf.com', '+1 (303) 770-6307', 'Procurement Manager', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-0eacf8d5', 'Tokyo Kizai Kogyo', 'Japan', 'Japan', '', 'CDB Classification: Bad | Scope: Steel structutre and piping | Quotes: 1 | Total Quoted: $32,999', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Japan'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Steel structutre and piping | Quotes: 1 | Total Quoted: $32,999' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Steel structutre and piping | Quotes: 1 | Total Quoted: $32,999' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-0eacf8d5';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-a9d5c7f2', 'cdb-0eacf8d5', 'Le Long', 'lelong@t-kizai.co.jp', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-77a7ab4a', 'Woahoo Energy', 'USA', 'Americas', '', 'CDB Classification: Follow up | Scope: Boom for crane | Quotes: 2 | Won: 1 | Total Quoted: $189,708 | Revenue: $4,300', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'USA'), region = COALESCE(NULLIF(region, ''), 'Americas'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Boom for crane | Quotes: 2 | Won: 1 | Total Quoted: $189,708 | Revenue: $4,300' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Boom for crane | Quotes: 2 | Won: 1 | Total Quoted: $189,708 | Revenue: $4,300' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-77a7ab4a';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-40802e39', 'cdb-77a7ab4a', 'Maria Almeda', 'mja@wahooenergy.com', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-9bb16045', 'Yokogawa Bridge Corp.', 'Japan', 'Japan', 'http://www.en.yokogawa-bridge.co.jp/', 'CDB Classification: Good | Scope: Bridge | Quotes: 32 | Won: 12 | Total Quoted: $44,641,353 | Revenue: $2,207,153', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Japan'), website = COALESCE(NULLIF(website, ''), 'http://www.en.yokogawa-bridge.co.jp/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Bridge | Quotes: 32 | Won: 12 | Total Quoted: $44,641,353 | Revenue: $2,207,153' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Bridge | Quotes: 32 | Won: 12 | Total Quoted: $44,641,353 | Revenue: $2,207,153' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-9bb16045';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-951e97e3', 'cdb-9bb16045', 'HAYAHITO ITO', 'ha.itoh@yokogawa-bridge.co.jp', ':+81-70-2469-4021', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-6ea73eab', 'Yoong Jin (Công ty TNHH Xây Dựng và Thương mại)', 'Korea', 'Asia & Other', '', 'CDB Classification: Bad | Scope: Steel structure | Quotes: 2 | Total Quoted: $6,930,686', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Steel structure | Quotes: 2 | Total Quoted: $6,930,686' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Steel structure | Quotes: 2 | Total Quoted: $6,930,686' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-6ea73eab';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-445d337b', 'Canada', 'Canada', 'Americas', '', 'CDB Classification: Follow up | Scope: Driven Pile, tube | Quotes: 2 | Total Quoted: $3,085,200 | Remark: Mr. Thac contact', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Canada'), region = COALESCE(NULLIF(region, ''), 'Americas'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Driven Pile, tube | Quotes: 2 | Total Quoted: $3,085,200 | Remark: Mr. Thac contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Driven Pile, tube | Quotes: 2 | Total Quoted: $3,085,200 | Remark: Mr. Thac contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-445d337b';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-542d57ef', 'VERBIO Vereinigte Bio Energie AG', 'Germany', 'Europe', 'https://www.verbio.us/project/verbio-nevada-biorefinery/', 'CDB Classification: Good | Scope: Heat exchanger, tank | Quotes: 26 | Won: 8 | Total Quoted: $7,580,188 | Revenue: $1,065,787', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.verbio.us/project/verbio-nevada-biorefinery/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Heat exchanger, tank | Quotes: 26 | Won: 8 | Total Quoted: $7,580,188 | Revenue: $1,065,787' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Heat exchanger, tank | Quotes: 26 | Won: 8 | Total Quoted: $7,580,188 | Revenue: $1,065,787' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-542d57ef';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-ca7b4c08', 'cdb-542d57ef', 'Michael Rau', 'michael.rau@verbio.de', '+49 174 7214 232', 'Project Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-609fd322', 'REEL Möller GmbH', 'Germany', 'Europe', 'https://www.reelinternational.com/', 'CDB Classification: Follow up | Scope: Steel structure and tank | Quotes: 2 | Total Quoted: $2,246,922', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.reelinternational.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure and tank | Quotes: 2 | Total Quoted: $2,246,922' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure and tank | Quotes: 2 | Total Quoted: $2,246,922' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-609fd322';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-3a12c5ef', 'cdb-609fd322', 'Frank PAETZEL', 'frank.paetzel@reel-moeller.com', '+49 172 7778 367', 'Head of Supply Chain Management', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-3370f8d0', 'FAM Materials Handling Systems India Pvt. Ltd.', 'India', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: Ship unloader and Stacker | Quotes: 3 | Total Quoted: $13,576,635', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'India'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Ship unloader and Stacker | Quotes: 3 | Total Quoted: $13,576,635' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Ship unloader and Stacker | Quotes: 3 | Total Quoted: $13,576,635' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-3370f8d0';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-0098b399', 'cdb-3370f8d0', 'Sumit Datta', 'sumit.datta@fam-india.com', '+91 9831687799', 'FAM Materials Handling Systems India Pvt. Ltd.', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-9048b023', 'BOLDROCCHI', 'Italy', 'Europe', 'https://www.boldrocchigroup.com/', 'CDB Classification: Follow up | Scope: Bypass system | Quotes: 5 | Total Quoted: $3,086,969', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Italy'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.boldrocchigroup.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Bypass system | Quotes: 5 | Total Quoted: $3,086,969' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Bypass system | Quotes: 5 | Total Quoted: $3,086,969' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-9048b023';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f4234d73', 'cdb-9048b023', 'Giovanni Barbieri', 'barbieri@boldrocchi.eu', '+390392202702', 'BU Director | Gas Turbine System & Noise Protection Division', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-34bca630', 'GE Hydro China', 'China', 'Asia & Other', 'https://www.ge.com/', 'CDB Classification: Follow up | Scope: Stay ring, support cone, stator frame | Quotes: 1 | Total Quoted: $5,313,583', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'China'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.ge.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Stay ring, support cone, stator frame | Quotes: 1 | Total Quoted: $5,313,583' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Stay ring, support cone, stator frame | Quotes: 1 | Total Quoted: $5,313,583' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-34bca630';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-2faab79f', 'cdb-34bca630', 'WANG Juan', 'juan.wang1@ge.com', '86 -13512981597', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-e84077c0', 'MCNALLY BHARAT', 'India', 'Asia & Other', 'https://www.mcnallybharat.com/', 'CDB Classification: Bad | Scope: Steel structure | Quotes: 1', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'India'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.mcnallybharat.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Steel structure | Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Steel structure | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-e84077c0';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-d96788f2', 'cdb-e84077c0', 'RAJIB MAJUMDER', 'rajib.majumder@mbecl.co.in', '', 'Manufacturing Quality Plan', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-2358a580', 'Jord Power Systems GmbH*', 'Singapore', 'Asia & Other', 'https://www.jord.com.au/industries/power/', 'CDB Classification: Bad | Scope: Steel structure | Quotes: 1 | Total Quoted: $1,001,087', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Singapore'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.jord.com.au/industries/power/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Steel structure | Quotes: 1 | Total Quoted: $1,001,087' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Steel structure | Quotes: 1 | Total Quoted: $1,001,087' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-2358a580';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-3099cdf6', 'cdb-2358a580', '''Arjun Doorvasula', 'DMallikarjun@jord.com.au', '+65 98 34 21 68', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-c9456437', 'SCHADE Lagertechnik GmbH', 'Germany', 'Europe', 'https://aumund.com/en/aumund-group/schade-lagertechnik-gmbh/', 'CDB Classification: Follow up | Scope: Stacker, Reclaimer | Quotes: 3 | Total Quoted: $4,189,509', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://aumund.com/en/aumund-group/schade-lagertechnik-gmbh/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Stacker, Reclaimer | Quotes: 3 | Total Quoted: $4,189,509' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Stacker, Reclaimer | Quotes: 3 | Total Quoted: $4,189,509' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-c9456437';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-8d3c92b3', 'cdb-c9456437', 'Vitali Stuckert', 'stuckert@AUMUND.de', '+49 209 503 16 480', 'Head of Purchasing', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-eab48745', 'GUGLER Water Turbines GmbH', 'Austria', 'Europe', 'https://www.gugler.com/', 'CDB Classification: Follow up | Scope: Spiral case, draft tube, discharge ring | Quotes: 4 | Total Quoted: $163,637', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Austria'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.gugler.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Spiral case, draft tube, discharge ring | Quotes: 4 | Total Quoted: $163,637' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Spiral case, draft tube, discharge ring | Quotes: 4 | Total Quoted: $163,637' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-eab48745';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-27100005', 'cdb-eab48745', 'Ing. Thomas NEUMÜLLER BSc MSc', 'T.Neumueller@gugler.com', '+43 676 351 93 56', 'Purchasing Department', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-4bd9c979', 'Global Hydro Energy GmbH', 'Austria', 'Europe', 'https://www.global-hydro.eu/en', 'CDB Classification: Follow up | Scope: Spiral case, draft tube, discharge ring | Quotes: 5 | Total Quoted: $1,485,131', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Austria'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.global-hydro.eu/en'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Spiral case, draft tube, discharge ring | Quotes: 5 | Total Quoted: $1,485,131' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Spiral case, draft tube, discharge ring | Quotes: 5 | Total Quoted: $1,485,131' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-4bd9c979';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-0f0e6065', 'cdb-4bd9c979', 'Martin Pernsteiner', 'martin.pernsteiner@global-hydro.eu', '+43 7285 - 514 - 0052', 'Procurement Engineer', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-af6960c2', 'Neilsoft Ltd.', 'USA', 'Americas', 'https://neilsoft.com/', 'CDB Classification: Good | Scope: Tank | Quotes: 4 | Total Quoted: $2,062,319 | Remark: Belongs to Verbio', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'USA'), region = COALESCE(NULLIF(region, ''), 'Americas'), website = COALESCE(NULLIF(website, ''), 'https://neilsoft.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Tank | Quotes: 4 | Total Quoted: $2,062,319 | Remark: Belongs to Verbio' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Tank | Quotes: 4 | Total Quoted: $2,062,319 | Remark: Belongs to Verbio' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-af6960c2';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-39d908ff', 'cdb-af6960c2', 'Tushar Gaikwad', 'nbrprocurement@neilsoft.com', '+1 (920) 659-6222', 'NBR PROCUREMENT TEAM.', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-5eb7119f', 'BFL Hydro', 'India', 'Asia & Other', 'https://www.bflhydro.com/', 'CDB Classification: Good | Scope: Spiral case, draft tube, discharge ring | Quotes: 7 | Won: 1 | Total Quoted: $534,680 | Revenue: $35,436', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'India'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.bflhydro.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Spiral case, draft tube, discharge ring | Quotes: 7 | Won: 1 | Total Quoted: $534,680 | Revenue: $35,436' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Spiral case, draft tube, discharge ring | Quotes: 7 | Won: 1 | Total Quoted: $534,680 | Revenue: $35,436' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-5eb7119f';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6a7b3dc0', 'cdb-5eb7119f', 'Narasimhaiah. M', 'narasimhaiah.m@bflhydro.com', '+919036043504', 'Engineer - Procurement', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-70dd1137', 'Hirose Vietnam Co.,Ltd', 'Japan', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: Kingpost | Quotes: 1', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Kingpost | Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Kingpost | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-70dd1137';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-143b8848', 'BakerHughes', 'Italy', 'Europe', 'https://www.bakerhughes.com/', 'CDB Classification: Follow up | Scope: Pump cover | Quotes: 7 | Total Quoted: $1,278,812', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Italy'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.bakerhughes.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Pump cover | Quotes: 7 | Total Quoted: $1,278,812' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Pump cover | Quotes: 7 | Total Quoted: $1,278,812' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-143b8848';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-1ee23c4a', 'cdb-143b8848', 'Mr. Duong', 'dao.duong@BakerHughes.com', '+84 903063311', 'Commodity Manager, Strategic Sourcing', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-a4dd8700', 'Camfil Power Systems AB', 'Austria', 'Asia & Other', 'https://www.camfil.com/en/', 'Scope: Air Intake System | Quotes: 2 | Total Quoted: $411,573', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Austria'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.camfil.com/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'Scope: Air Intake System | Quotes: 2 | Total Quoted: $411,573' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | Scope: Air Intake System | Quotes: 2 | Total Quoted: $411,573' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-a4dd8700';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f054fb8c', 'cdb-a4dd8700', 'Arvind Chandel', 'arvind.chandel@camfil.com', '+46 33178597', 'Manager-Global Sourcing', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-7ebda36e', 'Kawasaki Trading Co., Ltd.', 'Japan', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 3 | Total Quoted: $3,556,350', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 3 | Total Quoted: $3,556,350' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 3 | Total Quoted: $3,556,350' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-7ebda36e';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-2d94be7d', 'cdb-7ebda36e', 'Miho NISHIDA (Ms.)', 'nishida_miho-ksc@corp.khi.co.jp', '+84 (0)91-3473-288', 'Ho Chi Minh City Representative Office', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-daa470e8', 'IOMES Group', 'Hong Kong', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $2,589,751', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Hong Kong'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $2,589,751' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $2,589,751' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-daa470e8';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-85437dee', 'cdb-daa470e8', 'Mr. Bach', 'bach.le@sacons.vn', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-1b84d28c', 'AUMUND Asia (H.K.) Limited', 'Hong Kong', 'Asia & Other', 'https://aumund.com/en/', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Hong Kong'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://aumund.com/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-1b84d28c';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6d9873a6', 'cdb-1b84d28c', 'Michele Gatto', 'gatto@aumund-asia.com', '+ 852 9727 6829', 'MScME - Sales Director', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-af967fbb', 'Esindus S.A.U', 'Spain', 'Europe', 'https://www.esindus.com/', 'CDB Classification: Follow up | Scope: Steel Structure and Steam Ducts | Quotes: 1 | Total Quoted: $1,327,200', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Spain'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.esindus.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel Structure and Steam Ducts | Quotes: 1 | Total Quoted: $1,327,200' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel Structure and Steam Ducts | Quotes: 1 | Total Quoted: $1,327,200' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-af967fbb';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f285fb6e', 'cdb-af967fbb', 'Arancha Abad Gracia', 'Vicente.Morera@hamon.com', '+ 34 91 766 75 93', 'Purchasing Engineer', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-45c36ce5', 'UPTIME', 'Norway', 'Europe', '', 'CDB Classification: Follow up | Scope: Elevator Tower | Quotes: 1', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Norway'), region = COALESCE(NULLIF(region, ''), 'Europe'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Elevator Tower | Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Elevator Tower | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-45c36ce5';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f28a3d25', 'cdb-45c36ce5', 'Alexander Hellesen', 'alexander.hellesen@uptime.no', '+4791811625', 'Sales Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-71007570', 'Nippon Steel Vietnam Co., Ltd.', 'Japan', 'Asia & Other', 'https://www.nipponsteel.com/vn/en/index.html', 'CDB Classification: Follow up | Scope: Cutting plate | Quotes: 1 | Total Quoted: $454,545', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.nipponsteel.com/vn/en/index.html'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Cutting plate | Quotes: 1 | Total Quoted: $454,545' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Cutting plate | Quotes: 1 | Total Quoted: $454,545' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-71007570';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-ab3f95c2', 'cdb-71007570', 'Tatsuro Mori (Mr.)', 'mori.x7e.tatsuroh@vn.nipponsteel.com', '(84) 90-914-9007', 'Sales & Marketing Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-65f486e6', 'GEA Bischoff (Essen, Germany)', 'Germany', 'Europe', 'https://www.gea.com/en/', 'CDB Classification: Follow up | Scope: Steel structure and pipe for candle filter | Quotes: 2 | Total Quoted: $914,396', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.gea.com/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure and pipe for candle filter | Quotes: 2 | Total Quoted: $914,396' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure and pipe for candle filter | Quotes: 2 | Total Quoted: $914,396' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-65f486e6';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-90b15f40', 'cdb-65f486e6', 'Eric Tan', 'Eric.Tan@gea.com', '+60 0192257318', 'Sales Manager - Emission Control, Asia Pacific (excl. China & India)', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-c55400cd', 'Mr. Stephane Von Schon', 'Canada', 'Americas', '', 'CDB Classification: Follow up | Scope: Anchor plate | Quotes: 7 | Total Quoted: $13,232,549 | Remark: Mr. Thac contact', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Canada'), region = COALESCE(NULLIF(region, ''), 'Americas'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Anchor plate | Quotes: 7 | Total Quoted: $13,232,549 | Remark: Mr. Thac contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Anchor plate | Quotes: 7 | Total Quoted: $13,232,549 | Remark: Mr. Thac contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-c55400cd';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-5f21036b', 'CECO Environmental', 'Netherlands', 'Europe', 'https://www.cecoenviro.com/', 'CDB Classification: Follow up | Scope: Bypass system | Quotes: 3 | Total Quoted: $3,828,706', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Netherlands'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.cecoenviro.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Bypass system | Quotes: 3 | Total Quoted: $3,828,706' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Bypass system | Quotes: 3 | Total Quoted: $3,828,706' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-5f21036b';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-2c18d6ab', 'cdb-5f21036b', 'Tijmen van Noord', 'tnoord@onececo.com', '+31 6 17 23 66 12', 'Procurement Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-24a1eab9', 'Công ty TNHH cơ khí Quảng Long Xương', 'Taiwan', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: pressing head plate | Quotes: 1', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Taiwan'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: pressing head plate | Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: pressing head plate | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-24a1eab9';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-5ee293ba', 'JFE Engineering Corporation - Philippine Branch', 'Philippine', 'Asia & Other', 'https://www.jfe-eng.co.jp/en/', 'CDB Classification: Follow up | Scope: Steel structure and duct | Quotes: 7 | Total Quoted: $3,832,479', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Philippine'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.jfe-eng.co.jp/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure and duct | Quotes: 7 | Total Quoted: $3,832,479' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure and duct | Quotes: 7 | Total Quoted: $3,832,479' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-5ee293ba';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-0f5718e6', 'cdb-5ee293ba', 'Jerico Tugade', 'jerico.tugade@jfe-eng.com.ph', '+63 917-586-8846', 'Procurement', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-55affcf2', 'TECHNIP ENGINEERING (THAILAND) LTD,.', 'Thailand', 'Asia & Other', 'www.technipenergies.com', 'CDB Classification: Follow up | Scope: Piping | Quotes: 1', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Thailand'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'www.technipenergies.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Piping | Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Piping | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-55affcf2';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-3981eb32', 'cdb-55affcf2', 'You Bin CHONG (YB)', 'Youbin.chong@external.technipenergies.com', '+60 (12) 387 9893', 'Subcontract Department', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-50b3241e', 'KOMAIHALTEC Inc.', 'Japan', 'Japan', 'https://www.komaihaltec.co.jp/', 'CDB Classification: Follow up | Scope: Steel structure for Bridge | Quotes: 2 | Total Quoted: $7,065,702', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Japan'), website = COALESCE(NULLIF(website, ''), 'https://www.komaihaltec.co.jp/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure for Bridge | Quotes: 2 | Total Quoted: $7,065,702' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure for Bridge | Quotes: 2 | Total Quoted: $7,065,702' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-50b3241e';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-d9548917', 'cdb-50b3241e', 'Naoki Kusaka', 'kusaka@komaihaltec.co.jp', '', 'Manager of Renewable Energy & Overseas business Department', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-ca941cde', 'Metso Outotec', 'Finland', 'Europe', 'https://www.mogroup.com/', 'CDB Classification: Follow up | Scope: Thickener | Quotes: 4 | Total Quoted: $16,469,616', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Finland'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.mogroup.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Thickener | Quotes: 4 | Total Quoted: $16,469,616' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Thickener | Quotes: 4 | Total Quoted: $16,469,616' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-ca941cde';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-2b0a821b', 'cdb-ca941cde', 'Fiona Li', 'wenjie.li@mogroup.com', '+358 40 6726400', 'Senior Sourcing Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-55bd9d37', 'VOGT POWER INTERNATIONAL', 'USA', 'Americas', 'https://www.vogtpower.com/', 'CDB Classification: Good | Scope: HRSG system | Quotes: 28 | Won: 5 | Total Quoted: $38,175,094 | Revenue: $2,813,334', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'USA'), region = COALESCE(NULLIF(region, ''), 'Americas'), website = COALESCE(NULLIF(website, ''), 'https://www.vogtpower.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: HRSG system | Quotes: 28 | Won: 5 | Total Quoted: $38,175,094 | Revenue: $2,813,334' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: HRSG system | Quotes: 28 | Won: 5 | Total Quoted: $38,175,094 | Revenue: $2,813,334' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-55bd9d37';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-65c34ca0', 'cdb-55bd9d37', 'Mr. Tom Block', 'TBlock@vogtpower.com', '502-541-6304', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-962ffd9c', 'Hamon Thermal Europe, S.A.', 'Spain', 'Europe', 'https://www.hamon.com/about/hamon-thermal-europe-sa.html', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 11 | Total Quoted: $38,510,057', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Spain'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.hamon.com/about/hamon-thermal-europe-sa.html'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 11 | Total Quoted: $38,510,057' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 11 | Total Quoted: $38,510,057' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-962ffd9c';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f0bc416f', 'cdb-962ffd9c', 'Ms. Arancha Abad Gracia', 'Arancha.Abad@hamon.com', '', 'contruction manager', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-319eba96', 'cdb-962ffd9c', 'Mr. Martin Bruno', 'Bruno.MARTINS@hamon.com', '', 'contruction manager', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-80ce7d60', 'Bilfinger Engineering & Technologies GmbH', 'Germany', 'Europe', 'https://www.bet.bilfinger.com/en/', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.bet.bilfinger.com/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-80ce7d60';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-d3f2e97a', 'cdb-80ce7d60', 'Mr. Sebastian Fidorra', 'sebastian.fidorra@bilfinger.com', '+49 208 4575-3946', 'Strategic Lead Buyer, Procurement & Supply Management', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-e49f8226', 'Bismark Maritime LTD', 'Papua New Guinea', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: shipbuilding | Quotes: 1', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Papua New Guinea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: shipbuilding | Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: shipbuilding | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-e49f8226';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-d380bb28', 'cdb-e49f8226', 'Marco Schwarz', 'marco_schwarz@bismark.com.pg', '', 'Fleet manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-17bf6adc', 'Pinnacle Kyosei Global Engineers Pvt. Ltd', 'India', 'Asia & Other', 'http://pinnaclekyosei.com', 'CDB Classification: Follow up | Scope: Centrifugal Cast Sleeves | Quotes: 1 | Total Quoted: $104,679', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'India'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'http://pinnaclekyosei.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Centrifugal Cast Sleeves | Quotes: 1 | Total Quoted: $104,679' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Centrifugal Cast Sleeves | Quotes: 1 | Total Quoted: $104,679' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-17bf6adc';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-58f48c56', 'cdb-17bf6adc', 'Sudipta Giri', 'sudipta.giri@pinnaclekyosei.com', '9836896558.0', 'GM-Projects & Marketing', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-276fc2b6', 'SUNGHYUN Co., Ltd.', 'Korea', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: Fabrication gas Tanks | Quotes: 1 | Total Quoted: $403,191', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Fabrication gas Tanks | Quotes: 1 | Total Quoted: $403,191' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Fabrication gas Tanks | Quotes: 1 | Total Quoted: $403,191' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-276fc2b6';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-4087f326', 'cdb-276fc2b6', 'Mr. Tu', 'tuln084@gmail.com', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-799d129e', 'Mit freundlichen Gruß', 'Germany', 'Europe', '', 'CDB Classification: Follow up | Scope: Tub version | Quotes: 2 | Total Quoted: $453,229', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), region = COALESCE(NULLIF(region, ''), 'Europe'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Tub version | Quotes: 2 | Total Quoted: $453,229' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Tub version | Quotes: 2 | Total Quoted: $453,229' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-799d129e';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-aa32bc28', 'cdb-799d129e', 'H. Steinbach', 'horst.vietnam@gmail.com', '+84 908443464', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-693d79c0', 'Kyk Construction Pte Ltd', 'Singapore', 'Asia & Other', '', 'CDB Classification: Bad | Scope: Cast Nylon and Polyurethane Wire Rope Rollers. | Quotes: 1 | Total Quoted: $1,624,274 | Remark: Mr. Andrew contact', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Singapore'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Cast Nylon and Polyurethane Wire Rope Rollers. | Quotes: 1 | Total Quoted: $1,624,274 | Remark: Mr. Andrew contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Cast Nylon and Polyurethane Wire Rope Rollers. | Quotes: 1 | Total Quoted: $1,624,274 | Remark: Mr. Andrew contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-693d79c0';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-e9ae28ba', 'cdb-693d79c0', 'Fong Shi Xiong', 'admin@kykengrg.com', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-d04fe502', 'Ntpc India', 'India', 'Asia & Other', '', 'CDB Classification: Bad | Scope: Steel structure | Quotes: 1 | Total Quoted: $1,324,070 | Remark: No information', 'INACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'India'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Bad | Scope: Steel structure | Quotes: 1 | Total Quoted: $1,324,070 | Remark: No information' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Bad | Scope: Steel structure | Quotes: 1 | Total Quoted: $1,324,070 | Remark: No information' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-d04fe502';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-201c1a3e', 'SMS Group', 'Vietnam', 'Asia & Other', 'www.sms-group.com', 'CDB Classification: Follow up | Scope: Silo, Duct fabrication | Quotes: 4 | Total Quoted: $3,173,186', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'www.sms-group.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Silo, Duct fabrication | Quotes: 4 | Total Quoted: $3,173,186' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Silo, Duct fabrication | Quotes: 4 | Total Quoted: $3,173,186' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-201c1a3e';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-62d344b8', 'cdb-201c1a3e', 'Galpelli ANIL', 'Anil.Galpelli@sms-group.com', '0084 028 35350201
0084 0889985904', 'Supply Chain Management', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-8c9da29d', 'Scheuch Gmbh', 'Austria', 'Europe', 'https://www.scheuch.com', 'CDB Classification: Follow up | Scope: filer | Quotes: 1 | Total Quoted: $30,240', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Austria'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'https://www.scheuch.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: filer | Quotes: 1 | Total Quoted: $30,240' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: filer | Quotes: 1 | Total Quoted: $30,240' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-8c9da29d';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-2ff1f03b', 'cdb-8c9da29d', 'Gerhard Forst', 'Gerhard.Forst@scheuch.com', '+436603429881', 'Senior Purchaser Global Sourcing', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-7217c184', 'Metso Outotec Australia Limited', 'Australia', 'Asia & Other', 'mogroup.com', 'CDB Classification: Follow up | Scope: Fabrication Vertical Mills | Quotes: 2 | Total Quoted: $954,704', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Australia'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'mogroup.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Fabrication Vertical Mills | Quotes: 2 | Total Quoted: $954,704' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Fabrication Vertical Mills | Quotes: 2 | Total Quoted: $954,704' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-7217c184';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-bc4d2455', 'cdb-7217c184', 'Geoff Elliott', 'geoff.elliott@mogroup.com', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-92481a76', 'TOKYU CONSTRUCTION CO., LTD', 'Japan', 'Asia & Other', 'https://www.tokyu-cnst.co.jp/en/', 'CDB Classification: Follow up | Scope: Bridge | Quotes: 2 | Total Quoted: $45,519,961', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'https://www.tokyu-cnst.co.jp/en/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Bridge | Quotes: 2 | Total Quoted: $45,519,961' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Bridge | Quotes: 2 | Total Quoted: $45,519,961' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-92481a76';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-dcfe4a74', 'cdb-92481a76', 'Mr. Pham Minh Tuan', 'tuan@tokyucnst-mmr.com', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-26a1db3e', 'Eujin', 'Korea', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: Steel structures / Two Buildings_Stockton | Quotes: 1 | Total Quoted: $9,852,367', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structures / Two Buildings_Stockton | Quotes: 1 | Total Quoted: $9,852,367' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structures / Two Buildings_Stockton | Quotes: 1 | Total Quoted: $9,852,367' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-26a1db3e';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-c28a8f73', 'cdb-26a1db3e', 'Mr. Eujin', 'geugin@naver.com', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-40049d0c', 'KCI Kraft Consulting Inc.', 'Canada', 'Asia & Other', 'www.kraftconsulting.ca', 'CDB Classification: Follow up | Scope: Steel Posts for Sound Wall in Ontario | Quotes: 6 | Total Quoted: $10,357,678 | Remark: Mr. Thac', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Canada'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'www.kraftconsulting.ca'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel Posts for Sound Wall in Ontario | Quotes: 6 | Total Quoted: $10,357,678 | Remark: Mr. Thac' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel Posts for Sound Wall in Ontario | Quotes: 6 | Total Quoted: $10,357,678 | Remark: Mr. Thac' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-40049d0c';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-22b78f84', 'cdb-40049d0c', 'Mr. Reiner', 'rainer@kraftconsulting.ca', '(1) 604 655 3577', 'President', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-e7e111b8', 'NOAH ACTUATION CO.,LTD', 'Korea', 'Asia & Other', 'Web: http://www.emico.co.kr', 'CDB Classification: Follow up | Scope: PRESSURE OF S-3 PROJECT [SANGJU KOREA] | Quotes: 1 | Total Quoted: $4,297,570', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'Web: http://www.emico.co.kr'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: PRESSURE OF S-3 PROJECT [SANGJU KOREA] | Quotes: 1 | Total Quoted: $4,297,570' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: PRESSURE OF S-3 PROJECT [SANGJU KOREA] | Quotes: 1 | Total Quoted: $4,297,570' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-e7e111b8';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f73b7602', 'cdb-e7e111b8', 'Jimmy Oh', 'shoh@emico.co.kr', 'M. 84-90-385-0351 (VIETNAM)
M. 82-10-2104-7576 (KOREA)', 'Head of Southeast Asia (Vietnam) branch', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-babed227', 'Black & Veatch', 'Thailand', 'Asia & Other', 'Phone: +84 28 3971 9395
Mobile: +84 767031187 / +91 9840568201', 'CDB Classification: Follow up | Scope: pressure vessel, tank, steel structure | Quotes: 6 | Total Quoted: $19,932,564 | Remark: www.babcock.com', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Thailand'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'Phone: +84 28 3971 9395
Mobile: +84 767031187 / +91 9840568201'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: pressure vessel, tank, steel structure | Quotes: 6 | Total Quoted: $19,932,564 | Remark: www.babcock.com' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: pressure vessel, tank, steel structure | Quotes: 6 | Total Quoted: $19,932,564 | Remark: www.babcock.com' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-babed227';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f7f75d1e', 'cdb-babed227', 'Pongthep Sriyathep', 'SriyathepP@BV.com', 'D +66-2797-1718  O +66-2797-1500', 'Project Procurement Manager, Supply Chain – Asia Pacific Region', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-27c6f3df', 'BABCOCK & WILCOX VIETNAM COMPANY LIMITED*', 'Vietnam', 'Asia & Other', 'www.babcock.com', 'CDB Classification: Follow up | Scope: ESP steel fabrication/ P-082540 ESP Casing and Cyclone Platework RFQ | Quotes: 1 | Total Quoted: $511,988', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), website = COALESCE(NULLIF(website, ''), 'www.babcock.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: ESP steel fabrication/ P-082540 ESP Casing and Cyclone Platework RFQ | Quotes: 1 | Total Quoted: $511,988' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: ESP steel fabrication/ P-082540 ESP Casing and Cyclone Platework RFQ | Quotes: 1 | Total Quoted: $511,988' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-27c6f3df';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6a562551', 'cdb-27c6f3df', 'J.Pavala Ayyanar', 'jpayyanar@babcock.com', 'Phone: +84 28 3971 9395
Mobile: +84 767031187 / +91 9840568201', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-6e4dd7ce', 'Wood', 'Spain', 'Europe', 'www.woodplc.com', 'CDB Classification: Follow up | Scope: One (1) HRSG boiler/ P-003428-ENERGAS | Quotes: 1 | Total Quoted: $1,381,753', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Spain'), region = COALESCE(NULLIF(region, ''), 'Europe'), website = COALESCE(NULLIF(website, ''), 'www.woodplc.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: One (1) HRSG boiler/ P-003428-ENERGAS | Quotes: 1 | Total Quoted: $1,381,753' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: One (1) HRSG boiler/ P-003428-ENERGAS | Quotes: 1 | Total Quoted: $1,381,753' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-6e4dd7ce';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6f09a6b2', 'cdb-6e4dd7ce', 'Francisco Pérez Rivera', 'f.perezrivera@woodplc.com', '+34 91 831 9133', 'Senior Purchaser', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-4cd74147', 'Mitsui Miike ( via Shinwa)*', 'Japan', 'Japan', 'https://www.mitsuimiike.co.jp', 'CDB Classification: Good | Remark: Connection from Mr. Sam', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japan'), region = COALESCE(NULLIF(region, ''), 'Japan'), website = COALESCE(NULLIF(website, ''), 'https://www.mitsuimiike.co.jp'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Remark: Connection from Mr. Sam' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Remark: Connection from Mr. Sam' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-4cd74147';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-7bce7dfd', 'CÔNG TY CỔ PHẦN LILAMA 10', '', '', 'https://lilama10.com/', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 2 | Total Quoted: $15,956 | Remark: Mr. Vinh contact', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'https://lilama10.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 2 | Total Quoted: $15,956 | Remark: Mr. Vinh contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 2 | Total Quoted: $15,956 | Remark: Mr. Vinh contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-7bce7dfd';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-a49e8e33', 'Thyssenkrupp Industrial Solutions
(Viet Nam)', '', '', 'https://www.thyssenkrupp.com/en/home', 'CDB Classification: Follow up | Quotes: 1 | Total Quoted: $3,305,169', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'https://www.thyssenkrupp.com/en/home'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Quotes: 1 | Total Quoted: $3,305,169' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Quotes: 1 | Total Quoted: $3,305,169' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-a49e8e33';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-a73c9143', 'cdb-a49e8e33', 'Vu Tuan, Nguyen', 'quang-hoa@thyssenkrupp.com', '+84989895155
+84965640711', '- Mr. Hoà: Project Manager', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-1981405b', 'cdb-a49e8e33', 'Hà Quang Hoà', 'vu-tuan.nguyen@thyssenkrupp.com', '+84989895155
+84965640711', '- Mr. Hoà: Project Manager', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-cdaa9f67', 'Công ty cơ khí xây dựng (DR)', '', '', 'https://dr-bm.com.vn/', 'CDB Classification: Good | Quotes: 2 | Total Quoted: $81,462', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'https://dr-bm.com.vn/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 2 | Total Quoted: $81,462' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 2 | Total Quoted: $81,462' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-cdaa9f67';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-ceb2fada', 'MES7 MECHANICAL SERVICES COMPANY LIMITED', '', '', 'https://mes7.com.vn/', 'CDB Classification: Follow up | Quotes: 1 | Total Quoted: $13,244', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'https://mes7.com.vn/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Quotes: 1 | Total Quoted: $13,244' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Quotes: 1 | Total Quoted: $13,244' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-ceb2fada';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-bb34cac0', 'Công ty cổ phần bột - giấy VNT 19', '', '', '', 'CDB Classification: Follow up | Scope: Phu Long 1, Binh Son, Quang Ngai | Quotes: 1', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Phu Long 1, Binh Son, Quang Ngai | Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Phu Long 1, Binh Son, Quang Ngai | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-bb34cac0';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-9ee05001', 'cdb-bb34cac0', 'Mr. Hưng', '', '+08478488108', 'Commercial', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-616e65ec', 'Keller – North America', '', '', 'https://www.keller-na.com/', 'CDB Classification: Follow up | Quotes: 1 | Total Quoted: $425,843', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'https://www.keller-na.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Quotes: 1 | Total Quoted: $425,843' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Quotes: 1 | Total Quoted: $425,843' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-616e65ec';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-55ee8373', 'cdb-616e65ec', 'Mr. Ruairi Mccann', '', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-cd01f5c7', '29 Investment Construction & Engineering Jsc', '', '', '', 'CDB Classification: Follow up | Scope: 73 Nguyen Trai Street, Thanh Xuan Dist., Ha Noi | Quotes: 1 | Total Quoted: $10,385,445 | Remark: Mr. Vinh contact', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: 73 Nguyen Trai Street, Thanh Xuan Dist., Ha Noi | Quotes: 1 | Total Quoted: $10,385,445 | Remark: Mr. Vinh contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: 73 Nguyen Trai Street, Thanh Xuan Dist., Ha Noi | Quotes: 1 | Total Quoted: $10,385,445 | Remark: Mr. Vinh contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-cd01f5c7';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-b6c6bd59', 'cdb-cd01f5c7', 'Bidding', '', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-6f5833fb', 'Agrimeco & JFE Steel Products Co., Ltd (A&J)', '', '', 'https://www.jfe-steel.co.jp/en/index.html', 'CDB Classification: Follow up | Quotes: 1 | Total Quoted: $2,035,723', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'https://www.jfe-steel.co.jp/en/index.html'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Quotes: 1 | Total Quoted: $2,035,723' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Quotes: 1 | Total Quoted: $2,035,723' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-6f5833fb';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-0e30451e', 'cdb-6f5833fb', 'Takeshi TATSUHARA', 't-tatsuhara@jfe-steel.co.jp', 'MP:+84-91-694-9938', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-5a6aca1c', 'AAF International', '', '', '', 'CDB Classification: Good | Quotes: 2 | Total Quoted: $1,500', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 2 | Total Quoted: $1,500' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 2 | Total Quoted: $1,500' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-5a6aca1c';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-4cfb68e9', 'cdb-5a6aca1c', 'Paula Rodríguez', 'paula.rodriguez@aafintl.com', '+34674148452', 'Project Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-86854d4e', 'CÔNG TY CỔ PHẦN Lisemco 5 MC', '', '', '', 'CDB Classification: Good | Scope: Km6, Freeway No.5, Hung Vuong, Hong Bang, Hai Phong | Quotes: 3 | Total Quoted: $8,077', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Km6, Freeway No.5, Hung Vuong, Hong Bang, Hai Phong | Quotes: 3 | Total Quoted: $8,077' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Km6, Freeway No.5, Hung Vuong, Hong Bang, Hai Phong | Quotes: 3 | Total Quoted: $8,077' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-86854d4e';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-9ea68436', 'cdb-86854d4e', 'Nguyen Van Hung', '', '+8414616180', 'Deputy director', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-1b8f91f8', '189 ONE MEMBER
LIMITED LIABILITY COMPANY', '', '', 'www.dongtau189.com', 'CDB Classification: Good | Scope: Dinh Vu Zone, Dong Hai 2 ward, Hai An district, Hai Phong City - Viet Na | Quotes: 1 | Total Quoted: $774,069', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'www.dongtau189.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Dinh Vu Zone, Dong Hai 2 ward, Hai An district, Hai Phong City - Viet Na | Quotes: 1 | Total Quoted: $774,069' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Dinh Vu Zone, Dong Hai 2 ward, Hai An district, Hai Phong City - Viet Na | Quotes: 1 | Total Quoted: $774,069' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-1b8f91f8';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-421ab994', 'cdb-1b8f91f8', 'Mr. Diễn', '', '+84988839789', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-6b245d05', 'Công ty Cổ phần Xây dựng Kết Cấu Thép IPC', '', '', '', 'CDB Classification: Good | Quotes: 1 | Total Quoted: $67,869 | Remark: Mr. Vinh contact', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 1 | Total Quoted: $67,869 | Remark: Mr. Vinh contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 1 | Total Quoted: $67,869 | Remark: Mr. Vinh contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-6b245d05';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-5526084e', 'Tổng Công ty Hóa chất và Dịch vụ Dầu khí', '', '', '', 'CDB Classification: Good | Quotes: 1 | Total Quoted: $2,234,818', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 1 | Total Quoted: $2,234,818' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 1 | Total Quoted: $2,234,818' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-5526084e';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-63f1fcaf', 'Dong Anh Licogi Mechanical Joint Stock Company (CKDA)', '', '', 'www.ckda.vn', 'CDB Classification: Good | Scope: Km 12+800, National road No.3, Group 6, Dong Anh townlet, Dong Anh District, Hanoi, Vietnam | Quotes: 1 | Total Quoted: $13,175', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'www.ckda.vn'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Km 12+800, National road No.3, Group 6, Dong Anh townlet, Dong Anh District, Hanoi, Vietnam | Quotes: 1 | Total Quoted: $13,175' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Km 12+800, National road No.3, Group 6, Dong Anh townlet, Dong Anh District, Hanoi, Vietnam | Quotes: 1 | Total Quoted: $13,175' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-63f1fcaf';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-e4c6848a', 'cdb-63f1fcaf', 'Tran Manh Tuan', 'tuan.tm@ckda.vn', '+84985088885', 'Commercial', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-1a3fea4d', 'Công ty cổ phần cơ khí xây dựng Amecc', '', '', '', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $694,380', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $694,380' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 1 | Total Quoted: $694,380' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-1a3fea4d';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-4bcf00a8', 'cdb-1a3fea4d', 'Bui Minh Tuan', 'tuanbm@amecc.com.vn', '+84963135969', 'Deputy general director', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-81c737a8', 'MESSER QUANG NGAI INDUSTRIAL GASES CO.,LTD', '', '', 'www.messer.com.vn', 'CDB Classification: Good | Scope: Underground piping | Quotes: 1 | Total Quoted: $1,899,012 | Remark: Mr. Hung (MRO)', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'www.messer.com.vn'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Underground piping | Quotes: 1 | Total Quoted: $1,899,012 | Remark: Mr. Hung (MRO)' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Underground piping | Quotes: 1 | Total Quoted: $1,899,012 | Remark: Mr. Hung (MRO)' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-81c737a8';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-01fcb657', 'cdb-81c737a8', 'Bidding online', '', '', 'Bidding online', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-57b562e5', 'JFE Myanmar', '', '', '', 'CDB Classification: Good | Scope: JFE Engineering Corporation (Yangon Branch) | Quotes: 2 | Total Quoted: $298,128', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: JFE Engineering Corporation (Yangon Branch) | Quotes: 2 | Total Quoted: $298,128' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: JFE Engineering Corporation (Yangon Branch) | Quotes: 2 | Total Quoted: $298,128' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-57b562e5';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-23fb94c7', 'cdb-57b562e5', 'Phyo Ei Maung (Ms)', 'phyoeimaung@mail.jfe-eng.com', '+959401618670', 'Engineer', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-0e6fc796', 'KC Cotrell', '', '', 'www.kc-cottrell.com', 'CDB Classification: Good | Scope: N/A | Quotes: 6 | Total Quoted: $2,535,036', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'www.kc-cottrell.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: N/A | Quotes: 6 | Total Quoted: $2,535,036' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: N/A | Quotes: 6 | Total Quoted: $2,535,036' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-0e6fc796';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-5795ba63', 'cdb-0e6fc796', 'YOUNGCHAN KIM (YC KIM)', 'yckim@kc-cottrell.com', '+82 2 320 6393', 'General Manager
Global Sales & Business Planning Division', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-ee5fd73e', 'Pacific Corp.', '', '', 'www.thaibinhduong.vn', 'CDB Classification: Good | Scope: 9th Floor, 25 Ly Thuong Kiet St., Phan Chu Trinh Ward, Hoan Kiem Dist., Ha Noi | Quotes: 1 | Total Quoted: $1,169,892', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'www.thaibinhduong.vn'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: 9th Floor, 25 Ly Thuong Kiet St., Phan Chu Trinh Ward, Hoan Kiem Dist., Ha Noi | Quotes: 1 | Total Quoted: $1,169,892' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: 9th Floor, 25 Ly Thuong Kiet St., Phan Chu Trinh Ward, Hoan Kiem Dist., Ha Noi | Quotes: 1 | Total Quoted: $1,169,892' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-ee5fd73e';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-27d96576', 'cdb-ee5fd73e', 'Vu Minh Tuan', 'tuan.vm@thaibinhduong.vn', '(+84)979247762', 'Commercial Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-50a9fad0', 'Braden-Europe B.V', '', '', 'www.braden.com', 'CDB Classification: Good | Scope: Casing, duct, by pass systems | Quotes: 3 | Total Quoted: $1,837,182', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'www.braden.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Casing, duct, by pass systems | Quotes: 3 | Total Quoted: $1,837,182' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Casing, duct, by pass systems | Quotes: 3 | Total Quoted: $1,837,182' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-50a9fad0';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-1afcb871', 'cdb-50a9fad0', 'Ivan Martinez', 'ivan.martinez@braden.com', '+34666508538', 'N/A', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-8cacf571', 'VISC International Shipping', '', '', '', 'CDB Classification: Good | Scope: No 4, Street 6, Plot B29-BT5, Waterfront, Vinh Niem Ward, Le Chan Dist., Hai Phong, Vietnam | Quotes: 2 | Total Quoted: $373,959 | Revenue: $977,065', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: No 4, Street 6, Plot B29-BT5, Waterfront, Vinh Niem Ward, Le Chan Dist., Hai Phong, Vietnam | Quotes: 2 | Total Quoted: $373,959 | Revenue: $977,065' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: No 4, Street 6, Plot B29-BT5, Waterfront, Vinh Niem Ward, Le Chan Dist., Hai Phong, Vietnam | Quotes: 2 | Total Quoted: $373,959 | Revenue: $977,065' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-8cacf571';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f7e66f92', 'cdb-8cacf571', 'Mr. Huy', 'huydx.pro@visc-shipping.com', '+84912234291', 'Deputy director', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-40049d0c', 'KCI Kraft Consulting Inc.', '', '', 'www.kraftconsulting.ca', 'CDB Classification: Good | Scope: Sound wall | Quotes: 1 | Total Quoted: $31,634', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'www.kraftconsulting.ca'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Sound wall | Quotes: 1 | Total Quoted: $31,634' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Sound wall | Quotes: 1 | Total Quoted: $31,634' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-40049d0c';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-5a38d3b2', 'cdb-40049d0c', 'Rainer Kraft', 'Rainer@kraftconsulting.ca', '+(1) 604.655.3577', 'President', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-74e30c18', 'TTCL Vietnam Corporation Limited', '', '', 'https://www.ttcl.com/', 'CDB Classification: Good | Scope: 106 Nguyen Van Troi Street,  Ward 8,  Phu Nhuan District,  HCMC,  Vietnam | Quotes: 2 | Total Quoted: $858,514', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'https://www.ttcl.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: 106 Nguyen Van Troi Street,  Ward 8,  Phu Nhuan District,  HCMC,  Vietnam | Quotes: 2 | Total Quoted: $858,514' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: 106 Nguyen Van Troi Street,  Ward 8,  Phu Nhuan District,  HCMC,  Vietnam | Quotes: 2 | Total Quoted: $858,514' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-74e30c18';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-4d4c0331', 'Công ty Cổ phần Cơ khí và Xây lắp Long Biên', '', '', 'N/A', 'CDB Classification: Good | Scope: No 19/197/150, Thạch Ban Street, Long Bien Dist., Ha Noi | Quotes: 1 | Total Quoted: $622,837 | Remark: Mr. Bằng contact', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'N/A'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: No 19/197/150, Thạch Ban Street, Long Bien Dist., Ha Noi | Quotes: 1 | Total Quoted: $622,837 | Remark: Mr. Bằng contact' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: No 19/197/150, Thạch Ban Street, Long Bien Dist., Ha Noi | Quotes: 1 | Total Quoted: $622,837 | Remark: Mr. Bằng contact' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-4d4c0331';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-c33c3b85', 'cdb-4d4c0331', 'Lê Phú Cần', '', '02216282522', 'Director', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-20748fc4', 'KNC', '', '', 'http://www.knc-engineering.com/', 'CDB Classification: Follow up | Scope: Pressure vessel | Quotes: 1 | Total Quoted: $34,659', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'http://www.knc-engineering.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Pressure vessel | Quotes: 1 | Total Quoted: $34,659' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Pressure vessel | Quotes: 1 | Total Quoted: $34,659' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-20748fc4';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-ea9d72f7', 'cdb-20748fc4', 'Baek', 'shbaek@knc-engineering.com', '+82-10-4652-7994', 'Deputy General Manager.', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-ad6ce436', 'PTSC-MC', '', 'Viet Nam', 'https://www.ptsc.com.vn/', 'CDB Classification: Good | Scope: Scaffolding | Quotes: 2 | Total Quoted: $32,562,000', 'ACTIVE');
UPDATE sale_customers SET region = COALESCE(NULLIF(region, ''), 'Viet Nam'), website = COALESCE(NULLIF(website, ''), 'https://www.ptsc.com.vn/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Scaffolding | Quotes: 2 | Total Quoted: $32,562,000' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Scaffolding | Quotes: 2 | Total Quoted: $32,562,000' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-ad6ce436';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-8d6ee4c8', 'cdb-ad6ce436', 'Hoang Thi Thuy', 'Thuythoang@ptsc.com.vn', '+84989 609 714', 'Procurement staff - Planning Dept', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-3b40f703', 'Technimont', '', '', 'https://www.tecnimont.it/', 'CDB Classification: Follow up | Scope: Mechanical and steel structure | Quotes: 1 | Total Quoted: $34,124,969', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'https://www.tecnimont.it/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Mechanical and steel structure | Quotes: 1 | Total Quoted: $34,124,969' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Mechanical and steel structure | Quotes: 1 | Total Quoted: $34,124,969' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-3b40f703';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-5052040c', 'cdb-3b40f703', 'Andrea Sabatino', 'a.sabatino@tecnimont.it', '+39 328 8022762', 'Construction Estimating Engineer', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-93410a5c', 'Sơ chế tôn tấm', '', '', '', 'CDB Classification: Good | Quotes: 1 | Total Quoted: $26,649', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 1 | Total Quoted: $26,649' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 1 | Total Quoted: $26,649' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-93410a5c';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-0f4bbaea', 'Flatiron Construction', '', '', '', 'CDB Classification: Good | Quotes: 1 | Total Quoted: $1,858,055', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 1 | Total Quoted: $1,858,055' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 1 | Total Quoted: $1,858,055' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-0f4bbaea';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-31f9bb70', 'Samsung Engineering Co Ltd', '', '', '', 'CDB Classification: Good | Quotes: 1 | Total Quoted: $8,325,352', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 1 | Total Quoted: $8,325,352' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 1 | Total Quoted: $8,325,352' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-31f9bb70';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-4d95cdd9', 'SHINWA POWER ENGINEERING AND TRADING', '', '', '', 'CDB Classification: Good | Quotes: 3 | Total Quoted: $2,735,687', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 3 | Total Quoted: $2,735,687' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 3 | Total Quoted: $2,735,687' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-4d95cdd9';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-36163292', 'Công ty IBS Holding', '', '', '', 'CDB Classification: Good | Quotes: 1 | Total Quoted: $82,742', 'ACTIVE');
UPDATE sale_customers SET business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 1 | Total Quoted: $82,742' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 1 | Total Quoted: $82,742' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-36163292';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-3c9a547e', 'cdb-36163292', 'Mr Thạc', '', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-99b68da9', 'Asia Erection And Technical Services Joint Stock Company', '', '', 'asiatechjsc.com', 'CDB Classification: Follow up | Scope: 21/56 Vu Xuan Thieu Street, Sai Dong Ward, Long Bien Distric, Ha Noi, Viet Nam', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'asiatechjsc.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: 21/56 Vu Xuan Thieu Street, Sai Dong Ward, Long Bien Distric, Ha Noi, Viet Nam' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: 21/56 Vu Xuan Thieu Street, Sai Dong Ward, Long Bien Distric, Ha Noi, Viet Nam' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-99b68da9';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-9e166a3b', 'cdb-99b68da9', 'Mr Truong Duc Thanh', 'Tunv@asiatechjsc.com', '0903250149
0936938466', 'President
Project Director', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6c0b4dc9', 'cdb-99b68da9', 'Mr Nguyen Van Tu', 'thanhtd@asiatechjsc.com', '0903250149
0936938466', 'President
Project Director', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-850ef400', 'AC Boilers', '', '', 'http://www.acboilers.com/', 'Quotes: 1', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'http://www.acboilers.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-850ef400';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-55f72bc7', 'cdb-850ef400', 'Alberto Pucci', '', '', '- Sales - Sales Department
- Procurement
Subcontrancting Team Leader', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-101681f2', 'cdb-850ef400', 'Matteo Furlato', '', '', '- Sales - Sales Department
- Procurement
Subcontrancting Team Leader', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-daca3e44', 'Star Scientific', 'Australia', '', 'http://www.starscientific.com.au/', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Australia'), website = COALESCE(NULLIF(website, ''), 'http://www.starscientific.com.au/'), updated_at = datetime('now') WHERE id = 'cdb-daca3e44';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-d117276d', 'cdb-daca3e44', 'Ladie Smith', 'lsmith@starscientific.com.au', 'phone: + 61 2 9376 6400
mobile: + 61 420 560 778', '- Administration Assistant
- Deputy Chair, Deputy CEO and Head of Business Development', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6850f1a1', 'cdb-daca3e44', 'Mathew Hingety', 'mhingerty@starscientific.com.au', 'phone: + 61 2 9376 6400
mobile: + 61 420 560 778', '- Administration Assistant
- Deputy Chair, Deputy CEO and Head of Business Development', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-e14c8a46', 'Enapter Co.,Ltd.', 'Thailand', '', 'http://www.enapter.com/', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Thailand'), website = COALESCE(NULLIF(website, ''), 'http://www.enapter.com/'), updated_at = datetime('now') WHERE id = 'cdb-e14c8a46';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-812beea2', 'cdb-e14c8a46', 'Paulina Thomas', 'paulina@enapter.com', '', 'Business Development', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-7a23cf3f', 'JGC CORPORATION', 'Japanese', '', '', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Japanese'), updated_at = datetime('now') WHERE id = 'cdb-7a23cf3f';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-8e54dfb9', 'cdb-7a23cf3f', 'Ryota Shiba', 'shiba.r@jgc.com', 'Tel: +81-80-3607-3827', 'Procurement Department', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-80026ed6', 'SPG DRY COOLING', 'Belgium', '', 'http://www.spgdrycooling.com/', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Belgium'), website = COALESCE(NULLIF(website, ''), 'http://www.spgdrycooling.com/'), updated_at = datetime('now') WHERE id = 'cdb-80026ed6';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6419d05b', 'cdb-80026ed6', 'Pierre Nguyen', 'claudio.loszach@spgdrycooling.com', '- Mobile: +32 (0)475 70 10 55
- M:    +32 471 187 767', '- Sales & Proposal Manager &
Proposal Engineering Leader
- Supply Chain Director', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-0c58dfa8', 'cdb-80026ed6', 'Claudio Loszach', 'pierre.nguyen@spgdrycooling.com', '- Mobile: +32 (0)475 70 10 55
- M:    +32 471 187 767', '- Sales & Proposal Manager &
Proposal Engineering Leader
- Supply Chain Director', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-bd87e5a4', 'Lotte E&C / LG화학 (Lotte Engineering & Construction)', 'Korea', 'Asia & Other', '', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), updated_at = datetime('now') WHERE id = 'cdb-bd87e5a4';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-e040c3c8', 'cdb-bd87e5a4', 'Kim Jinmin(김 진 민 사원)', 'jinmin.kim1@lotte.net', 'tel +82-02-3284-5011  
Cell +82-10-5145-6249', 'Plant Estimation Team(플랜트견적팀)', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-e8f87066', 'Damen Song Cam Shipyard Co.,LTd', 'Vietnam', 'Vietnam/Domestic', 'www.damen.com', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'www.damen.com'), updated_at = datetime('now') WHERE id = 'cdb-e8f87066';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-10e2dbfd', 'cdb-e8f87066', 'Joris Van Tienen', '-hendrik.jan.de.kluiver@damen.com', '- Joris: VN +84904225900
NL +31612145172
- Hendrik: VN +31332474040
NL +31639548758
- Gerben: +31 651571282; +84906232126
- Jeller: +31629722789', '- General Director
- Managing Director
- Site Manager
- Director - Damen Specialized Vessels', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-5093e043', 'cdb-e8f87066', 'Hendrik Jan de Kluiver', 'jelle.brantsma@damen.com', '- Joris: VN +84904225900
NL +31612145172
- Hendrik: VN +31332474040
NL +31639548758
- Gerben: +31 651571282; +84906232126
- Jeller: +31629722789', '- General Director
- Managing Director
- Site Manager
- Director - Damen Specialized Vessels', 0);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-ea71dcf1', 'cdb-e8f87066', 'Gerben den Hartog', 'gerben.den.hartog@damen.com', '- Joris: VN +84904225900
NL +31612145172
- Hendrik: VN +31332474040
NL +31639548758
- Gerben: +31 651571282; +84906232126
- Jeller: +31629722789', '- General Director
- Managing Director
- Site Manager
- Director - Damen Specialized Vessels', 0);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-4bb37c60', 'cdb-e8f87066', 'Jelle Brantsma', 'Joris.van.tienen@damen.com', '- Joris: VN +84904225900
NL +31612145172
- Hendrik: VN +31332474040
NL +31639548758
- Gerben: +31 651571282; +84906232126
- Jeller: +31629722789', '- General Director
- Managing Director
- Site Manager
- Director - Damen Specialized Vessels', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-9f8e001c', 'ASIA networks Pems Co.,Ltd (PEMS)', 'Vietnam', 'Vietnam/Domestic', 'www.pemsvn.com', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'www.pemsvn.com'), updated_at = datetime('now') WHERE id = 'cdb-9f8e001c';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-fd446189', 'cdb-9f8e001c', 'Nguyễn Đức Phong', 'phong.nguyen@asianetworks.com', '+84368389468', 'Sales Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-4a3a5253', '- KAV Engineering & Construction
- Daekwang International (DK)', 'Korea', 'Asia & Other', '', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), updated_at = datetime('now') WHERE id = 'cdb-4a3a5253';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-5ef616d4', 'cdb-4a3a5253', 'Kim Hui Cheol', 'kim4978@gmail.com', 'Kr: +82 10 6877 7799
VN: +84 797898816', 'President', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-fe1126d7', 'Fortescue', 'Vietnam', 'Vietnam/Domestic', '', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), updated_at = datetime('now') WHERE id = 'cdb-fe1126d7';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-c9214b8a', 'cdb-fe1126d7', 'Joe Russo', 'ha.hoang@fortescue.com', 'Joe: +61408721856
- Ms. Ha: +84903429722', '', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-fb93b6ff', 'cdb-fe1126d7', 'Hoang Thi Hong Ha', 'joe.russo@fortescue.com', 'Joe: +61408721856
- Ms. Ha: +84903429722', '', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-a9fab70c', 'Woosung Industry Co.,Ltd', 'Korea', 'Asia & Other', '', 'Won: 79', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'Won: 79' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | Won: 79' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-a9fab70c';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-b10cd207', 'cdb-a9fab70c', 'Jin-Sung, Hwang', 'woosung1977@nate.com', '+82312111673', 'President', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-e3af2fab', 'Siemens Energy (with Braden)', '', '', '', '', 'ACTIVE');

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-a5a76325', 'cdb-e3af2fab', 'Mr. Solamuthu Arumugam Murugappan', 'arumugam.solamuthu@siemens-energy.com', '+6590117220', 'Quality Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-7d86503c', 'Doosan Enerbility Vietnam', 'Vietnam', 'Vietnam/Domestic', '', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), updated_at = datetime('now') WHERE id = 'cdb-7d86503c';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f6f7ea23', 'cdb-7d86503c', 'Tran Khac Tuyen', 'tuyen.trankhac@doosan.com', '+84969118679', 'Deputy Manager of Project Management Division (PM 2 team)', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-85c724cb', 'Daewoo E&C', 'Korea', 'Asia & Other', '', 'Remark: Module fabrication', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Korea'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'Remark: Module fabrication' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | Remark: Module fabrication' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-85c724cb';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-5b5f0c58', 'cdb-85c724cb', 'Jovert Aquino', 'jovert.aquino@daewooenc.com', 'T: +822 2288 3805
M: +821048350878', 'Engineer estimator (Plant Estimation team)', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-e24b99c3', 'Durr Germany', 'Germany', '', 'http://www.durr.com/', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Germany'), website = COALESCE(NULLIF(website, ''), 'http://www.durr.com/'), updated_at = datetime('now') WHERE id = 'cdb-e24b99c3';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-2af94f4d', 'cdb-e24b99c3', 'Damian Delmer', 'Damian.Delmer@durr.com', '- Damian: T: +49 7142 78-1530
M: +49 173 8622830
- Robin:', '- Procurement Project Manager.
- Lead Buyer Structural Steel', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-2d64afc3', 'cdb-e24b99c3', 'Mr. Robin Posten', 'Robin.Posten@durr.com', '- Damian: T: +49 7142 78-1530
M: +49 173 8622830
- Robin:', '- Procurement Project Manager.
- Lead Buyer Structural Steel', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-b27a6e61', 'IHI  CORPORATION', '', '', '', '', 'ACTIVE');

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-2e0a66d9', 'cdb-b27a6e61', 'Mr. Konosuke YOSHII', 'kajima4610@ihi-g.com', 'T: +842439345305
M: +84904534858', '- General Manager 
Vietnam Base
Business Development Division', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-bf763eed', 'Công ty TNHH IHI Infrastructure Asia', 'Vietnam', 'Vietnam/Domestic', '', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), updated_at = datetime('now') WHERE id = 'cdb-bf763eed';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-745ad185', 'cdb-bf763eed', 'Mr. Kajima Kenji', 'thang9584@ihi-g.com', '- Mr. Kajima: 
T: +842258830112
M: 0901528226
- Mr. Thang: 
T: +842258830112
M: 0901586639/0912853859', '- General Director
- Deputy Director/ Sales Manager', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-47f7ae2c', 'cdb-bf763eed', 'Mr. Phương Đình Thắng', 'yoshii7093@ihi-g.com', '- Mr. Kajima: 
T: +842258830112
M: 0901528226
- Mr. Thang: 
T: +842258830112
M: 0901586639/0912853859', '- General Director
- Deputy Director/ Sales Manager', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-6c1f4728', 'Công ty TNHH SOJITZ Việt Nam - CN Hà Nội', 'Vietnam', 'Vietnam/Domestic', '', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), updated_at = datetime('now') WHERE id = 'cdb-6c1f4728';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-21dbfaa2', 'cdb-6c1f4728', 'Trần Mai Lâm', 'tran.lam@sojitz.com', '+84 987879668', 'Phó Chủ tịch', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-dc953799', 'Oriental Consultants Global', 'Vietnam', 'Vietnam/Domestic', 'www.ocglobal.jp', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'www.ocglobal.jp'), updated_at = datetime('now') WHERE id = 'cdb-dc953799';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-c6f677fc', 'cdb-dc953799', 'Dr. Phan Le Binh', 'bnh-p@ocglobal.jp', '+84936148669', 'Deputy General Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-d88a61e2', 'KYC ASIA', 'Singapore', 'Asia & Other', '', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Singapore'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), updated_at = datetime('now') WHERE id = 'cdb-d88a61e2';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-c884e62f', 'cdb-d88a61e2', 'Masatoshi Naokawa (Mark)', 'tanchoonheng989@gmail.com', '+65 81298551
+65 98280300
+65 96233245', '- Director
- Director/Advisory
- Managing Director', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-32dfbb74', 'cdb-d88a61e2', 'Peter Tan', 'ma-naokawa@kyc.co.jp', '+65 81298551
+65 98280300
+65 96233245', '- Director
- Director/Advisory
- Managing Director', 0);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-0621feb2', 'cdb-d88a61e2', 'Kim Tae Jung', 'kim@kycscaffolding.com', '+65 81298551
+65 98280300
+65 96233245', '- Director
- Director/Advisory
- Managing Director', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-e7450bb3', 'Tổng Công ty Xây dựng cảng Trung Quốc (China Harbour Engineering Company LTD', 'Vietnam', 'Vietnam/Domestic', '', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), updated_at = datetime('now') WHERE id = 'cdb-e7450bb3';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-367d9dea', 'cdb-e7450bb3', 'Thiện Đỉnh Long', 'dlshan@chec.bj.cn', '+84 817808111
+84 929182226', '- Phó Tổng giám đốc
- Giám đốc Ban Đấu thầu', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-88fe7368', 'cdb-e7450bb3', 'Phạm Đức Cường', 'duccuong.chec@gmail.com', '+84 817808111
+84 929182226', '- Phó Tổng giám đốc
- Giám đốc Ban Đấu thầu', 0);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-9359e786', 'PEJA VIETNAM', 'Vietnam', 'Vietnam/Domestic', 'www.pejavietnam.com', '', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'www.pejavietnam.com'), updated_at = datetime('now') WHERE id = 'cdb-9359e786';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-074a48b3', 'cdb-9359e786', 'Doan Nam', 'nam@pejavietnam.com', '+84 2438244627', 'Chief Representative', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-272511c7', 'HEXAGON', '', '', '', '', 'ACTIVE');

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-58f20fb8', 'CTCI', '', '', '', '', 'ACTIVE');

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-c709d3e0', 'Maerz', '', '', '', '', 'ACTIVE');

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-4baa0965', 'Baltec', '', '', 'www.baltec.com.au', 'Remark: Reconnect with new contact person', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'www.baltec.com.au'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'Remark: Reconnect with new contact person' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | Remark: Reconnect with new contact person' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-4baa0965';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-fac2bf31', 'cdb-4baa0965', 'Stefan Meijers', 'stefan.meijers@egl.com.au', '+31 653773475', 'Regional Manager', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-b24bb989', 'Phúc Thành Company', '', '', '', '', 'ACTIVE');

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-6eeda39d', 'Babcock Client Southern Co.', '', '', '', '', 'ACTIVE');

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-50392c27', 'STF Loterios s.r.l.', '', '', 'www.stf-loterios.com', 'Quotes: 25009 | Remark: Via Monte Grappa 44
21040 - Gerenzano (VA) - Italy', 'ACTIVE');
UPDATE sale_customers SET website = COALESCE(NULLIF(website, ''), 'www.stf-loterios.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'Quotes: 25009 | Remark: Via Monte Grappa 44
21040 - Gerenzano (VA) - Italy' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | Quotes: 25009 | Remark: Via Monte Grappa 44
21040 - Gerenzano (VA) - Italy' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-50392c27';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-153ee71d', 'cdb-50392c27', 'Stephen Stein', 'stephen.stein@stf-loterios.com', '+1.281.908.6200', 'Manager Asia-Pacific', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-24a1eab9', 'Công ty TNHH cơ khí Quảng Long Xương', 'Taiwan', 'Asia & Other', '', 'CDB Classification: Follow up | Scope: pressing head plate | Quotes: 1', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Taiwan'), region = COALESCE(NULLIF(region, ''), 'Asia & Other'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: pressing head plate | Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: pressing head plate | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-24a1eab9';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-7bce7dfd', 'CÔNG TY CỔ PHẦN LILAMA 10', 'Vietnam', 'Vietnam/Domestic', 'https://lilama10.com/', 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 2 | Total Quoted: $15,956', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'https://lilama10.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Steel structure | Quotes: 2 | Total Quoted: $15,956' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Steel structure | Quotes: 2 | Total Quoted: $15,956' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-7bce7dfd';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-a49e8e33', 'Thyssenkrupp Industrial Solutions
(Viet Nam)', 'Vietnam', 'Vietnam/Domestic', 'https://www.thyssenkrupp.com/en/home', 'CDB Classification: Follow up | Quotes: 1 | Total Quoted: $3,305,169', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'https://www.thyssenkrupp.com/en/home'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Quotes: 1 | Total Quoted: $3,305,169' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Quotes: 1 | Total Quoted: $3,305,169' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-a49e8e33';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-a73c9143', 'cdb-a49e8e33', 'Vu Tuan, Nguyen', 'vu-tuan.nguyen@thyssenkrupp.com', '+84989895155', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-cdaa9f67', 'Công ty cơ khí xây dựng (DR)', 'Vietnam', 'Vietnam/Domestic', 'https://dr-bm.com.vn/', 'CDB Classification: Good | Quotes: 2 | Total Quoted: $81,462', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'https://dr-bm.com.vn/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 2 | Total Quoted: $81,462' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 2 | Total Quoted: $81,462' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-cdaa9f67';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-bb34cac0', 'Công ty cổ phần bột - giấy VNT 19', 'Vietnam', 'Vietnam/Domestic', '', 'CDB Classification: Follow up | Scope: Phu Long 1, Binh Son, Quang Ngai | Quotes: 1', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: Phu Long 1, Binh Son, Quang Ngai | Quotes: 1' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: Phu Long 1, Binh Son, Quang Ngai | Quotes: 1' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-bb34cac0';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-9ee05001', 'cdb-bb34cac0', 'Mr. Hưng', '', '+08478488108', 'Commercial', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-cd01f5c7', '29 Investment Construction & Engineering Jsc', 'Vietnam', 'Vietnam/Domestic', '', 'CDB Classification: Follow up | Scope: 73 Nguyen Trai Street, Thanh Xuan Dist., Ha Noi | Quotes: 1 | Total Quoted: $10,385,445', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: 73 Nguyen Trai Street, Thanh Xuan Dist., Ha Noi | Quotes: 1 | Total Quoted: $10,385,445' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: 73 Nguyen Trai Street, Thanh Xuan Dist., Ha Noi | Quotes: 1 | Total Quoted: $10,385,445' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-cd01f5c7';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-b6c6bd59', 'cdb-cd01f5c7', 'Bidding', '', '', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-86854d4e', 'CÔNG TY CỔ PHẦN Lisemco 5 MC', 'Vietnam', 'Vietnam/Domestic', '', 'CDB Classification: Good | Scope: Km6, Freeway No.5, Hung Vuong, Hong Bang, Hai Phong | Quotes: 3 | Total Quoted: $8,077', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Km6, Freeway No.5, Hung Vuong, Hong Bang, Hai Phong | Quotes: 3 | Total Quoted: $8,077' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Km6, Freeway No.5, Hung Vuong, Hong Bang, Hai Phong | Quotes: 3 | Total Quoted: $8,077' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-86854d4e';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-9ea68436', 'cdb-86854d4e', 'Nguyen Van Hung', '', '+8414616180', 'Deputy director', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-1b8f91f8', '189 ONE MEMBER
LIMITED LIABILITY COMPANY', 'Vietnam', 'Vietnam/Domestic', 'www.dongtau189.com', 'CDB Classification: Good | Scope: Dinh Vu Zone, Dong Hai 2 ward, Hai An district, Hai Phong City - Viet Na | Quotes: 1 | Total Quoted: $774,069', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'www.dongtau189.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Dinh Vu Zone, Dong Hai 2 ward, Hai An district, Hai Phong City - Viet Na | Quotes: 1 | Total Quoted: $774,069' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Dinh Vu Zone, Dong Hai 2 ward, Hai An district, Hai Phong City - Viet Na | Quotes: 1 | Total Quoted: $774,069' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-1b8f91f8';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-421ab994', 'cdb-1b8f91f8', 'Mr. Diễn', '', '+84988839789', '', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-6b245d05', 'Công ty Cổ phần Xây dựng Kết Cấu Thép IPC', 'Vietnam', 'Vietnam/Domestic', '', 'CDB Classification: Good | Quotes: 1 | Total Quoted: $67,869', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 1 | Total Quoted: $67,869' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 1 | Total Quoted: $67,869' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-6b245d05';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-5526084e', 'Tổng Công ty Hóa chất và Dịch vụ Dầu khí', 'Vietnam', 'Vietnam/Domestic', '', 'CDB Classification: Good | Quotes: 1 | Total Quoted: $2,234,818', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Quotes: 1 | Total Quoted: $2,234,818' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Quotes: 1 | Total Quoted: $2,234,818' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-5526084e';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-63f1fcaf', 'Dong Anh Licogi Mechanical Joint Stock Company (CKDA)', 'Vietnam', 'Vietnam/Domestic', 'www.ckda.vn', 'CDB Classification: Good | Scope: Km 12+800, National road No.3, Group 6, Dong Anh townlet, Dong Anh District, Hanoi, Vietnam | Quotes: 1 | Total Quoted: $13,175', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'www.ckda.vn'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Km 12+800, National road No.3, Group 6, Dong Anh townlet, Dong Anh District, Hanoi, Vietnam | Quotes: 1 | Total Quoted: $13,175' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Km 12+800, National road No.3, Group 6, Dong Anh townlet, Dong Anh District, Hanoi, Vietnam | Quotes: 1 | Total Quoted: $13,175' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-63f1fcaf';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-e4c6848a', 'cdb-63f1fcaf', 'Tran Manh Tuan', 'tuan.tm@ckda.vn', '+84985088885', 'Commercial', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-8cacf571', 'VISC International Shipping', 'Vietnam', 'Vietnam/Domestic', '', 'CDB Classification: Good | Scope: No 4, Street 6, Plot B29-BT5, Waterfront, Vinh Niem Ward, Le Chan Dist., Hai Phong, Vietnam | Quotes: 2 | Total Quoted: $373,959 | Revenue: $977,065', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: No 4, Street 6, Plot B29-BT5, Waterfront, Vinh Niem Ward, Le Chan Dist., Hai Phong, Vietnam | Quotes: 2 | Total Quoted: $373,959 | Revenue: $977,065' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: No 4, Street 6, Plot B29-BT5, Waterfront, Vinh Niem Ward, Le Chan Dist., Hai Phong, Vietnam | Quotes: 2 | Total Quoted: $373,959 | Revenue: $977,065' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-8cacf571';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-f7e66f92', 'cdb-8cacf571', 'Mr. Huy', 'huydx.pro@visc-shipping.com', '+84912234291', 'Deputy director', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-74e30c18', 'TTCL Vietnam Corporation Limited', 'Vietnam', 'Vietnam/Domestic', 'https://www.ttcl.com/', 'CDB Classification: Good | Scope: 106 Nguyen Van Troi Street,  Ward 8,  Phu Nhuan District,  HCMC,  Vietnam | Quotes: 2 | Total Quoted: $858,514', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'https://www.ttcl.com/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: 106 Nguyen Van Troi Street,  Ward 8,  Phu Nhuan District,  HCMC,  Vietnam | Quotes: 2 | Total Quoted: $858,514' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: 106 Nguyen Van Troi Street,  Ward 8,  Phu Nhuan District,  HCMC,  Vietnam | Quotes: 2 | Total Quoted: $858,514' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-74e30c18';

INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-4d4c0331', 'Công ty Cổ phần Cơ khí và Xây lắp Long Biên', 'Vietnam', 'Vietnam/Domestic', 'N/A', 'CDB Classification: Good | Scope: No 19/197/150, Thạch Ban Street, Long Bien Dist., Ha Noi | Quotes: 1 | Total Quoted: $622,837', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'N/A'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: No 19/197/150, Thạch Ban Street, Long Bien Dist., Ha Noi | Quotes: 1 | Total Quoted: $622,837' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: No 19/197/150, Thạch Ban Street, Long Bien Dist., Ha Noi | Quotes: 1 | Total Quoted: $622,837' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-4d4c0331';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-c33c3b85', 'cdb-4d4c0331', 'Lê Phú Cần', '', '02216282522', 'Director', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-ad6ce436', 'PTSC-MC', 'Vietnam', 'Vietnam/Domestic', 'https://www.ptsc.com.vn/', 'CDB Classification: Good | Scope: Scaffolding | Quotes: 2 | Total Quoted: $32,562,000', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'https://www.ptsc.com.vn/'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Good | Scope: Scaffolding | Quotes: 2 | Total Quoted: $32,562,000' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Good | Scope: Scaffolding | Quotes: 2 | Total Quoted: $32,562,000' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-ad6ce436';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-8d6ee4c8', 'cdb-ad6ce436', 'Hoang Thi Thuy', 'Thuythoang@ptsc.com.vn', '+84989 609 714', 'Procurement staff - Planning Dept', 1);
INSERT OR IGNORE INTO sale_customers (id, name, country, region, website, business_description, status)
  VALUES ('cdb-99b68da9', 'Asia Erection And Technical Services Joint Stock Company', 'Vietnam', 'Vietnam/Domestic', 'asiatechjsc.com', 'CDB Classification: Follow up | Scope: 21/56 Vu Xuan Thieu Street, Sai Dong Ward, Long Bien Distric, Ha Noi, Viet Nam', 'ACTIVE');
UPDATE sale_customers SET country = COALESCE(NULLIF(country, ''), 'Vietnam'), region = COALESCE(NULLIF(region, ''), 'Vietnam/Domestic'), website = COALESCE(NULLIF(website, ''), 'asiatechjsc.com'), business_description = CASE WHEN business_description IS NULL OR business_description = '' THEN 'CDB Classification: Follow up | Scope: 21/56 Vu Xuan Thieu Street, Sai Dong Ward, Long Bien Distric, Ha Noi, Viet Nam' WHEN business_description NOT LIKE '%CDB Classification%' THEN business_description || ' | CDB Classification: Follow up | Scope: 21/56 Vu Xuan Thieu Street, Sai Dong Ward, Long Bien Distric, Ha Noi, Viet Nam' ELSE business_description END, updated_at = datetime('now') WHERE id = 'cdb-99b68da9';

INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-9e166a3b', 'cdb-99b68da9', 'Mr Truong Duc Thanh', 'Tunv@asiatechjsc.com', '0903250149
0936938466', 'President
Project Director', 1);
INSERT OR IGNORE INTO sale_customer_contacts (id, customer_id, name, email, phone, position, is_primary)
  VALUES ('cdbcc-6c0b4dc9', 'cdb-99b68da9', 'Mr Nguyen Van Tu', 'thanhtd@asiatechjsc.com', '0903250149
0936938466', 'President
Project Director', 0);

-- Total: 172 customers, 164 contacts from Client_Data_Base