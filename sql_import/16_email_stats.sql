-- sale_customers UPDATE (enrich with mbox email statistics)
-- Generated: 2026-04-29 07:06:15
-- Records: 39 existing customers enriched with mbox engagement data
-- Source: customers.json (ibshi@ibs.com.vn mbox export, 40,122 messages)

-- JFE: JFE Engineering Corporation (8155 msgs across 10 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 8155 msgs, 2271 threads, 2019-12-10 to 2026-02-13 (jfe-eng.co.jp, jfe-bd.com, mail.jfe-eng.com, mm.jfe-eng.com, tm.jfe-eng.co.jp, jfe-eng.com.ph, jfe-shoji.com.vn, jfe-shoji.co.jp, jfe-steel.co.jp, vn.jfe-eng.com)' WHERE id = '6d7154218cfc43';

-- BRA: Braden-Europe B.V (5696 msgs across 5 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 5696 msgs, 1616 threads, 2020-03-06 to 2026-04-21 (aafintl.com, braden.com, aafgb.com, aaf.es, aafsa.es)' WHERE id = 'ce3934334dc841';

-- VPI: VOGT POWER INTERNATIONAL (5372 msgs across 4 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 5372 msgs, 1740 threads, 2022-02-05 to 2026-04-22 (vogtpower.com, babcockpower.com, notes.babcockpower.com, babcock.com)' WHERE id = '5b8a1ce4141c44';

-- VER: VERBIO Vereinigte Bio Energie AG (1965 msgs across 2 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 1965 msgs, 386 threads, 2021-02-20 to 2025-10-20 (verbio.de, verbio.us)' WHERE id = '433f99eca0d841';

-- SED: Siempelkamp Energy Drying Solutions (863 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 863 msgs, 198 threads, 2024-10-28 to 2026-04-18 (siempelkamp.com)' WHERE id = 'db8e68470f7f45';

-- WNC: Wendt-Noise Control GMBH (703 msgs across 2 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 703 msgs, 205 threads, 2024-12-19 to 2026-04-22 (wendt-noise-control.de, wendt-sit.de)' WHERE id = 'bb8fc90583f843';

-- LSC5: CÔNG TY CỔ PHẦN Lisemco 5 MC (606 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 606 msgs, 246 threads, 2020-03-25 to 2026-03-12 (lisemco.com.vn)' WHERE id = '4dc4927404c046';

-- SHI: SHINWA ENGINEERING CO.,LTD (421 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 421 msgs, 120 threads, 2022-12-26 to 2026-03-17 (shinwa-engineer.co.jp)' WHERE id = 'b8faee2239df4b';

-- KCC: KC Cottrell (410 msgs across 3 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 410 msgs, 95 threads, 2021-12-21 to 2025-12-15 (kc-cottrell.com, kc-cottrell.com.vn, kccottrell-es.com)' WHERE id = '64875fc252cf40';

-- MSA: Metso Australia Pty Ltd (388 msgs across 2 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 388 msgs, 108 threads, 2021-12-01 to 2026-04-20 (mogroup.com, metso.com)' WHERE id = 'e772c31f715446';

-- TKPV: Thyssenkrupp Polysius (Vietnam) Ltd (337 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 337 msgs, 124 threads, 2020-02-17 to 2026-03-23 (thyssenkrupp.com)' WHERE id = 'ba90702e6dcb4a';

-- JFEI: JFE Engineering Corporation (317 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 317 msgs, 71 threads, 2020-12-21 to 2025-04-08 (jfe-eng.co.in)' WHERE id = '8adc2c388a7745';

-- HTE: Hamon Thermal Europe, S.A. (277 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 277 msgs, 118 threads, 2020-07-30 to 2025-12-15 (hamon.com)' WHERE id = '65862a2e99e44e';

-- JCE: John Cockerill Energy (236 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 236 msgs, 69 threads, 2020-02-15 to 2026-04-01 (johncockerill.com)' WHERE id = 'af142d441ee345';

-- YBC: Yokogawa Bridge Corp. (215 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 215 msgs, 44 threads, 2020-02-21 to 2026-03-16 (yokogawa-bridge.co.jp)' WHERE id = '908f6584e87848';

-- GEA: GEA Bischoff GmbH (206 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 206 msgs, 30 threads, 2021-08-09 to 2026-03-26 (gea.com)' WHERE id = 'c42773f4293946';

-- BNE: Büttner Energy (183 msgs across 2 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 183 msgs, 28 threads, 2021-06-01 to 2026-02-23 (drewes-group.com, buettner-energy-dryer.com)' WHERE id = 'da2242c845e540';

-- SPG: SPG DRY COOLING BELGIUM (173 msgs across 2 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 173 msgs, 59 threads, 2019-11-12 to 2026-02-18 (spgdrycooling.com, spg-steiner.com)' WHERE id = '0d3caef234bb48';

-- WEL: WAHOO ENERGY LLC (137 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 137 msgs, 43 threads, 2020-09-14 to 2025-02-13 (wahooenergy.com)' WHERE id = '1a2d7b3da19b42';

-- Tak: Takraf India (113 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 113 msgs, 46 threads, 2020-12-22 to 2025-06-10 (takraf.com)' WHERE id = 'aae1cd9d64344b';

-- HLS: CÔNG TY TNHH MTV ĐÓNG TÀU HẠ LONG (94 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 94 msgs, 26 threads, 2024-11-09 to 2025-12-17 (hlsy.com.vn)' WHERE id = 'e7d8d681c8b344';

-- VH: CÔNG TY CỔ PHẦN CÔNG NGHIỆP VIỆT HẢI (94 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 94 msgs, 23 threads, 2021-11-29 to 2023-09-22 (vhe.com.vn)' WHERE id = 'fc1076c996864c';

-- DSCS: Damen Song Cam Shipyard (75 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 75 msgs, 24 threads, 2024-06-25 to 2025-12-29 (damen.com)' WHERE id = 'e7afb9ebc5f545';

-- VISC: Công ty cổ phần vận tải biển VISC (73 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 73 msgs, 42 threads, 2019-12-05 to 2025-03-20 (visc-shipping.com)' WHERE id = 'b1eabbb9143a4e';

-- DEC: Daewoo Engineering & Construction Co., Ltd. (71 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 71 msgs, 26 threads, 2024-03-26 to 2025-12-15 (daewooenc.com)' WHERE id = '6ce18c0c27c542';

-- KMH: Komaihaltec Inc. (67 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 67 msgs, 24 threads, 2020-12-21 to 2025-12-15 (komaihaltec.co.jp)' WHERE id = '0afaece1faf24d';

-- NEM: NEM Energy BV (55 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 55 msgs, 19 threads, 2022-11-30 to 2026-03-25 (nem-energy.com)' WHERE id = '334b9740b9c24a';

-- BRU: Brucks Siwertell (51 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 51 msgs, 14 threads, 2024-09-18 to 2026-03-17 (bruks-siwertell.com)' WHERE id = '668da959559a46';

-- PEJ: Peja Vietnam Co.,Ltd (45 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 45 msgs, 7 threads, 2024-06-18 to 2025-05-22 (pejavietnam.com)' WHERE id = '18bd36d3193545';

-- BII: Bachmann (43 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 43 msgs, 7 threads, 2025-01-29 to 2026-04-14 (bachmannusa.com)' WHERE id = '15fc57e9695b49';

-- GON: Gonnix Engineering (40 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 40 msgs, 11 threads, 2025-09-03 to 2026-04-22 (gonnix.com)' WHERE id = '6e72843f1524c4';

-- STF: STF Loterios S.r.l. (34 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 34 msgs, 11 threads, 2024-10-21 to 2025-02-19 (stf-loterios.com)' WHERE id = 'f9db1f7bd5c24b';

-- WGY: Woo Gyeong Co., Ltd (33 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 33 msgs, 7 threads, 2025-04-10 to 2026-01-26 (woogyeong.kr)' WHERE id = '40ab64e7515a4f';

-- KHPT: KHPT Co., LTD. (31 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 31 msgs, 13 threads, 2025-08-20 to 2026-04-06 (khpetro.com)' WHERE id = '641131c5b70746';

-- FEL: Fortafric Energy Limited (29 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 29 msgs, 7 threads, 2024-11-11 to 2025-05-12 (fortafric.com)' WHERE id = '9c58961482c442';

-- IEV: Idemitsu Engineering Vietnam (25 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 25 msgs, 6 threads, 2022-05-26 to 2025-09-10 (idemitsu.com)' WHERE id = '69e0ab99f3884f';

-- SAI: Société d’Acoustique Industrielle (17 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 17 msgs, 4 threads, 2025-09-27 to 2026-01-29 (saifrance.com)' WHERE id = 'e9bd98e0352e4e';

-- IWT: IWT-MOLDRUP ASIA PACIFIC PROCUREMENT AND SALES (15 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 15 msgs, 4 threads, 2025-07-01 to 2025-12-15 (moldrup.com)' WHERE id = '1363a3c3a07b44';

-- OCI: Công ty Cổ Phần Công nghiệp Đại Dương (11 msgs across 1 domains)
UPDATE sale_customers SET business_description = COALESCE(business_description, '') || ' | ' || '[MBOX] 11 msgs, 1 threads, 2025-05-23 to 2025-06-19 (oci.com.vn)' WHERE id = 'e4dac2be404f4e';

