-- ═══════════════════════════════════════════════════════════
-- 19_won_contracts.sql
-- Source: Quotation Record - Contract sheet (187 awarded quotations)
-- Generated: 2026-04-29 (regenerated with proper SQL)
-- Updates sale_quotation_history: status → WON, adds contract_date via remark
-- ═══════════════════════════════════════════════════════════

-- Add contract_date column if missing (safe ALTER)
-- SQLite: ALTER TABLE ADD COLUMN is idempotent-safe if we catch error
-- We'll store contract_date in remark field as prefix instead

-- 25112 | Wendt-Noise Control GMBH | Acoustic Enclosure, ladder&platform | Contract: 2025-08-11
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-08-11 | ' || COALESCE(remark, '') WHERE quotation_no = 25112 AND status != 'WON';
-- 25111 | Siempelkamp Energy & Drying Solutions GmbH | duct, chute and diverter flap | Contract: 2025-08-29
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-08-29 | ' || COALESCE(remark, '') WHERE quotation_no = 25111 AND status != 'WON';
-- 25110 | Büttner Energie- und Trocknungstechnik GmbH | Duct | Contract: 00:00:00
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract date unknown | ' || COALESCE(remark, '') WHERE quotation_no = 25110 AND status != 'WON';
-- 25109 | VOGT POWER INTERNATIONAL | Free issue materials | Contract: 00:00:00
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract date unknown | ' || COALESCE(remark, '') WHERE quotation_no = 25109 AND status != 'WON';
-- 25108 | VOGT POWER INTERNATIONAL | Garlock Gylon gasket | Contract: 00:00:00
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract date unknown | ' || COALESCE(remark, '') WHERE quotation_no = 25108 AND status != 'WON';
-- 25104 | VOGT POWER INTERNATIONAL | Bumpers | Contract: 2025-08-13
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-08-13 | ' || COALESCE(remark, '') WHERE quotation_no = 25104 AND status != 'WON';
-- 25075 | SHINWA ENGINEERING CO.,LTD | Frame | Contract: 2025-05-20
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-05-20 | ' || COALESCE(remark, '') WHERE quotation_no = 25075 AND status != 'WON';
-- 25069 | VOGT POWER INTERNATIONAL | Name plate | Contract: 2025-04-29
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-04-29 | ' || COALESCE(remark, '') WHERE quotation_no = 25069 AND status != 'WON';
-- 25066 | Thyssenkrupp Polysius (Viet Nam) | Duct, piping | Contract: 2025-04-24
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-04-24 | ' || COALESCE(remark, '') WHERE quotation_no = 25066 AND status != 'WON';
-- 25054 | Wendt-Noise Control GMBH | Acoustic Enclosure, ladder&platform | Contract: 2025-05-19
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-05-19 | ' || COALESCE(remark, '') WHERE quotation_no = 25054 AND status != 'WON';
-- 25051 | Thyssenkrupp Polysius (Viet Nam) | 03 new items | Contract: 2024-12-18
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-12-18 | ' || COALESCE(remark, '') WHERE quotation_no = 25051 AND status != 'WON';
-- 25049 | VOGT POWER INTERNATIONAL | Casing | Contract: 2025-04-10
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-04-10 | ' || COALESCE(remark, '') WHERE quotation_no = 25049 AND status != 'WON';
-- 25048 | CÔNG TY CỔ PHẦN Lisemco 5 MC | Làm sạch và sơn | Contract: 2025-03-25
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-03-25 | ' || COALESCE(remark, '') WHERE quotation_no = 25048 AND status != 'WON';
-- 25041 | VISC International Shipping JSC | Sửa chữa các hạng mục phát sinh | Contract: 2025-04-15
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-04-15 | ' || COALESCE(remark, '') WHERE quotation_no = 25041 AND status != 'WON';
-- 25033 | SHINWA ENGINEERING CO.,LTD | Frame | Contract: 2025-03-04
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-03-04 | ' || COALESCE(remark, '') WHERE quotation_no = 25033 AND status != 'WON';
-- 25032 | CÔNG TY TNHH MTV ĐÓNG TÀU HẠ LONG | Doa chải sơn chống rỉ các block | Contract: 00:00:00
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract date unknown | ' || COALESCE(remark, '') WHERE quotation_no = 25032 AND status != 'WON';
-- 25029 | Wendt-Noise Control GMBH | Steel structure hot dip galvanized | Contract: 2025-03-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-03-26 | ' || COALESCE(remark, '') WHERE quotation_no = 25029 AND status != 'WON';
-- 25027 | VISC International Shipping JSC | Lifting ear, lashing ear | Contract: 2025-06-13
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-06-13 | ' || COALESCE(remark, '') WHERE quotation_no = 25027 AND status != 'WON';
-- 24154 | Büttner Energie- und Trocknungstechnik GmbH | Frame | Contract: 2025-05-15
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-05-15 | ' || COALESCE(remark, '') WHERE quotation_no = 24154 AND status != 'WON';
-- 24154 | SHINWA ENGINEERING CO.,LTD | Frame | Contract: 2024-11-15
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-11-15 | ' || COALESCE(remark, '') WHERE quotation_no = 24154 AND status != 'WON';
-- 25013 | VOGT POWER INTERNATIONAL | Construction Lifting Device | Contract: 2025-03-06
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-03-06 | ' || COALESCE(remark, '') WHERE quotation_no = 25013 AND status != 'WON';
-- 25011 | VOGT POWER INTERNATIONAL | Large Bore Structural Steel Pipe Supports | Contract: 2025-02-05
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-02-05 | ' || COALESCE(remark, '') WHERE quotation_no = 25011 AND status != 'WON';
-- 24174 | Braden-Europe B.V | Diverter | Contract: 2025-03-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-03-26 | ' || COALESCE(remark, '') WHERE quotation_no = 24174 AND status != 'WON';
-- 24154 | Büttner Energie- und Trocknungstechnik GmbH | Duct from Dry to Cyclone | Contract: 2025-06-24
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-06-24 | ' || COALESCE(remark, '') WHERE quotation_no = 24154 AND status != 'WON';
-- 24154 | Büttner Energie | drum dryer, duct and cyclone | Contract: 00:00:00
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract date unknown | ' || COALESCE(remark, '') WHERE quotation_no = 24154 AND status != 'WON';
-- 24152 | Braden | Flap damper (2) | Contract: 2025-02-17
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-02-17 | ' || COALESCE(remark, '') WHERE quotation_no = 24152 AND status != 'WON';
-- 24151 | Braden-Europe B.V | Whyalla | Contract: 2025-01-16
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-01-16 | ' || COALESCE(remark, '') WHERE quotation_no = 24151 AND status != 'WON';
-- 24150 | Thyssenkrupp Polysius (Vietnam) Ltd | Tertiary air duct | Contract: 2024-12-18
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-12-18 | ' || COALESCE(remark, '') WHERE quotation_no = 24150 AND status != 'WON';
-- 24146 | SHINWA ENGINEERING CO.,LTD | Shiploader | Contract: 2025-06-30
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2025-06-30 | ' || COALESCE(remark, '') WHERE quotation_no = 24146 AND status != 'WON';
-- 24139 | VOGT POWER INTERNATIONAL | V17556 PT Freeport | Contract: 2024-11-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-11-26 | ' || COALESCE(remark, '') WHERE quotation_no = 24139 AND status != 'WON';
-- 24137 | CÔNG TY TNHH MTV 189 | XP-01 | Contract: 2024-10-05
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-10-05 | ' || COALESCE(remark, '') WHERE quotation_no = 24137 AND status != 'WON';
-- 24110 | Thyssenkrupp Polysius (Viet Nam) | Chutes package (29 tons) | Contract: 2024-08-07
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-08-07 | ' || COALESCE(remark, '') WHERE quotation_no = 24110 AND status != 'WON';
-- 24099 | CÔNG TY TNHH MỘT THÀNH VIÊN 189 | Cutting | Contract: 2024-07-01
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-07-01 | ' || COALESCE(remark, '') WHERE quotation_no = 24099 AND status != 'WON';
-- 24093 | Damen | blocks building for Damen vessels | Contract: 2024-11-05
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-11-05 | ' || COALESCE(remark, '') WHERE quotation_no = 24093 AND status != 'WON';
-- 24092 | Thyssenkrupp Polysius (Viet Nam) | Chutes package | Contract: 2024-07-22
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-07-22 | ' || COALESCE(remark, '') WHERE quotation_no = 24092 AND status != 'WON';
-- 24091 | VOGT POWER INTERNATIONAL | adding work (flange SS321) | Contract: 2024-08-08
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-08-08 | ' || COALESCE(remark, '') WHERE quotation_no = 24091 AND status != 'WON';
-- 24070 | VOGT POWER INTERNATIONAL | V17552- storage | Contract: 2024-09-16
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-09-16 | ' || COALESCE(remark, '') WHERE quotation_no = 24070 AND status != 'WON';
-- 24057 | Braden | Adding work - Platform + Ladder | Contract: 2024-11-21
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-11-21 | ' || COALESCE(remark, '') WHERE quotation_no = 24057 AND status != 'WON';
-- 24057 | Braden | Fabrication one (1) exhaus stack | Contract: 2024-07-18
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-07-18 | ' || COALESCE(remark, '') WHERE quotation_no = 24057 AND status != 'WON';
-- 24039 | VOGT POWER INTERNATIONAL | Ductwork | Contract: 2024-05-09
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-05-09 | ' || COALESCE(remark, '') WHERE quotation_no = 24039 AND status != 'WON';
-- 24036 | VOGT POWER INTERNATIONAL | Manufacturing of silencers | Contract: 2024-06-19
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-06-19 | ' || COALESCE(remark, '') WHERE quotation_no = 24036 AND status != 'WON';
-- 24032 | IBS Corporation | Supply material, fabrication, painting (steel beams of Elavator) | Contract: 2024-04-23
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-04-23 | ' || COALESCE(remark, '') WHERE quotation_no = 24032 AND status != 'WON';
-- 24026 | DR (Công ty CP Cơ khí xây dựng) | Painting, poonton assembly | Contract: 2024-02-28
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-02-28 | ' || COALESCE(remark, '') WHERE quotation_no = 24026 AND status != 'WON';
-- 23153 | Braden | manufacturing of 10 (ten) open cycle stacks | Contract: 2024-06-30
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-06-30 | ' || COALESCE(remark, '') WHERE quotation_no = 23153 AND status != 'WON';
-- 23145 | VOGT INTERNATIONAL | Insulation pins | Contract: 2023-12-01
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-12-01 | ' || COALESCE(remark, '') WHERE quotation_no = 23145 AND status != 'WON';
-- 23143 | VerBIO Vereinigte BioEnergie AG | Heat Exchanger (U-Stamp) | Contract: 2023-11-16
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-11-16 | ' || COALESCE(remark, '') WHERE quotation_no = 23143 AND status != 'WON';
-- 23134 | Dong Anh Licogi | Coal shed support | Contract: 2023-11-21
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-11-21 | ' || COALESCE(remark, '') WHERE quotation_no = 23134 AND status != 'WON';
-- 23131 | SHINWA ENGINEERING CO.,LTD | Boom, bucket wheel of reclaimer | Contract: 2024-03-04
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2024-03-04 | ' || COALESCE(remark, '') WHERE quotation_no = 23131 AND status != 'WON';
-- 23127 | Công ty TNHH cách nhiệt và ống gió Huỳnh Kim | Cut and roll the tub base protection panel | Contract: 2023-10-24
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-10-24 | ' || COALESCE(remark, '') WHERE quotation_no = 23127 AND status != 'WON';
-- 23123 | VISC International Shipping JSC | 03 RGT Crane | Contract: 2023-11-10
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-11-10 | ' || COALESCE(remark, '') WHERE quotation_no = 23123 AND status != 'WON';
-- 23109 | Verbio | CO2 Degassing Tank | Contract: 2023-09-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-09-26 | ' || COALESCE(remark, '') WHERE quotation_no = 23109 AND status != 'WON';
-- 23103 | VISC International Shipping JSC | Crane 200T | Contract: 2023-09-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-09-26 | ' || COALESCE(remark, '') WHERE quotation_no = 23103 AND status != 'WON';
-- 23098 | VISC International Shipping JSC | Crane | Contract: 2023-08-15
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-08-15 | ' || COALESCE(remark, '') WHERE quotation_no = 23098 AND status != 'WON';
-- 23089 | Công ty TNHH MTV dịch vụ cơ khí Hàng Hải (PTSC) | Provide scaffolding tubes | Contract: 2023-08-01
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-08-01 | ' || COALESCE(remark, '') WHERE quotation_no = 23089 AND status != 'WON';
-- 23087 | VOGT POWER INTERNATIONAL | Fabrication drain piping for HRSG | Contract: 2023-09-11
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-09-11 | ' || COALESCE(remark, '') WHERE quotation_no = 23087 AND status != 'WON';
-- 23085 | Stejasa | NDE Requirement/ 7229002 VPIT Manzanillo | Contract: 2023-08-01
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-08-01 | ' || COALESCE(remark, '') WHERE quotation_no = 23085 AND status != 'WON';
-- 23084 | Stejasa | Revised drawings/ 7229002 VPIT Manzanillo | Contract: 2023-08-01
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-08-01 | ' || COALESCE(remark, '') WHERE quotation_no = 23084 AND status != 'WON';
-- 23083 | KC Cottrell | MSL UNIT5 | Contract: 2023-07-28
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-07-28 | ' || COALESCE(remark, '') WHERE quotation_no = 23083 AND status != 'WON';
-- 23082 | KC Cottrell | MSL UNIT4 | Contract: 2023-07-28
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-07-28 | ' || COALESCE(remark, '') WHERE quotation_no = 23082 AND status != 'WON';
-- 23079 | CÔNG TY CỔ PHẦN Lisemco 5 MC | Labor for paint | Contract: 2023-07-11
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-07-11 | ' || COALESCE(remark, '') WHERE quotation_no = 23079 AND status != 'WON';
-- 23078 | KC Cottrell | TCE | Contract: 2023-07-28
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-07-28 | ' || COALESCE(remark, '') WHERE quotation_no = 23078 AND status != 'WON';
-- 23077 | VOGT POWER INTERNATIONAL | Field Installed Components/ 550 - PT Amman | Contract: 2023-09-11
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-09-11 | ' || COALESCE(remark, '') WHERE quotation_no = 23077 AND status != 'WON';
-- 23075 | VOGT POWER INTERNATIONAL | HRSG system/ V17553 San Pedro One Unit | Contract: 2023-08-07
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-08-07 | ' || COALESCE(remark, '') WHERE quotation_no = 23075 AND status != 'WON';
-- 23073 | VOGT POWER INTERNATIONAL | HRSG system/ V17552 Guyana (4) Four Units | Contract: 2023-08-10
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-08-10 | ' || COALESCE(remark, '') WHERE quotation_no = 23073 AND status != 'WON';
-- 23070 | CÔNG TY CỔ PHẦN Lisemco 5 MC | Cutting the Tubes | Contract: 2023-06-23
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-06-23 | ' || COALESCE(remark, '') WHERE quotation_no = 23070 AND status != 'WON';
-- 23069 | Công ty Cổ phần Cơ khí Đông Anh | Drilling plate | Contract: 2023-07-10
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-07-10 | ' || COALESCE(remark, '') WHERE quotation_no = 23069 AND status != 'WON';
-- 23064 | JFE Engineering Corporation | Labor for delivery steel plate | Contract: 2023-06-19
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-06-19 | ' || COALESCE(remark, '') WHERE quotation_no = 23064 AND status != 'WON';
-- 23056 | CÔNG TY TNHH MỘT THÀNH VIÊN 189 | Manufacturing of the block | Contract: 2023-06-05
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-06-05 | ' || COALESCE(remark, '') WHERE quotation_no = 23056 AND status != 'WON';
-- 23049 | VOGT POWER INTERNATIONAL | Drum & Tank Support Beams/ 550 - PT Amman project | Contract: 2023-05-24
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-05-24 | ' || COALESCE(remark, '') WHERE quotation_no = 23049 AND status != 'WON';
-- 23047 | VOGT POWER INTERNATIONAL | Drain Funnels/ 549 - Manzanillo project | Contract: 2023-05-16
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-05-16 | ' || COALESCE(remark, '') WHERE quotation_no = 23047 AND status != 'WON';
-- 23041 | VERBIO Vereinigte Bio Energie AG | TGN / RFQ CIP tank | Contract: 2023-07-07
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-07-07 | ' || COALESCE(remark, '') WHERE quotation_no = 23041 AND status != 'WON';
-- 23036 | CÔNG TY CỔ PHẦN Lisemco 5 MC | Painting steel structure | Contract: 2023-06-04
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-06-04 | ' || COALESCE(remark, '') WHERE quotation_no = 23036 AND status != 'WON';
-- 23035 | Stejasa | Cutting plan 1.4878 and AISI 409/ 7229002 VPIT Manzanillo | Contract: 2023-04-03
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-04-03 | ' || COALESCE(remark, '') WHERE quotation_no = 23035 AND status != 'WON';
-- 23034 | Stejasa | PMI Test/ 7229002 VPIT Manzanillo | Contract: 2023-04-04
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-04-04 | ' || COALESCE(remark, '') WHERE quotation_no = 23034 AND status != 'WON';
-- 23032 | VOGT POWER INTERNATIONAL | Pipe Racks/ 549 -  Manzanillo | Contract: 2023-06-04
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-06-04 | ' || COALESCE(remark, '') WHERE quotation_no = 23032 AND status != 'WON';
-- 23017 | VOGT POWER INTERNATIONAL | Base and Bearing Plates/ 550 - PT Amman | Contract: 00:00:00
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract date unknown | ' || COALESCE(remark, '') WHERE quotation_no = 23017 AND status != 'WON';
-- 23007 | Stejasa | Test post/ VPIT Manzanillo | Contract: 2023-05-04
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-05-04 | ' || COALESCE(remark, '') WHERE quotation_no = 23007 AND status != 'WON';
-- 22182 | PHB | Supply for Extra hardware/ 002047-0053 | Contract: 2022-12-17
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-12-17 | ' || COALESCE(remark, '') WHERE quotation_no = 22182 AND status != 'WON';
-- 22181 | Stejasa | Test port for Inlet Duct/ ELSAUZ TKPV | Contract: 2022-12-17
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-12-17 | ' || COALESCE(remark, '') WHERE quotation_no = 22181 AND status != 'WON';
-- 22180 | Stejasa | Supply for Liner material | Contract: 2022-12-14
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-12-14 | ' || COALESCE(remark, '') WHERE quotation_no = 22180 AND status != 'WON';
-- 22178 | JFE Engineering Corporation | Paint material for site and adjustment liner plate/ Djibouti Jetty Project | Contract: 2022-12-15
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-12-15 | ' || COALESCE(remark, '') WHERE quotation_no = 22178 AND status != 'WON';
-- 22170 | PHB | Supply of site supervision | Contract: 2022-12-17
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-12-17 | ' || COALESCE(remark, '') WHERE quotation_no = 22170 AND status != 'WON';
-- 22169 | DR (Công ty CP Cơ khí xây dựng) | Painting steel structure | Contract: 2022-11-18
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-11-18 | ' || COALESCE(remark, '') WHERE quotation_no = 22169 AND status != 'WON';
-- 22153 | Stejasa | Liner material/ 7229001 TKPV El Sauz | Contract: 2022-10-12
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-10-12 | ' || COALESCE(remark, '') WHERE quotation_no = 22153 AND status != 'WON';
-- 22146 | PHB | Supply labor and equipment to repair according to revised drawings/ SMELTER Structure | Contract: 2022-10-18
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-10-18 | ' || COALESCE(remark, '') WHERE quotation_no = 22146 AND status != 'WON';
-- 22138 | CÔNG TY TNHH NHÀ THÉP TIỀN CHẾ ZAMIL VIỆT NAM | Blasting and painting | Contract: 2022-09-19
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-09-19 | ' || COALESCE(remark, '') WHERE quotation_no = 22138 AND status != 'WON';
-- 22135 | VOGT POWER INTERNATIONAL | Structural Supports/ V17511-REQ 14716 | Contract: 2022-12-09
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-12-09 | ' || COALESCE(remark, '') WHERE quotation_no = 22135 AND status != 'WON';
-- 22134 | Stejasa | RFQ Steel Structure/ VPIT Manzanillo | Contract: 2023-01-13
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-01-13 | ' || COALESCE(remark, '') WHERE quotation_no = 22134 AND status != 'WON';
-- 22124 | Stejasa | Diverters, Guillotines, Transition silencer to Stack, Expansion Joints, Stack, Silencer/ SC2975 RFQ - Manzanillo | Contract: 2023-01-13
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2023-01-13 | ' || COALESCE(remark, '') WHERE quotation_no = 22124 AND status != 'WON';
-- 22118 | PHB | Supply material, labor and equipment to repairing according to revised drawings | Contract: 2022-09-24
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-09-24 | ' || COALESCE(remark, '') WHERE quotation_no = 22118 AND status != 'WON';
-- 22116 | Stejasa | Revised drawing and packing frame - ENP-330-21- 9 Guillotine dampers | Contract: 2022-08-12
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-08-12 | ' || COALESCE(remark, '') WHERE quotation_no = 22116 AND status != 'WON';
-- 22097 | Stejasa | Supply labor as request from Stejasa | Contract: 2022-07-18
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-07-18 | ' || COALESCE(remark, '') WHERE quotation_no = 22097 AND status != 'WON';
-- 22095 | Stejasa | Test ports - 7229001 TKPV El Sauz | Contract: 2022-08-12
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-08-12 | ' || COALESCE(remark, '') WHERE quotation_no = 22095 AND status != 'WON';
-- 22093 | CÔNG TY TNHH NHÀ THÉP TIỀN CHẾ ZAMIL VIỆT NAM | Blasting and painting | Contract: 2022-07-11
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-07-11 | ' || COALESCE(remark, '') WHERE quotation_no = 22093 AND status != 'WON';
-- 22085 | Stejasa | Storage fee of Unit 5&6 - Golden pass project | Contract: 2022-06-22
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-06-22 | ' || COALESCE(remark, '') WHERE quotation_no = 22085 AND status != 'WON';
-- 22082 | JFE Engineering Corporation | Lifting of Stringer | Contract: 2022-06-07
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-06-07 | ' || COALESCE(remark, '') WHERE quotation_no = 22082 AND status != 'WON';
-- 22067 | JFE Engineering Corporation | Anchor bolt M16 x 384 - Djibouti Jetty Project | Contract: 2022-05-25
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-05-25 | ' || COALESCE(remark, '') WHERE quotation_no = 22067 AND status != 'WON';
-- 22064 | CÔNG TY TNHH NHÀ THÉP TIỀN CHẾ ZAMIL VIỆT NAM | Labor for blasting and paiting of structure | Contract: 2022-06-13
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-06-13 | ' || COALESCE(remark, '') WHERE quotation_no = 22064 AND status != 'WON';
-- 22063 | Flsmidth A/S | Provice equipment for delivery | Contract: 2022-05-17
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-05-17 | ' || COALESCE(remark, '') WHERE quotation_no = 22063 AND status != 'WON';
-- 22047 | JFE Engineering Corporation | Design for Abjidan project | Contract: 2022-04-25
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-04-25 | ' || COALESCE(remark, '') WHERE quotation_no = 22047 AND status != 'WON';
-- 22042 | PHB | Frames Conveyors | Contract: 2022-05-05
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-05-05 | ' || COALESCE(remark, '') WHERE quotation_no = 22042 AND status != 'WON';
-- 22036 | Briese Schiffahrts GmbH & Co.KG | Tween Deck Fabrication | Contract: 2022-06-08
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-06-08 | ' || COALESCE(remark, '') WHERE quotation_no = 22036 AND status != 'WON';
-- 22027 | VERBIO Vereinigte Bio Energie AG | Fabrication of STHE & Vessels | Contract: 2022-04-29
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-04-29 | ' || COALESCE(remark, '') WHERE quotation_no = 22027 AND status != 'WON';
-- 22023 | Stejasa | Diverters, Guillotines, Duct, Transition silencer, Expansion Joints and Stack | Contract: 2022-08-12
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-08-12 | ' || COALESCE(remark, '') WHERE quotation_no = 22023 AND status != 'WON';
-- 22018 | Stejasa | Sealing air fans support | Contract: 2022-03-28
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-03-28 | ' || COALESCE(remark, '') WHERE quotation_no = 22018 AND status != 'WON';
-- 22015 | Viet Han Engineering Co., Ltd. (VHE) | Beam, Column, plate, ladder and handrail. | Contract: 2022-02-24
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-02-24 | ' || COALESCE(remark, '') WHERE quotation_no = 22015 AND status != 'WON';
-- 22012 | BFL Hydro | fabrication & machining of draft tube assembly | Contract: 2022-05-13
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-05-13 | ' || COALESCE(remark, '') WHERE quotation_no = 22012 AND status != 'WON';
-- 22010 | VERBIO Vereinigte Bio Energie AG | Design of columns 1402K001_2_3 | Contract: 2022-02-18
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-02-18 | ' || COALESCE(remark, '') WHERE quotation_no = 22010 AND status != 'WON';
-- 22006 | PHB | Transfer towers, Conveyors Supports and Belt conveyors | Contract: 2022-03-30
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-03-30 | ' || COALESCE(remark, '') WHERE quotation_no = 22006 AND status != 'WON';
-- 22003 | JFE Engineering Corporation | Fabrication for Repair F.P welding line | Contract: 2022-01-21
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-01-21 | ' || COALESCE(remark, '') WHERE quotation_no = 22003 AND status != 'WON';
-- 22002 | Stejasa | Supply of AISI 409 | Contract: 2022-02-10
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-02-10 | ' || COALESCE(remark, '') WHERE quotation_no = 22002 AND status != 'WON';
-- 21161 | Stejasa | The replacement of some pieces of the actuators | Contract: 2021-11-29
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-11-29 | ' || COALESCE(remark, '') WHERE quotation_no = 21161 AND status != 'WON';
-- 21159 | VERBIO Vereinigte Bio Energie AG | 10% spare bolts of Column | Contract: 2021-11-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-11-26 | ' || COALESCE(remark, '') WHERE quotation_no = 21159 AND status != 'WON';
-- 21151 | VERBIO Vereinigte Bio Energie AG | Fabrication of columns 1403K001_2_3 and STHE 1403W003 | Contract: 2021-12-08
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-12-08 | ' || COALESCE(remark, '') WHERE quotation_no = 21151 AND status != 'WON';
-- 21147 | Stejasa | The sealing air system, drainage system and guillotine frame support | Contract: 2021-11-19
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-11-19 | ' || COALESCE(remark, '') WHERE quotation_no = 21147 AND status != 'WON';
-- 21136 | Stejasa | Guillotine dampers | Contract: 2022-01-28
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-01-28 | ' || COALESCE(remark, '') WHERE quotation_no = 21136 AND status != 'WON';
-- 21128 | Stejasa | Supply of shaft | Contract: 2021-10-05
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-10-05 | ' || COALESCE(remark, '') WHERE quotation_no = 21128 AND status != 'WON';
-- 21124 | Stejasa | Manufacturing of Diverters, Guillotines, Duct | Contract: 2021-11-15
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-11-15 | ' || COALESCE(remark, '') WHERE quotation_no = 21124 AND status != 'WON';
-- 21109 | Stejasa | Analyzes for all the paints | Contract: 2021-10-01
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-10-01 | ' || COALESCE(remark, '') WHERE quotation_no = 21109 AND status != 'WON';
-- 21108 | JFE Engineering Corporation | Fabrication of 2 Pontoons and connecting bridges - Djibouti | Contract: 2022-04-06
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-04-06 | ' || COALESCE(remark, '') WHERE quotation_no = 21108 AND status != 'WON';
-- 21107 | VERBIO Vereinigte Bio Energie AG | Insulation of Column heat exchanger | Contract: 2021-09-21
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-09-21 | ' || COALESCE(remark, '') WHERE quotation_no = 21107 AND status != 'WON';
-- 21090 | Stejasa | Supply of bolt | Contract: 2021-07-12
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-07-12 | ' || COALESCE(remark, '') WHERE quotation_no = 21090 AND status != 'WON';
-- 21089 | Stejasa | Supply labor for additional FAT on July 05 | Contract: 2021-07-05
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-07-05 | ' || COALESCE(remark, '') WHERE quotation_no = 21089 AND status != 'WON';
-- 21085 | Stejasa | Supply of labor | Contract: 2021-06-30
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-06-30 | ' || COALESCE(remark, '') WHERE quotation_no = 21085 AND status != 'WON';
-- 21083 | VERBIO Vereinigte Bio Energie AG | Fabrication of Shims | Contract: 2021-06-23
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-06-23 | ' || COALESCE(remark, '') WHERE quotation_no = 21083 AND status != 'WON';
-- 21078 | Stejasa | Packing Item T | Contract: 2021-06-17
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-06-17 | ' || COALESCE(remark, '') WHERE quotation_no = 21078 AND status != 'WON';
-- 21077 | Stejasa | Test PMI (positive material identification) | Contract: 2021-09-22
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-09-22 | ' || COALESCE(remark, '') WHERE quotation_no = 21077 AND status != 'WON';
-- 21066 | IBS Corporation | Load Beam | Contract: 2021-06-07
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-06-07 | ' || COALESCE(remark, '') WHERE quotation_no = 21066 AND status != 'WON';
-- 21048 | JFE Engineering Corporation | Fabrication for Mock-up | Contract: 2021-05-13
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-05-13 | ' || COALESCE(remark, '') WHERE quotation_no = 21048 AND status != 'WON';
-- 21037 | RK Engineering Co.,Ltd. | shell rolling for vessel | Contract: 2022-04-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2022-04-26 | ' || COALESCE(remark, '') WHERE quotation_no = 21037 AND status != 'WON';
-- 21033 | DR (Công ty CP Cơ khí xây dựng) | Supply labor for painting | Contract: 2021-04-03
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-04-03 | ' || COALESCE(remark, '') WHERE quotation_no = 21033 AND status != 'WON';
-- 21031 | Stejasa | Supply tarpaulins support | Contract: 2021-03-30
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-03-30 | ' || COALESCE(remark, '') WHERE quotation_no = 21031 AND status != 'WON';
-- 21028 | DR (Công ty CP Cơ khí xây dựng) | Supply labor for painting | Contract: 2021-03-20
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-03-20 | ' || COALESCE(remark, '') WHERE quotation_no = 21028 AND status != 'WON';
-- 21027 | JFE Engineering Corporation | Structural steel fabrication for Jamuna in Bangladesh | Contract: 2021-04-28
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-04-28 | ' || COALESCE(remark, '') WHERE quotation_no = 21027 AND status != 'WON';
-- 21018 | VERBIO Vereinigte Bio Energie AG | Fabrication of Column heat exchanger | Contract: 2021-04-30
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-04-30 | ' || COALESCE(remark, '') WHERE quotation_no = 21018 AND status != 'WON';
-- 21012 | CÔNG TY TNHH TM XÂY DỰNG VẬT TẢI PHƯƠNG ĐÔNG | Supply labor for bending Pl50 | Contract: 2021-01-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-01-26 | ' || COALESCE(remark, '') WHERE quotation_no = 21012 AND status != 'WON';
-- 21010 | Stejasa | Supply of packing material for the sealing air pipes | Contract: 2021-02-25
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-02-25 | ' || COALESCE(remark, '') WHERE quotation_no = 21010 AND status != 'WON';
-- 21002 | DR (Công ty CP Cơ khí xây dựng) | Supply labor for painting | Contract: 2021-01-05
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-01-05 | ' || COALESCE(remark, '') WHERE quotation_no = 21002 AND status != 'WON';
-- 20134 | DR (Công ty CP Cơ khí xây dựng) | Supply labor for painting | Contract: 2020-12-16
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-12-16 | ' || COALESCE(remark, '') WHERE quotation_no = 20134 AND status != 'WON';
-- 20132 | Stejasa | Manufacturing for items of the revised drawing. | Contract: 2020-12-15
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-12-15 | ' || COALESCE(remark, '') WHERE quotation_no = 20132 AND status != 'WON';
-- 20130 | DR (Công ty CP Cơ khí xây dựng) | Labor for paint | Contract: 2020-12-09
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-12-09 | ' || COALESCE(remark, '') WHERE quotation_no = 20130 AND status != 'WON';
-- 20125 | DR (Công ty CP Cơ khí xây dựng) | Bending plate | Contract: 2020-12-02
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-12-02 | ' || COALESCE(remark, '') WHERE quotation_no = 20125 AND status != 'WON';
-- 20122 | DR (Công ty CP Cơ khí xây dựng) | Labor for paint | Contract: 2020-11-27
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-11-27 | ' || COALESCE(remark, '') WHERE quotation_no = 20122 AND status != 'WON';
-- 20121 | DR (Công ty CP Cơ khí xây dựng) | Labor for paint | Contract: 2020-12-02
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-12-02 | ' || COALESCE(remark, '') WHERE quotation_no = 20121 AND status != 'WON';
-- 20118 | DR (Công ty CP Cơ khí xây dựng) | Labor for paint | Contract: 2020-11-23
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-11-23 | ' || COALESCE(remark, '') WHERE quotation_no = 20118 AND status != 'WON';
-- 20117 | Stejasa | TANDEM DAMPERS | Contract: 2020-11-30
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-11-30 | ' || COALESCE(remark, '') WHERE quotation_no = 20117 AND status != 'WON';
-- 20116 | Stejasa | Test PMI (positive material identification) | Contract: 2020-12-01
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-12-01 | ' || COALESCE(remark, '') WHERE quotation_no = 20116 AND status != 'WON';
-- 20115 | Kawakin Core-Tech Vietnam Co., Ltd. | Supply material for trial fabrication | Contract: 2020-12-01
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-12-01 | ' || COALESCE(remark, '') WHERE quotation_no = 20115 AND status != 'WON';
-- 20113 | Stejasa | STACK DAMPER | Contract: 2021-06-24
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-06-24 | ' || COALESCE(remark, '') WHERE quotation_no = 20113 AND status != 'WON';
-- 20112 | DR (Công ty CP Cơ khí xây dựng) | Labor for paint | Contract: 2020-11-14
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-11-14 | ' || COALESCE(remark, '') WHERE quotation_no = 20112 AND status != 'WON';
-- 20111 | Stejasa | Supply material and fabrication of Check Valve | Contract: 2021-03-09
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2021-03-09 | ' || COALESCE(remark, '') WHERE quotation_no = 20111 AND status != 'WON';
-- 20110 | IBS Corporation | Frame for load test | Contract: 2020-10-27
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-10-27 | ' || COALESCE(remark, '') WHERE quotation_no = 20110 AND status != 'WON';
-- 20109 | Cơ khí Hà nội | Roller | Contract: 2020-10-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-10-26 | ' || COALESCE(remark, '') WHERE quotation_no = 20109 AND status != 'WON';
-- 20108 | Woahoo Energy | Fabrication Boom | Contract: 2020-10-23
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-10-23 | ' || COALESCE(remark, '') WHERE quotation_no = 20108 AND status != 'WON';
-- 20106 | Stejasa | Supply material and fabrication | Contract: 2020-10-09
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-10-09 | ' || COALESCE(remark, '') WHERE quotation_no = 20106 AND status != 'WON';
-- 20105 | Stejasa | Supply  material | Contract: 2020-10-01
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-10-01 | ' || COALESCE(remark, '') WHERE quotation_no = 20105 AND status != 'WON';
-- 20098 | Yokogawa Bridge Corp. | Cost for delay delivery | Contract: 2020-10-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-10-26 | ' || COALESCE(remark, '') WHERE quotation_no = 20098 AND status != 'WON';
-- 20097 | Yokogawa Bridge Corp. | Box fabrication | Contract: 2020-10-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-10-26 | ' || COALESCE(remark, '') WHERE quotation_no = 20097 AND status != 'WON';
-- 20089 | Tân Phong | Báo giá bổ sung | Contract: 2020-09-08
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-09-08 | ' || COALESCE(remark, '') WHERE quotation_no = 20089 AND status != 'WON';
-- 20078 | Quin Right Enterprises Pte Ltd | Fabricate head of tanks, CIF | Contract: 2020-09-11
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-09-11 | ' || COALESCE(remark, '') WHERE quotation_no = 20078 AND status != 'WON';
-- 20077 | Stejasa | Fabricate 10 sets of Diverter | Contract: 2020-11-13
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-11-13 | ' || COALESCE(remark, '') WHERE quotation_no = 20077 AND status != 'WON';
-- 20072 | Stejasa | Supply bolt, washer, bracket … | Contract: 2020-08-07
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-08-07 | ' || COALESCE(remark, '') WHERE quotation_no = 20072 AND status != 'WON';
-- 20070 | Tân Phong | Fabricate the pipe for Filter | Contract: 2020-08-04
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-08-04 | ' || COALESCE(remark, '') WHERE quotation_no = 20070 AND status != 'WON';
-- 20068 | Yokogawa Bridge Corp. | Supply cable and shackle | Contract: 2020-10-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-10-26 | ' || COALESCE(remark, '') WHERE quotation_no = 20068 AND status != 'WON';
-- 20065 | Stejasa | Manpower for repair of Stejasa brokend product | Contract: 2020-08-28
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-08-28 | ' || COALESCE(remark, '') WHERE quotation_no = 20065 AND status != 'WON';
-- 20062 | Tân Phong | Fabricate steel structure for Dust Filter | Contract: 2020-08-01
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-08-01 | ' || COALESCE(remark, '') WHERE quotation_no = 20062 AND status != 'WON';
-- 20057 | Stejasa | Quotation for repare | Contract: 2020-10-05
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-10-05 | ' || COALESCE(remark, '') WHERE quotation_no = 20057 AND status != 'WON';
-- 20055 | Yokogawa Bridge Corp. | Kalna Bridge Lifting device | Contract: 2020-10-26
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-10-26 | ' || COALESCE(remark, '') WHERE quotation_no = 20055 AND status != 'WON';
-- 20032 | Stejasa | Manufacture and Installation of 10 Test Ports | Contract: 2020-06-06
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-06-06 | ' || COALESCE(remark, '') WHERE quotation_no = 20032 AND status != 'WON';
-- 20030 | Yokogawa Bridge Corp. | Hanger Piece for Girder and Cutting Splice Plates | Contract: 2020-07-13
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-07-13 | ' || COALESCE(remark, '') WHERE quotation_no = 20030 AND status != 'WON';
-- 20029 | Yokogawa Bridge Corp. | Fabricate for Stiffening Girder | Contract: 2020-07-13
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-07-13 | ' || COALESCE(remark, '') WHERE quotation_no = 20029 AND status != 'WON';
-- 20025 | Stejasa | Manufacturing of 6 Diverters and 6 Guillotines | Contract: 2020-08-25
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-08-25 | ' || COALESCE(remark, '') WHERE quotation_no = 20025 AND status != 'WON';
-- 20013 | Yokogawa Bridge Corp. | Specimens of field welding procedure | Contract: 2020-04-07
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-04-07 | ' || COALESCE(remark, '') WHERE quotation_no = 20013 AND status != 'WON';
-- 20012 | Agrimeco Jsc | Manpower to install bolts and paint buttom pannels | Contract: 2019-09-06
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2019-09-06 | ' || COALESCE(remark, '') WHERE quotation_no = 20012 AND status != 'WON';
-- 20004 | Stejasa | Diverter, Guillotine, Transition, Expansion Joints, Stack, Silencer, Structure | Contract: 2020-03-23
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-03-23 | ' || COALESCE(remark, '') WHERE quotation_no = 20004 AND status != 'WON';
-- 20002 | Macgregor Norway As. | Gear box housing, shaft & center | Contract: 2020-02-14
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-02-14 | ' || COALESCE(remark, '') WHERE quotation_no = 20002 AND status != 'WON';
-- 20001 | Agrimeco Jsc | Lashing work for container | Contract: 2020-03-20
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-03-20 | ' || COALESCE(remark, '') WHERE quotation_no = 20001 AND status != 'WON';
-- 19039 | Macgregor Norway As. | Gear box housing, shaft & center | Contract: 2019-07-04
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2019-07-04 | ' || COALESCE(remark, '') WHERE quotation_no = 19039 AND status != 'WON';
-- 19038 | Dong Bac Shipbuilding Industry Jsc | Barges Project | Contract: 2019-10-29
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2019-10-29 | ' || COALESCE(remark, '') WHERE quotation_no = 19038 AND status != 'WON';
-- 19037 | Yokogawa Bridge Corp. | Fabrication, trial assembly, painting, packing and delivery | Contract: 2019-08-15
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2019-08-15 | ' || COALESCE(remark, '') WHERE quotation_no = 19037 AND status != 'WON';
-- 19022 | Agrimeco Jsc | Supply labor, consumable for repair work. | Contract: 2019-09-06
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2019-09-06 | ' || COALESCE(remark, '') WHERE quotation_no = 19022 AND status != 'WON';
-- 19017 | Yokogawa Bridge Corp. | Supply of labor, consumable for fabricate additionally 44 hanger pieces for site erection. | Contract: 2020-01-30
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-01-30 | ' || COALESCE(remark, '') WHERE quotation_no = 19017 AND status != 'WON';
-- 19015 | Yokogawa Bridge Corp. | Supply labor for drilling 44 cable holes | Contract: 2020-01-30
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-01-30 | ' || COALESCE(remark, '') WHERE quotation_no = 19015 AND status != 'WON';
-- 19014 | Yokogawa Bridge Corp. | Supply labor, consumable for welding stiffeners | Contract: 2020-01-30
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-01-30 | ' || COALESCE(remark, '') WHERE quotation_no = 19014 AND status != 'WON';

-- Total: 184 UPDATE statements for won contracts (skipped 2 invalid)

-- Verification
-- SELECT 'Won contracts updated: ' || changes();
-- 19010 | Yokogawa Bridge Corp. | Supply Nuts and consumable materials labor (manual fix - multiline source)
UPDATE sale_quotation_history SET status = 'WON', remark = '[WON] Contract: 2020-01-30 | ' || COALESCE(remark, '') WHERE quotation_no = 19010 AND status != 'WON';
