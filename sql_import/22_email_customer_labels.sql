-- ═══════════════════════════════════════════════════════════
-- 22_email_customer_labels.sql
-- Source: ibshi@ibs.com.vn Gmail labels 2026-04-29 10:11:33
-- Customer relationship labels from organized email folders
-- ═══════════════════════════════════════════════════════════

-- === EMAIL CUSTOMER LABELS (enrichment for sale_customers) ===
CREATE TABLE IF NOT EXISTS sale_email_labels (
    id              TEXT PRIMARY KEY,
    label_name      TEXT NOT NULL,
    conversation_count INTEGER DEFAULT 0,
    customer_id     TEXT REFERENCES sale_customers(id),
    source          TEXT DEFAULT 'Gmail labels ibshi@',
    created_at      TEXT DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-9088d5ed', 'BAKE HUGHES', 1);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-12495cb8', 'BILFINGER engineering & technologies', 8);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-b98a97a8', 'BOLDROCCHI', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-4be5b88d', 'Briese shipping', 39);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-4d60e9af', 'Briese Oteco 9000', 1);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-46f5ae70', 'CECO', 3);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-c666aa2e', 'DNV', 1);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-7ded2823', 'EVAPCO', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-88143ad8', 'FAM Materials handling system', 3);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-a49b81f7', 'FINNSEA', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-95bd7168', 'GEA', 7);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-c470a7d2', 'GLOBAL HYDRO ENERGY', 5);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-891e2fe6', 'GUGLER WATER TURBINES', 1);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-140cde24', 'HAMON VN', 1);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-f189ef8f', 'HITACHI ZOSEN INOVA AG', 5);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-a70e79d0', 'INVESTNET', 3);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-5b890a21', 'JFE INDIA', 13);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-26aede54', 'JFE INDIA (2)', 4);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-b6190152', 'JFE JP', 36);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-d26349d2', 'JFE Myanmar', 1);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-2ec14054', 'JFE PHILIPINES', 12);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-2b819c0b', 'John Cockerill', 4);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-d374e40d', 'KIRCHNER Italy', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-62dbe1c0', 'Komaihaltec', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-26f43b30', 'MAc Gregor - TWD outfitting', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-c2f36734', 'MacGregor Norway AS', 1);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-44d52490', 'MIHO', 11);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-a02ad35c', 'Mitsubishi Power', 1);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-9394f610', 'Mitsui miike', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-4a7d2fb3', 'NIPPON STEEL', 3);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-32d78539', 'PHB indonesia project', 14);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-3d36aa89', 'Prodesa', 1);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-088b5372', 'REEL MOLLER', 3);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-115333eb', 'Saskarc', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-909585c4', 'SCHADE', 7);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-4f40996c', 'Siemens Germany', 6);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-31a63434', 'siemens Holland', 5);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-b6d87190', 'SMS group, Paul Wurth', 9);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-9569c5da', 'STEJASA', 42);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-da81aaf5', 'Stejasa audit', 7);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-8e53e8ce', 'TAIM WESER', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-8ad13b72', 'TAKRAF- USA', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-889bde32', 'TENOVA italy', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-f9d92a89', 'Tokyu', 2);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-2dee26ad', 'UPTIME', 7);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-a9191864', 'VERBIO', 5);
INSERT OR IGNORE INTO sale_email_labels (id, label_name, conversation_count)
  VALUES ('label-b476e8b9', 'VPI audit', 3);