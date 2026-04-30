-- ═══════════════════════════════════════════════════════════
-- 25_client_visits.sql
-- Source: Client_Data_Base → Client Visit Schedule sheet
-- Generated: 2026-04-29 13:16:04
-- 149 client visits (Oct 2022 – Apr 2026)
-- Maps to: sale_customer_interactions (interaction_type = 'CLIENT_VISIT')
-- ═══════════════════════════════════════════════════════════

INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-95dd0ba9', 'Hai Phong Sicience Technology Development Center coopearte with KITA (Kitakyushu International Techn', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-a5da52a2', 'OTJ', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-e00b6594', 'KC COTTRELL', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-982e3910', 'Canadian Customer', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-e16d6563', 'OCI', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-aebccec3', 'Ortsted', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-c87876c7', 'TAIF', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-fb1939d8', 'Hyundai', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-4704b45c', 'Cargobull', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-9bedf01c', 'Embassy of the Isalamic Republic of Iran in Hanoi', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-2f075ba1', 'SLB', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-a7f1a0fe', 'G.P.S', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-bd3867f4', 'Wendt-Noise Control GMBH', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-7585a9d6', 'Tei', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-787f6486', 'Moldrup', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-3a057128', 'Gonnix', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-65524eec', 'Orbia Fluor & Energy Materials', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-8b96c5fb', 'KHPT Co.,Ltd', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
INSERT OR IGNORE INTO sale_customers (id, name, status, business_description)
  VALUES ('cdb-0e843ba0', 'Bachmann Industries, Inc', 'ACTIVE', 'Visit-only customer from CDB Client Visit Schedule');
-- 19 visit-only customers added

-- === CLIENT VISITS → sale_customer_interactions ===

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-1727bdfc', 'cdb-8cacf571', 'CLIENT_VISIT', '2022-10-25', 'IBS HI Factory', 'DINH NGOC THANG & HIS CLIENT FROM KUENZ CRANE COMPANY', 'Client Visit: VISC', 'Attendees: DINH NGOC THANG & HIS CLIENT FROM KUENZ CRANE COMPANY | Purpose: Greetings and shoptour', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-9709e3ad', 'cdb-95dd0ba9', 'CLIENT_VISIT', '2022-10-25', 'IBS HI Factory', '1. Mr Rie Ozono, Manager of Trade & Investment Team
  2. Mr Naomi Sasaki, Assistant Manager of Trade and Investment Team
  3. Mr Toshikatsu Miyata, Senior Technical Expert
  4. Ms Hioshi Emoto, Senior', 'Client Visit: Hai Phong Sicience Technology Development Center coopearte with KITA (Kitakyushu International Techno-cooperative Assosiation)', 'Attendees: 1. Mr Rie Ozono, Manager of Trade & Investment Team
  2. Mr Naomi Sasaki, Assistant Manager of Trade and Investment Team
  3. Mr Toshikatsu Miyata, Senior Technical Expert
  4. Ms Hioshi Emoto, Senior | Purpose: Greetings and shoptour', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-22f801af', 'cdb-bf58d0c8', 'CLIENT_VISIT', '2022-26-12', 'IBS HI Factory', 'Mr Ivan Group Manufacturing Manager
  Ms Paula Project Manager', 'Client Visit: AAF/Stejasa', 'Attendees: Mr Ivan Group Manufacturing Manager
  Ms Paula Project Manager | Purpose: Factory survey, checking on status of EL Sauz project and technical clarification.', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-e4f21597', 'cdb-c40da0fc', 'CLIENT_VISIT', '2022-01-11', 'IBS HI Factory', 'Mr Toyosei Aota, Engineering Manager
  Mr Naoki Hiruta, Design Engineer
  Mr Kohei Sato, Deputy Manager
  Mr Keita Nakano, SCM Engineer
  Ms Momoko Hayashi, Procurement
  Mr Takehiro Fujiki, Deputy Ma', 'Client Visit: MHI', 'Attendees: Mr Toyosei Aota, Engineering Manager
  Mr Naoki Hiruta, Design Engineer
  Mr Kohei Sato, Deputy Manager
  Mr Keita Nakano, SCM Engineer
  Ms Momoko Hayashi, Procurement
  Mr Takehiro Fujiki, Deputy Ma | Purpose: Factory Survey and Technical Clarification. Dicsussed on Lub Oil Storage on machining of flange after fully constructed.', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-8a24154e', 'cdb-46241fe2', 'CLIENT_VISIT', '2022-01-11', 'IBS HI Factory', 'Mr. Yamagishi Kazuya / PMO, Senior General Manager (JFE Engineering Corp)
  Mr. Shiobara Sadayuki / Head of Project Management Office (JFE Engineering Corp)
  Mr. Ohara Takanobu / General Director (JF', 'Client Visit: JFE', 'Attendees: Mr. Yamagishi Kazuya / PMO, Senior General Manager (JFE Engineering Corp)
  Mr. Shiobara Sadayuki / Head of Project Management Office (JFE Engineering Corp)
  Mr. Ohara Takanobu / General Director (JF | Purpose: Greetings and shoptour', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-5a8a6db8', 'cdb-40049d0c', 'CLIENT_VISIT', '2022-01-11', 'IBS HI Factory', 'Mr& Mrs Kraft', 'Client Visit: KCI- Kraft Consulting Inc', 'Attendees: Mr& Mrs Kraft | Purpose: Greetings and shoptour', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-e865766d', 'cdb-65f486e6', 'CLIENT_VISIT', '2022-11-16', 'IBS HI Factory', 'Mr. Le Dung Phuoc, Sales Manager', 'Client Visit: GEA', 'Attendees: Mr. Le Dung Phuoc, Sales Manager | Purpose: Greetings and shoptour', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-86ef2ec4', 'cdb-e7e111b8', 'CLIENT_VISIT', '2022-11-17', 'IBS HI Factory', 'Mr. Jimmy Oh
  Mr. Kyoung Bea Jang', 'Client Visit: NOAH Auctuation', 'Attendees: Mr. Jimmy Oh
  Mr. Kyoung Bea Jang | Purpose: Greetings and shoptour', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-3e33a5bb', 'cdb-bf58d0c8', 'CLIENT_VISIT', '2022-29-11', 'IBS HI Factory', 'Mr. Hastings David', 'Client Visit: AAF/Stejasa', 'Attendees: Mr. Hastings David | Purpose: HSE Audit for Air Filtering System.', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-2e29d9eb', 'cdb-a5da52a2', 'CLIENT_VISIT', '2022-01-12', 'IBS HI Factory', 'Mr. Shimizu
  Mr. Matsunaga', 'Client Visit: OTJ', 'Attendees: Mr. Shimizu
  Mr. Matsunaga | Purpose: the final measurement and others, and visit your factory also.', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-f1d23c6b', 'cdb-46241fe2', 'CLIENT_VISIT', '2022-02-12', 'IBS HI Factory', 'Mr. Mr. Nomura (Group Manager)
  Mr. Kang (Project Procurement Manager) 
  Mr. Jun Takahashi, Project Procurement Manager
  Procurement Sector – Overseas Project Department – Project Procurement Group', 'Client Visit: JFE', 'Attendees: Mr. Mr. Nomura (Group Manager)
  Mr. Kang (Project Procurement Manager) 
  Mr. Jun Takahashi, Project Procurement Manager
  Procurement Sector – Overseas Project Department – Project Procurement Group | Purpose: Greetings and shoptour
  Dinner => car to airport', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-ec461673', 'cdb-46241fe2', 'CLIENT_VISIT', '2022-05-12', 'IBS HI Factory', 'Mr. Koeda Takeshi
  Mr. Doi', 'Client Visit: JFE', 'Attendees: Mr. Koeda Takeshi
  Mr. Doi | Purpose: explain the project outline and confirm schedule and cost for Mombasa project=> Xin xe đón từ HN ngày cn 04.12', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-d3d95798', 'cdb-4cd74147', 'CLIENT_VISIT', '2022-07-12', 'IBS HI Factory', 'Mr. Noda, Mr Koga, Mr. Ichiki and Mr. Imatomi', 'Client Visit: Mitsui Miike Japan', 'Attendees: Mr. Noda, Mr Koga, Mr. Ichiki and Mr. Imatomi | Purpose: Greetings and shoptour', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-688bccbe', 'cdb-46241fe2', 'CLIENT_VISIT', '2022-08-12', 'IBS HI Factory', 'Valin: 2 members
  -JFE Shoji Hanoi: Ms. Osaka. Ms. Tram', 'Client Visit: JFE Shoji anJFE SHOJI VIETNAM CO., LTD - Hanoi Branchd &Valin', 'Attendees: Valin: 2 members
  -JFE Shoji Hanoi: Ms. Osaka. Ms. Tram | Purpose: Greetings and shoptour', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-47fde1bf', 'cdb-27c6f3df', 'CLIENT_VISIT', '2022-15-12', 'IBS HI Factory', 'Anand Palki, Director of Design Engineering
  Kumar Gopathi, Chief Sourcing Officer - BP', 'Client Visit: Babcock Power (Thailand)/ VOGT Power International (VPI)', 'Attendees: Anand Palki, Director of Design Engineering
  Kumar Gopathi, Chief Sourcing Officer - BP | Purpose: Greetings and shoptour', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-d4dee58d', 'cdb-e00b6594', 'CLIENT_VISIT', '2022-12-22', 'IBS HI Factory', 'Mr. Hoonsang Cho- Projetc manager
  Mr. Sung Kwon Kim - Engineering Manager
  Mr. Yong Soo Choi- Main mechanical engineer', 'Client Visit: KC COTTRELL', 'Attendees: Mr. Hoonsang Cho- Projetc manager
  Mr. Sung Kwon Kim - Engineering Manager
  Mr. Yong Soo Choi- Main mechanical engineer | Purpose: Greetings shoptour and discuss about new project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-6387cbbb', 'cdb-c9456437', 'CLIENT_VISIT', '2023-12-01', 'IBS HI Factory', 'Mr. Woojin- quality inspector/Quality assurance/control CWI/CSWIP
  MR. Vu Xuan Thang', 'Client Visit: SCHADE', 'Attendees: Mr. Woojin- quality inspector/Quality assurance/control CWI/CSWIP
  MR. Vu Xuan Thang | Purpose: Audit', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-4c2e55d5', 'cdb-55bd9d37', 'CLIENT_VISIT', '2023-18-01', 'IBS HI Factory', 'Mr. Gary Hansen- Quality Director
  MR. Henry Schlee- Senior quality engineer
  MR. Hohn Berra- Manager of Manufacturing Asia
  MR. Ittichet Saitin- QC manager', 'Client Visit: VPI - Babcock Power (Thailand)/ VOGT Power International (VPI)', 'Attendees: Mr. Gary Hansen- Quality Director
  MR. Henry Schlee- Senior quality engineer
  MR. Hohn Berra- Manager of Manufacturing Asia
  MR. Ittichet Saitin- QC manager | Purpose: have a Pre-Fabrication meeting for Manzanillo Damper.', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-d3a78eb6', 'cdb-9bb16045', 'CLIENT_VISIT', '2023-01-02', 'IBS HI Factory', 'Mr. Ito', 'Client Visit: YBC', 'Attendees: Mr. Ito | Purpose: meeting to discuss new project-Balu River Bridge_Fabrication schedule | Follow-up: Online meeting', 'Follow-up required', 'Online meeting', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-687e1af1', 'cdb-982e3910', 'CLIENT_VISIT', '2023-02-02', 'IBS HI Factory', 'Mr. Stephane', 'Client Visit: Canadian Customer', 'Attendees: Mr. Stephane | Purpose: To discuss about potential projects | Follow-up: Online meeting', 'Follow-up required', 'Online meeting', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-3a2af118', 'cdb-46241fe2', 'CLIENT_VISIT', '2023-02-04', 'IBS HI Factory', 'Mr. Matsugana. Ms. Edo', 'Client Visit: JFE engineering Japan', 'Attendees: Mr. Matsugana. Ms. Edo | Purpose: To discuss about 10% warranty bond… | Follow-up: Online meeting', 'Follow-up required', 'Online meeting', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-f2fe8260', 'cdb-982e3910', 'CLIENT_VISIT', '2023-09-02', 'IBS HI Factory', 'Mr. Stephane and his customer Mr. Ed Cote', 'Client Visit: Canadian Customer', 'Attendees: Mr. Stephane and his customer Mr. Ed Cote | Purpose: Discuss new projects | Follow-up: Online meeting', 'Follow-up required', 'Online meeting', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-beb8f20c', 'cdb-799d129e', 'CLIENT_VISIT', '2023-09-02', 'IBS HI Factory', 'Mitui Miike, Shinwa Vietnam and Shinwa Japan', 'Client Visit: Shinwa ( Mitsui Miike)', 'Attendees: Mitui Miike, Shinwa Vietnam and Shinwa Japan | Purpose: To discuss about some general sepecification | Follow-up: Online meeting 1', 'Follow-up required', 'Online meeting 1', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-c8ef1d62', 'cdb-e16d6563', 'CLIENT_VISIT', '2023-15-09', 'IBS HI Factory', 'Mr. Seongjun Park', 'Client Visit: OCI', 'Attendees: Mr. Seongjun Park | Purpose: Dis cuss about potential project and shoptour', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-a0742c1f', 'cdb-799d129e', 'CLIENT_VISIT', '2023-17-02', 'IBS HI Factory', 'Mr. Đức', 'Client Visit: Shinwa P.E.T Vietnam', 'Attendees: Mr. Đức | Purpose: To discuss about some general sepecification | Follow-up: Online meeting 2', 'Follow-up required', 'Online meeting 2', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-a628a8ee', 'cdb-799d129e', 'CLIENT_VISIT', '2023-27-02', 'IBS HI Factory', 'Ms. Tra', 'Client Visit: Shinwa ( Mitsui Miike)', 'Attendees: Ms. Tra | Purpose: To discuss about some general sepecification | Follow-up: Online meeting 3', 'Follow-up required', 'Online meeting 3', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-e606024f', 'cdb-bf58d0c8', 'CLIENT_VISIT', '2023-03-01', 'IBS HI Factory', 'Mr. Ivan and Ms. Paula', 'Client Visit: AAF/Stejasa', 'Attendees: Mr. Ivan and Ms. Paula', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-9940be4e', 'cdb-55bd9d37', 'CLIENT_VISIT', '2023-03-02', 'IBS HI Factory', '', 'Client Visit: VPI', '', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-7666f1d3', 'cdb-982e3910', 'CLIENT_VISIT', '2023-01-03', 'IBS HI Factory', 'Via Mr. Stephane', 'Client Visit: Canadian Customer', 'Attendees: Via Mr. Stephane | Purpose: Discuss with customer about some potential contract…. | Follow-up: Car pick up from HN at 22:00, 27/02/2023', 'Follow-up required', 'Car pick up from HN at 22:00, 27/02/2023', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-2daabc7c', 'cdb-982e3910', 'CLIENT_VISIT', '2023-03-03', 'IBS HI Factory', 'Via Mr. Stephane', 'Client Visit: Canadian Customer', 'Attendees: Via Mr. Stephane | Purpose: Discuss with customer about some potential contract….', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-1e04d292', 'cdb-4cd74147', 'CLIENT_VISIT', '2023-07-03', 'IBS HI Factory', '', 'Client Visit: Mitsui Miike Japan and shinwa', 'Purpose: Discuss about potential potential projects', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-2e3d6fac', 'cdb-e00b6594', 'CLIENT_VISIT', '2023-07-03', 'IBS HI Factory', 'Mr. Jun Ma - Mr. Hoon Sang - Mr.Sung Kwon Kim/Senior Manager, Overseass Project Mamagement Team', 'Client Visit: KC Cottrell Korea', 'Attendees: Mr. Jun Ma - Mr. Hoon Sang - Mr.Sung Kwon Kim/Senior Manager, Overseass Project Mamagement Team | Purpose: Request to requote. Epoxy reson for FGD do at site. Requested 1.500 USD/kg | Follow-up: Car pick up from Manoir hotel at 9:00 on 07/03/2023', 'Follow-up required', 'Car pick up from Manoir hotel at 9:00 on 07/03/2023', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-fe5bd9de', 'cdb-aebccec3', 'CLIENT_VISIT', '2023-13-03', 'IBS HI Factory', 'Zi Jian Tin -
  Dong Thi Thuy Duong', 'Client Visit: Ortsted', 'Attendees: Zi Jian Tin -
  Dong Thi Thuy Duong | Purpose: Discuss on scope you plan to supply and what is your plan for that
  Shoptour | Follow-up: follow up on concrete external platform, ventillation pipe, request to send concrete paltform drawings and spec to our contractor (IBS vendor). Deadline 31 Mar 23', 'Follow-up required', 'follow up on concrete external platform, ventillation pipe, request to send concrete paltform drawings and spec to our contractor (IBS vendor). Deadline 31 Mar 23', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-48dd238c', 'cdb-bf58d0c8', 'CLIENT_VISIT', '2023-15-03', 'IBS HI Factory', 'AAF: Ivan, Huy, Juan, Victor, Ayato
  IBS: Andrew, Luu, Thu', 'Client Visit: AAF/Stejasa', 'Attendees: AAF: Ivan, Huy, Juan, Victor, Ayato
  IBS: Andrew, Luu, Thu | Purpose: Discussion on drawings for transport skid, test port, structure (item h) , gratings requirments put on hold, | Follow-up: AAF is to respond to our queries', 'Follow-up required', 'AAF is to respond to our queries', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-0dab338a', 'cdb-31f9bb70', 'CLIENT_VISIT', '2023-03-16', 'IBS HI Factory', 'Chulwon Choi / Rain HwangKey Account Manager(Stationary) of Asia region
  Alex Hwang CEO / Kyuong Bae Jang Sales General Manager Noah Actuation', 'Client Visit: Samsung engineering & Noah', 'Attendees: Chulwon Choi / Rain HwangKey Account Manager(Stationary) of Asia region
  Alex Hwang CEO / Kyuong Bae Jang Sales General Manager Noah Actuation | Purpose: Future Project information and shop tour | Follow-up: Samsung will provide RFQ for chemical storage tanker with epoxy resin coating. Provide company profile, workload 2023 and financial statement 2023', 'Follow-up required', 'Samsung will provide RFQ for chemical storage tanker with epoxy resin coating. Provide company profile, workload 2023 and financial statement 2023', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-70b8fca8', 'cdb-55bd9d37', 'CLIENT_VISIT', '2023-15-04', 'IBS HI Factory', 'Anand Palki, Director of Design Engineering, Tony Brandano, CFO = Mike Blandford, Pook,', 'Client Visit: VPI', 'Attendees: Anand Palki, Director of Design Engineering, Tony Brandano, CFO = Mike Blandford, Pook, | Purpose: yard tour and engineering capbilities | Follow-up: conducted by Toan, Nhan, Hoan, arrange car to pick up at Sheraton at 10.45am, no lunch', 'Follow-up required', 'conducted by Toan, Nhan, Hoan, arrange car to pick up at Sheraton at 10.45am, no lunch', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-3886c90f', 'cdb-55bd9d37', 'CLIENT_VISIT', '2023-19-04', 'IBS HI Factory', 'Henning, Matt 
  Palki, Anand', 'Client Visit: VPI', 'Attendees: Henning, Matt 
  Palki, Anand | Purpose: Shop Tour, VPI upcoming work, Capacity Chart / Workload. VPI require us to submit loading chart every month. Clarify VPI insurance requirements. Give a list of confirmed VPI project | Follow-up: pick up 8.30am from Sheraton to yard and send them to Hai Phong Airport after meeting, flight 2.15pm (Lunch @ yard for 6p)', 'Follow-up required', 'pick up 8.30am from Sheraton to yard and send them to Hai Phong Airport after meeting, flight 2.15pm (Lunch @ yard for 6p)', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-920d5372', 'cdb-46241fe2', 'CLIENT_VISIT', '2023-20-04', 'IBS HI Factory', 'Anand Marwadi
  Yogesh Belure', 'Client Visit: JFE India', 'Attendees: Anand Marwadi
  Yogesh Belure | Purpose: introduction and yard tour. Feedback: In the past we always quoted 25% higher than our local competitors. | Follow-up: arrsnge own transport', 'Follow-up required', 'arrsnge own transport', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-31504d83', 'cdb-80026ed6', 'CLIENT_VISIT', '2023-20-04', 'IBS HI Factory', 'Pierre Nguyen Sales & Proposal Manager
  Mike Sandifer (Construction & Commissioning Manager USA),', 'Client Visit: SPG Dry Cooling', 'Attendees: Pierre Nguyen Sales & Proposal Manager
  Mike Sandifer (Construction & Commissioning Manager USA), | Purpose: Intorduction, yard tour, SPGDC Will send RFQ 25 dry cooling modules for Chung Chia Taiwan project. To follow up | Follow-up: Pick up 9.30am from Hanoi -Scent Premium Hotel to yard and drop off at Nikko hotel after meeting (Lunch @ yard for 6p)', 'Follow-up required', 'Pick up 9.30am from Hanoi -Scent Premium Hotel to yard and drop off at Nikko hotel after meeting (Lunch @ yard for 6p)', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-dac368b9', 'cdb-a49e8e33', 'CLIENT_VISIT', '2023-24-04', 'IBS HI Factory', 'Christian Freye, Wolfgang Niedziella, Nguyen Vu Tuan', 'Client Visit: Thyssenkrupp', 'Attendees: Christian Freye, Wolfgang Niedziella, Nguyen Vu Tuan | Purpose: Introduction and yard tour. Conducted by Toan | Follow-up: follow up with Thyssenkrupt for any new projects', 'Follow-up required', 'follow up with Thyssenkrupt for any new projects', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-6755ba2d', 'cdb-1c0042c8', 'CLIENT_VISIT', '2023-27-04', 'IBS HI Factory', 'Yoshitaka Sasaki Manager of Global Business Promotion', 'Client Visit: Nippon Paint', 'Attendees: Yoshitaka Sasaki Manager of Global Business Promotion | Purpose: introduce by Itoh from YBC (supplier of paint) | Follow-up: No need pick up', 'Follow-up required', 'No need pick up', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-a9fe7f65', 'cdb-c87876c7', 'CLIENT_VISIT', '2023-20-05', 'IBS HI Factory', 'Mr Ruslan Shigabutdinov-CEO, 
  Mr Ilnur Zamaletdinov-Head of Finance, 
  Mr Albert Latypov-Investment Expert, 
  Mr Anand Subramanian -Oil&Gas Expert', 'Client Visit: TAIF', 'Attendees: Mr Ruslan Shigabutdinov-CEO, 
  Mr Ilnur Zamaletdinov-Head of Finance, 
  Mr Albert Latypov-Investment Expert, 
  Mr Anand Subramanian -Oil&Gas Expert | Purpose: yard tour and presentation | Follow-up: request for projects list that yard completed on VN two oil renfineries', 'Follow-up required', 'request for projects list that yard completed on VN two oil renfineries', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-4a08c52a', 'cdb-9bb16045', 'CLIENT_VISIT', '2023-22-05', 'IBS HI Factory', 'Mr.Inokuchi, Mr.Kumaki and Itoh', 'Client Visit: YBC', 'Attendees: Mr.Inokuchi, Mr.Kumaki and Itoh | Purpose: Meeting Itoh san boss and discuss on upcoming projects | Follow-up: No need pick up, yet', 'Follow-up required', 'No need pick up, yet', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-e49c7d52', 'cdb-50392c27', 'CLIENT_VISIT', '2023-31-05', 'IBS HI Factory', 'Herve Vallee / Erection Manager', 'Client Visit: Five Stiein', 'Attendees: Herve Vallee / Erection Manager | Purpose: project clarifciation, yard tour, corporate presentation, dinner | Follow-up: Furnance equipment, duct and structure, Sale Team2 to follow up on the RFQ', 'Follow-up required', 'Furnance equipment, duct and structure, Sale Team2 to follow up on the RFQ', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-3708c980', 'cdb-65f486e6', 'CLIENT_VISIT', '2023-21-06', 'IBS HI Factory', 'Robert Bockman', 'Client Visit: GEA', 'Attendees: Robert Bockman | Purpose: Fetch Robert from hotel, yard visit, corporate presentatation, fill up quality audit form | Follow-up: follow up on RFQ', 'Follow-up required', 'follow up on RFQ', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-7cba275d', 'cdb-fb1939d8', 'CLIENT_VISIT', '2023-05-07', 'IBS HI Factory', 'Brian Han 
  Joohee Park', 'Client Visit: Hyundai', 'Attendees: Brian Han 
  Joohee Park | Purpose: Introduction, market situation | Follow-up: Like to know which transport company we used . Mr Park woud like to meet our Chairman', 'Follow-up required', 'Like to know which transport company we used . Mr Park woud like to meet our Chairman', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-75abcf5c', 'cdb-46241fe2', 'CLIENT_VISIT', '2023-05-08', 'IBS HI Factory', 'IMURA Yasuhiro', 'Client Visit: JFE/Blagladesh Railway', 'Attendees: IMURA Yasuhiro | Purpose: Introduction, JFE Presenation, IBS presentaion, safety moment, QA workflow, yard tour, exchnage of present | Follow-up: JFE is sastified. Ask for photos taken for this event and yard presentation', 'Follow-up required', 'JFE is sastified. Ask for photos taken for this event and yard presentation', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-803ebf62', 'cdb-ca941cde', 'CLIENT_VISIT', '2023-26-08', 'IBS HI Factory', 'Rogerio Rodrigues (Vice President Global Procurement)
  Daniel Pongitor
  Head of Sourcing, Asia-Pacific – Minerals BA', 'Client Visit: Metso Australia Limited', 'Attendees: Rogerio Rodrigues (Vice President Global Procurement)
  Daniel Pongitor
  Head of Sourcing, Asia-Pacific – Minerals BA | Purpose: Corporate PersentaionYard Tour | Follow-up: - Pick us up from Sheraton Haiphong at 8:30am to visit IBS Lisemco', 'Follow-up required', '- Pick us up from Sheraton Haiphong at 8:30am to visit IBS Lisemco', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-95d2f62d', 'cdb-20748fc4', 'CLIENT_VISIT', '2023-13-19', 'IBS HI Factory', 'Mr Đức', 'Client Visit: KNC Engineering', 'Attendees: Mr Đức | Purpose: Introduce pressure vessel | Follow-up: Meeting room 202', 'Follow-up required', 'Meeting room 202', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-c98e218c', 'cdb-428648f9', 'CLIENT_VISIT', '2023-19-09', 'IBS HI Factory', 'Mr Fausto Cattagni', 'Client Visit: Kirchner Italy S.p.A', 'Attendees: Mr Fausto Cattagni | Purpose: - Presentation
  - Working about heating, heat exchanger; and 
  answering some technical questions
  - Visiting th factory | Follow-up: - Pick up from Hoang Huy Grand Tower, 2 Đường Hồng Bàng, Hồng Bàng, Hải Phòng
 - Arrange meals at the company
 - Meeting room 202', 'Follow-up required', '- Pick up from Hoang Huy Grand Tower, 2 Đường Hồng Bàng, Hồng Bàng, Hải Phòng
 - Arrange meals at the company
 - Meeting room 202', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-8b83c8c9', 'cdb-46241fe2', 'CLIENT_VISIT', '2023-01-10', 'IBS HI Factory', 'Mr Sivakumar Velayutham', 'Client Visit: JFE Engineering India Private Limited', 'Attendees: Mr Sivakumar Velayutham', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-63687cc1', 'cdb-799d129e', 'CLIENT_VISIT', '2023-03-10', 'IBS HI Factory', 'Kiyoshi Kodama', 'Client Visit: Shinwa Engineering Co., Ltd', 'Attendees: Kiyoshi Kodama | Purpose: - Presentation
 - Working about ... and 
 answering some technical questions
 - Visiting the factory | Follow-up: - Metting room 202', 'Follow-up required', '- Metting room 202', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-521ed14f', 'cdb-ca941cde', 'CLIENT_VISIT', '2023-05-10', 'IBS HI Factory', 'Daniel Pongitor', 'Client Visit: Metso Australia Limited', 'Attendees: Daniel Pongitor | Purpose: - Working about ... and 
 answering some technical questions
 - Visiting the factory', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-73582ff1', 'cdb-55bd9d37', 'CLIENT_VISIT', '2023-10-10', 'IBS HI Factory', '', 'Client Visit: VOGT Power International', 'Purpose: Factory tour', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-3f34507f', 'cdb-799d129e', 'CLIENT_VISIT', '2023-10-19', 'IBS HI Factory', 'Mr. Tokimoto; Mr. Dang Duc Hai, Mr Nguyen Van Duc', 'Client Visit: Shinwa', 'Attendees: Mr. Tokimoto; Mr. Dang Duc Hai, Mr Nguyen Van Duc | Purpose: - Presentation', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-29c2ae05', 'cdb-55bd9d37', 'CLIENT_VISIT', '2023-10-24', 'IBS HI Factory', 'Anand Palki & Matt Henning, Mr Ittichet Saitin (Pook)', 'Client Visit: VOGT Power International', 'Attendees: Anand Palki & Matt Henning, Mr Ittichet Saitin (Pook) | Purpose: Go over IBS’s schedule and fabrication plan for the VPI projects V17552 Guyana and V17553 San Pedro. | Follow-up: 1:30 pm', 'Follow-up required', '1:30 pm', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-34dc1ef0', 'cdb-e00b6594', 'CLIENT_VISIT', '2023-10-24', 'IBS HI Factory', 'Danny Han - Vice Presiden
 JEIE CHEOL RYU 
 Dong Soo Seo', 'Client Visit: KC Cottrell', 'Attendees: Danny Han - Vice Presiden
 JEIE CHEOL RYU 
 Dong Soo Seo | Follow-up: 10am', 'Follow-up required', '10am', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-2d356444', 'cdb-9048b023', 'CLIENT_VISIT', '2023-10-27', 'IBS HI Factory', 'Mr. Cong', 'Client Visit: Boldrocchi', 'Attendees: Mr. Cong', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-9fd302c1', 'cdb-e00b6594', 'CLIENT_VISIT', '2023-31-10', 'IBS HI Factory', 'Dong Soo Seo
 Jeie Cheol Ryu', 'Client Visit: KC Cottrell', 'Attendees: Dong Soo Seo
 Jeie Cheol Ryu | Purpose: discuss technical matters, QC matters', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-fbf3eaf5', 'cdb-799d129e', 'CLIENT_VISIT', '2023-11-11', 'IBS HI Factory', '', 'Client Visit: Shinwa', 'Purpose: discuss project related to the quote for stack & Claimer | Follow-up: online meeting', 'Follow-up required', 'online meeting', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-f7f32b7d', 'cdb-850ef400', 'CLIENT_VISIT', '2023-11-14', 'IBS HI Factory', 'Alberto Pucci
 Nguyen Van Toai (Viet Solution Technology)', 'Client Visit: AC boilers', 'Attendees: Alberto Pucci
 Nguyen Van Toai (Viet Solution Technology) | Purpose: discuss HRSG', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-f67628f7', 'cdb-9bb16045', 'CLIENT_VISIT', '2023-12-09', 'IBS HI Factory', 'Inokuchi
 Tokuda', 'Client Visit: YBC', 'Attendees: Inokuchi
 Tokuda | Purpose: discuss some project of YBC, offer a RFQ for brigde in Nicaragua', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-4c247d9b', 'cdb-799d129e', 'CLIENT_VISIT', '2023-12-19', 'IBS HI Factory', '', 'Client Visit: Shinwa', 'Purpose: greetings, introduce the Manager assistant', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-ec682292', 'cdb-50a9fad0', 'CLIENT_VISIT', '2024-01-09', 'IBS HI Factory', 'Ivan martinez
 Gelu Dragan', 'Client Visit: Braden', 'Attendees: Ivan martinez
 Gelu Dragan | Purpose: yard audit; discuss some Quotes', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-1a8bd200', 'cdb-4704b45c', 'CLIENT_VISIT', '2024-01-10', 'IBS HI Factory', 'Gavin Lu
 Frauke Otto (Ms)', 'Client Visit: Cargobull', 'Attendees: Gavin Lu
 Frauke Otto (Ms)', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-26b778bb', 'cdb-799d129e', 'CLIENT_VISIT', '2024-01-25', 'IBS HI Factory', '', 'Client Visit: Shinwa', '', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-87f69340', 'cdb-80026ed6', 'CLIENT_VISIT', '2024-01-26', 'IBS HI Factory', 'Pierry Nguyen', 'Client Visit: SPG Dry Cooling', 'Attendees: Pierry Nguyen | Purpose: Audit', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-43b25b97', 'cdb-077d30c4', 'CLIENT_VISIT', '2024-02-07', 'IBS HI Factory', 'Mr. Grini Habib', 'Client Visit: John Cockerill SA', 'Attendees: Mr. Grini Habib | Purpose: negotiate to sign PO', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-c164d75f', 'cdb-7a23cf3f', 'CLIENT_VISIT', '2024-03-11', 'IBS HI Factory', '- Rei Nishio
 - Ryota Shiba
 - Bin Zhou', 'Client Visit: JGC', 'Attendees: - Rei Nishio
 - Ryota Shiba
 - Bin Zhou | Purpose: shop tour, discuss QC matters', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-18d59142', 'cdb-99b68da9', 'CLIENT_VISIT', '2024-03-21', 'IBS HI Factory', 'Nguyễn Đức Phong', 'Client Visit: Pems (Asia Networks PEMS Co.,Ltd', 'Attendees: Nguyễn Đức Phong', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-c6d1ba01', 'cdb-4a3a5253', 'CLIENT_VISIT', '2024-04-05', 'IBS HI Factory', 'Mr. Kim Hui Cheol', 'Client Visit: - KAV Engineering & Construction
 - Daekwang International', 'Attendees: Mr. Kim Hui Cheol', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-f479820a', 'cdb-e8f87066', 'CLIENT_VISIT', '2024-04-10', 'IBS HI Factory', '- Mr.Joris Van Tiennen
 - Mr. Hendrik Jan de kluiver', 'Client Visit: DAMEN', 'Attendees: - Mr.Joris Van Tiennen
 - Mr. Hendrik Jan de kluiver', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-d1079c85', 'cdb-fe1126d7', 'CLIENT_VISIT', '2024-04-22', 'IBS HI Factory', '', 'Client Visit: Fortescue', '', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-d30f3215', 'cdb-50a9fad0', 'CLIENT_VISIT', '2024-04-23', 'IBS HI Factory', 'Mr. Murugappan (Siemens)
 Mr. Huy (Braden)', 'Client Visit: Braden - Siemens', 'Attendees: Mr. Murugappan (Siemens)
 Mr. Huy (Braden)', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-4f4f531f', 'cdb-ad6ce436', 'CLIENT_VISIT', '2024-04-24', 'IBS HI Factory', 'Mr. Bùi Thanh Bình + 4 others', 'Client Visit: PTSC', 'Attendees: Mr. Bùi Thanh Bình + 4 others', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-d16c9fce', 'cdb-a49e8e33', 'CLIENT_VISIT', '2024-04-25', 'IBS HI Factory', 'Vu Tuan Nguyen', 'Client Visit: Thyssenkrupp', 'Attendees: Vu Tuan Nguyen | Purpose: Audit: abrication of welded structures, steel plate works and steel structures category topics including machining', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-e0b4b7c8', 'cdb-a9fab70c', 'CLIENT_VISIT', '2024-04-26', 'IBS HI Factory', 'Jin - Sung, Hwang', 'Client Visit: Woosung Industry', 'Attendees: Jin - Sung, Hwang', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-6c327d32', 'cdb-ca941cde', 'CLIENT_VISIT', '2024-05-15', 'IBS HI Factory', '- Mr. Rogerio Rodrigues – VP of Global Procurement
 - Mr. Daniel Pongitor – Director of Procurement Asia-Pacific
 - Mr. Tuomas Tanskanen – Director of Sourcing, Hydrometallurgy Business Line', 'Client Visit: Metso Australia Limited', 'Attendees: - Mr. Rogerio Rodrigues – VP of Global Procurement
 - Mr. Daniel Pongitor – Director of Procurement Asia-Pacific
 - Mr. Tuomas Tanskanen – Director of Sourcing, Hydrometallurgy Business Line', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-3b397086', 'cdb-0e6fc796', 'CLIENT_VISIT', '2024-05-22', 'IBS HI Factory', '- Jeong Hee Lee
 - Heo PilSeong
 - Terry Koo
 - Phan Thanh Son', 'Client Visit: KC Cotrell', 'Attendees: - Jeong Hee Lee
 - Heo PilSeong
 - Terry Koo
 - Phan Thanh Son | Purpose: discuss opportunity to work in project in VietNam:', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-9649ba7d', 'cdb-e8f87066', 'CLIENT_VISIT', '2024-05-28', 'IBS HI Factory', '', 'Client Visit: 189-Damen', 'Purpose: discuss opportunity on ship-building project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-e449a01c', 'cdb-a49e8e33', 'CLIENT_VISIT', '2024-05-30', 'IBS HI Factory', 'Hà Quang Hoà', 'Client Visit: Thyssenkrupp', 'Attendees: Hà Quang Hoà | Purpose: Audit yard and discuss Quotation 24069 - ODEFA project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-4ad2abef', 'cdb-55bd9d37', 'CLIENT_VISIT', '2024-06-17', 'IBS HI Factory', '- Anand Palki
 - Gary Hansen
 - Samuel A.Goodwin
 - Chutima Pachuenjai (EYE)', 'Client Visit: VOGT Power International', 'Attendees: - Anand Palki
 - Gary Hansen
 - Samuel A.Goodwin
 - Chutima Pachuenjai (EYE) | Purpose: - discuss opportunity strategy
 - training working on silencer', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-f2f14ed1', 'cdb-e8f87066', 'CLIENT_VISIT', '2024-06-25', 'IBS HI Factory', '', 'Client Visit: DAMEN', '', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-e024f403', 'cdb-9bb16045', 'CLIENT_VISIT', '2024-06-28', 'IBS HI Factory', '- Hironobu Tokuda
 - Mamoru SAKO', 'Client Visit: YBC', 'Attendees: - Hironobu Tokuda
 - Mamoru SAKO | Purpose: - Greetings & Audit yard', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-ca372c4e', 'cdb-50a9fad0', 'CLIENT_VISIT', '2024-07-02', 'IBS HI Factory', '- Ivan Martinez
 - Roland Passeri', 'Client Visit: Braden', 'Attendees: - Ivan Martinez
 - Roland Passeri | Purpose: kick off meeting for NEOM project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-a00a00b1', 'cdb-9bedf01c', 'CLIENT_VISIT', '2024-07-04', 'IBS HI Factory', '- Mohsen Rezaei Pour
 - Tran Thi Hanh Dung', 'Client Visit: Embassy of the Isalamic Republic of Iran in Hanoi', 'Attendees: - Mohsen Rezaei Pour
 - Tran Thi Hanh Dung | Purpose: discuss IBS''s ship-building capacity', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-9370c8e5', 'cdb-e8f87066', 'CLIENT_VISIT', '2024-07-17', 'IBS HI Factory', '', 'Client Visit: Damen', 'Purpose: discuss to make the PO for ship-building project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-06843530', 'cdb-a49e8e33', 'CLIENT_VISIT', '2024-07-29', 'IBS HI Factory', '', 'Client Visit: Thyssenkrupp', 'Purpose: kick off meeting for ODEFA _ Chutes package', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-8e5164bd', 'cdb-9bb16045', 'CLIENT_VISIT', '2024-07-30', 'IBS HI Factory', 'Itoh', 'Client Visit: YBC', 'Attendees: Itoh', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-2c8c98c8', 'cdb-50a9fad0', 'CLIENT_VISIT', '2024-08-29', 'IBS HI Factory', 'Mr. Norman Gorka', 'Client Visit: Braden', 'Attendees: Mr. Norman Gorka | Purpose: Greetings', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-c2e68b52', 'cdb-babed227', 'CLIENT_VISIT', '2024-09-05', 'IBS HI Factory', 'Mr. Kreingkrai Tuntananukul', 'Client Visit: Black & Vetch + VPI', 'Attendees: Mr. Kreingkrai Tuntananukul | Purpose: Audit: Shoptour & visit TECO project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-34218457', 'cdb-b24bb989', 'CLIENT_VISIT', '2024-09-18', 'IBS HI Factory', 'Mr. Dao Hoang Quy', 'Client Visit: Phuc Thanh company', 'Attendees: Mr. Dao Hoang Quy | Purpose: greetings & shoptour, discuss about quotation for tanks', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-1a6ca7ab', 'cdb-24a1eab9', 'CLIENT_VISIT', '2024-09-26', 'IBS HI Factory', '- Mai Thanh Tuấn
 - Lê Tiến Dũng
 - Nguyễn Văn Hoàng', 'Client Visit: Công ty TNHH CTCI Việt Nam', 'Attendees: - Mai Thanh Tuấn
 - Lê Tiến Dũng
 - Nguyễn Văn Hoàng | Purpose: discuss opportuinities on frabrication of HRSG', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-e52d133e', 'cdb-799d129e', 'CLIENT_VISIT', '2024-10-09', 'IBS HI Factory', '- Shinwa: Mr. Hasegawa, Mr. Duc', 'Client Visit: Shinwa + MMM', 'Attendees: - Shinwa: Mr. Hasegawa, Mr. Duc | Purpose: - discuss quotation 24142 for for conveyor of Steel manufactory KOBE', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-35f4d8e4', 'cdb-799d129e', 'CLIENT_VISIT', '2024-10-10', 'IBS HI Factory', '- Shinwa: Mr. Hasegawa, Mr. Duc
 - MMM: supervisors at shop', 'Client Visit: Shinwa + MMM', 'Attendees: - Shinwa: Mr. Hasegawa, Mr. Duc
 - MMM: supervisors at shop | Purpose: summary of the implementation of Project: Fabrication bucket wheel & wheel frame', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-e043923b', 'cdb-27c6f3df', 'CLIENT_VISIT', '2024-11-07', 'IBS HI Factory', 'Ittichet (Pook) Saitin', 'Client Visit: BABCOCK POWER (THAILAND) LIMITED', 'Attendees: Ittichet (Pook) Saitin | Purpose: Audit: Manufacturing &amp; Quality System Overview; Shop tour evaluating implementation of the quality program', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-0af7f80f', 'cdb-50a9fad0', 'CLIENT_VISIT', '2024-12-02', 'IBS HI Factory', 'Tony Armstrong
 Ivo Feld', 'Client Visit: Braden', 'Attendees: Tony Armstrong
 Ivo Feld | Purpose: Audit for 13002 project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-9aa1fa2f', 'cdb-50a9fad0', 'CLIENT_VISIT', '2024-12-05', 'IBS HI Factory', 'Frank Hoffman
 Gelu Dragan', 'Client Visit: Braden', 'Attendees: Frank Hoffman
 Gelu Dragan | Purpose: Audit for NEOM project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-30b1a43e', 'cdb-2f075ba1', 'CLIENT_VISIT', '2024-12-04', 'IBS HI Factory', 'Asyraf Zulkifli', 'Client Visit: SLB', 'Attendees: Asyraf Zulkifli | Purpose: Audit: Manufacturing
 Process(Production & Quality
 control), Engineering Processes, Procurement-Supply chain', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-9ab192cf', 'cdb-3485e685', 'CLIENT_VISIT', '2024-12-11', 'IBS HI Factory', 'Mr Liêm', 'Client Visit: GE', 'Attendees: Mr Liêm | Purpose: Audit for Braden project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-aad7353d', 'cdb-12f902b9', 'CLIENT_VISIT', '2024-12-11', 'IBS HI Factory', 'Thomas Grafen', 'Client Visit: Büttner Energie', 'Attendees: Thomas Grafen | Purpose: Audit workshop:
 -Production and maching/rolling capabilities
 -Corrosion protection and painting
 -Packaging, labeling for transport
 -Organisation of your production', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-3220785d', 'cdb-799d129e', 'CLIENT_VISIT', '2024-12-16', 'IBS HI Factory', 'Mohamed khadir
 Ajibola', 'Client Visit: Fortafric Energy Limited', 'Attendees: Mohamed khadir
 Ajibola | Purpose: Fotafric audit for 13002 Project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-7928ff97', 'cdb-a7f1a0fe', 'CLIENT_VISIT', '2024-12-26', 'IBS HI Factory', 'Mutalib', 'Client Visit: G.P.S', 'Attendees: Mutalib | Purpose: GPS-Büttner audit', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-94e1ba05', 'cdb-a49e8e33', 'CLIENT_VISIT', '2025-01-08', 'IBS HI Factory', '- Mr. Balasubramanian
 - Thyssen team: Hoà, Hương…', 'Client Visit: Thyssenkrupp', 'Attendees: - Mr. Balasubramanian
 - Thyssen team: Hoà, Hương… | Purpose: KOM meeting', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-6a3c2e98', 'cdb-46241fe2', 'CLIENT_VISIT', '2025-01-15', 'IBS HI Factory', 'Funaba Taku', 'Client Visit: JFE Engineering Corp', 'Attendees: Funaba Taku', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-d4909756', 'cdb-55bd9d37', 'CLIENT_VISIT', '2025-01-22', 'IBS HI Factory', 'Anand Palki, Matt Henning', 'Client Visit: VOGT Power International', 'Attendees: Anand Palki, Matt Henning | Purpose: Capacity Reservation Agreement', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-58109d99', 'cdb-50a9fad0', 'CLIENT_VISIT', '2025-01-23', 'IBS HI Factory', 'Norman Gorka', 'Client Visit: Braden', 'Attendees: Norman Gorka | Purpose: Ongoing projects, GE audit (results), Capacity tracker, workload update', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-5d3ecc3c', 'cdb-799d129e', 'CLIENT_VISIT', '2025-02-05', 'IBS HI Factory', 'YUSUKE TAKEUCHI', 'Client Visit: Shinwa', 'Attendees: YUSUKE TAKEUCHI | Purpose: Update the lastest project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-863f530c', 'cdb-bd3867f4', 'CLIENT_VISIT', '2025-02-05', 'IBS HI Factory', 'Voß Josef', 'Client Visit: Wendt-Noise Control GMBH', 'Attendees: Voß Josef', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-8e0ed3b9', 'cdb-e8f87066', 'CLIENT_VISIT', '2025-02-12', 'IBS HI Factory', 'Doan Nam', 'Client Visit: DAMEN', 'Attendees: Doan Nam', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-66be5581', 'cdb-50392c27', 'CLIENT_VISIT', '2025-02-12', 'IBS HI Factory', 'Stephen Stein', 'Client Visit: STF Loterios S.r.l.', 'Attendees: Stephen Stein | Purpose: Pressure tank', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-2dfe11e2', 'cdb-a49e8e33', 'CLIENT_VISIT', '2025-02-19', 'IBS HI Factory', 'Thyssenkrupp Polysius USA
 TKPV team', 'Client Visit: Thyssenkrupp', 'Attendees: Thyssenkrupp Polysius USA
 TKPV team | Purpose: thyssenkrupp Polysius Atlanta visit', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-4a6bdb08', 'cdb-799d129e', 'CLIENT_VISIT', '2025-03-14', 'IBS HI Factory', 'Nguyen Van Duc', 'Client Visit: Shinwa', 'Attendees: Nguyen Van Duc | Purpose: Introduce new customer', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-5877c506', 'cdb-50a9fad0', 'CLIENT_VISIT', '2025-03-26', 'IBS HI Factory', 'Ivan Martinez', 'Client Visit: Braden', 'Attendees: Ivan Martinez', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-d1f66a57', 'cdb-55bd9d37', 'CLIENT_VISIT', '2025-03-29', 'IBS HI Factory', 'Anand Palki
 Matthew S Henning', 'Client Visit: VOGT Power International', 'Attendees: Anand Palki
 Matthew S Henning | Purpose: V17565 Williston (Bison) NPP project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-4cd10ad2', 'cdb-7585a9d6', 'CLIENT_VISIT', '2025-03-31', 'IBS HI Factory', '', 'Client Visit: Tei', '', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-0906c77a', 'cdb-3485e685', 'CLIENT_VISIT', '2025-04-15', 'IBS HI Factory', '', 'Client Visit: GE', 'Purpose: Auditted by GE', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-fe5ddf30', 'cdb-46241fe2', 'CLIENT_VISIT', '2025-04-22', 'IBS HI Factory', '', 'Client Visit: JFE', 'Purpose: Greetings', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-022c9f0e', 'cdb-bd3867f4', 'CLIENT_VISIT', '2025-05-15', 'IBS HI Factory', 'Mr. Joself', 'Client Visit: Wendt-Noise Control GMBH', 'Attendees: Mr. Joself | Purpose: discussion potiential projects', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-701cdeef', 'cdb-50a9fad0', 'CLIENT_VISIT', '2025-06-03', 'IBS HI Factory', 'Mr. Ivan', 'Client Visit: Braden Europe B.V', 'Attendees: Mr. Ivan', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-2b7e04f6', 'cdb-077d30c4', 'CLIENT_VISIT', '2025-06-19', 'IBS HI Factory', 'Ms. Laurence GUIDI', 'Client Visit: John Cockerill SA', 'Attendees: Ms. Laurence GUIDI | Purpose: negotiation project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-b042893c', 'cdb-787f6486', 'CLIENT_VISIT', '2025-07-14', 'IBS HI Factory', 'Mr. Lone Moldrup', 'Client Visit: Moldrup', 'Attendees: Mr. Lone Moldrup | Purpose: Greetings and discuss cooperation opportunity', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-54155d50', 'cdb-55bd9d37', 'CLIENT_VISIT', '2025-08-06', 'IBS HI Factory', 'Mr. Varakorn', 'Client Visit: VOGT Power International', 'Attendees: Mr. Varakorn | Purpose: Greetings and checking Bison Project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-cb55d09d', 'cdb-bd3867f4', 'CLIENT_VISIT', '2025-08-07', 'IBS HI Factory', 'Mr. Joself', 'Client Visit: Wendt-Noise Control GMBH', 'Attendees: Mr. Joself | Purpose: checking ongoing projects', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-942f45c4', 'cdb-af6960c2', 'CLIENT_VISIT', '2025-08-12', 'IBS HI Factory', 'Mr. Naren Rao', 'Client Visit: NEM', 'Attendees: Mr. Naren Rao | Purpose: Audit workshop', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-e93fc9fd', 'cdb-55bd9d37', 'CLIENT_VISIT', '2025-08-13', 'IBS HI Factory', 'Ms. Chutima', 'Client Visit: VOGT Power International', 'Attendees: Ms. Chutima | Purpose: Greetings and introduce new PM, QC Engineer', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-01f0132d', 'cdb-27c6f3df', 'CLIENT_VISIT', '2025-08-19', 'IBS HI Factory', 'Mr. Dennis Chambers', 'Client Visit: Babcock Power Services', 'Attendees: Mr. Dennis Chambers | Purpose: Greetings and discuss cooperation opportunity', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-66e3e8ca', 'cdb-3a057128', 'CLIENT_VISIT', '2025-09-10', 'IBS HI Factory', 'Mr. Nhật', 'Client Visit: Gonnix', 'Attendees: Mr. Nhật | Purpose: Negotiation project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-9d9e68a3', 'cdb-7a23cf3f', 'CLIENT_VISIT', '2025-09-19', 'IBS HI Factory', 'Mr. Ryota Shiba', 'Client Visit: JGC Corporation', 'Attendees: Mr. Ryota Shiba | Purpose: Greetings and discuss cooperation opportunity', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-0f2810e7', 'cdb-55bd9d37', 'CLIENT_VISIT', '2025-09-22', 'IBS HI Factory', 'Mr. Chris Turner
Mr. Anand Palki', 'Client Visit: VOGT Power International', 'Attendees: Mr. Chris Turner
Mr. Anand Palki | Purpose: Greetings and negotiation projects', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-d8f11ec7', 'cdb-af6960c2', 'CLIENT_VISIT', '2025-09-30', 'IBS HI Factory', 'Mr. Harald Swienty', 'Client Visit: NEM', 'Attendees: Mr. Harald Swienty | Purpose: Greetings and negotiation projects', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-627bd246', 'cdb-a49e8e33', 'CLIENT_VISIT', '2025-10-21', 'IBS HI Factory', '', 'Client Visit: Thyssenkrupp Spain', '', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-122c04a2', 'cdb-65524eec', 'CLIENT_VISIT', '2025-10-24', 'IBS HI Factory', 'Ms. Lucila Alvarez', 'Client Visit: Orbia Fluor & Energy Materials', 'Attendees: Ms. Lucila Alvarez | Purpose: Online Meeting - Greetings and discuss cooperation opportunity', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-b001ef6c', 'cdb-8b96c5fb', 'CLIENT_VISIT', '2025-11-11', 'IBS HI Factory', 'Mr. Y J Lee', 'Client Visit: KHPT Co.,Ltd', 'Attendees: Mr. Y J Lee | Purpose: Greetings and negotiation projects', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-142260c2', 'cdb-55bd9d37', 'CLIENT_VISIT', '2025-11-18', 'IBS HI Factory', '- Mr. Henning Matt
- Mr. John Berra
- Mr. Gary Hansen', 'Client Visit: VOGT Power International', 'Attendees: - Mr. Henning Matt
- Mr. John Berra
- Mr. Gary Hansen | Purpose: - review ongoing projects.
- review IBS workload
- Review upcoming line of sight', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-71d937fd', 'cdb-50a9fad0', 'CLIENT_VISIT', '2025-11-19', 'IBS HI Factory', '- Mr. Ivan Martinez
- Mr. Roland Passer', 'Client Visit: Braden Europe B.V', 'Attendees: - Mr. Ivan Martinez
- Mr. Roland Passer', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-a1973d90', 'cdb-077d30c4', 'CLIENT_VISIT', '2025-12-09', 'IBS HI Factory', '- Mr. Miloslav Roµec', 'Client Visit: 2JCP', 'Attendees: - Mr. Miloslav Roµec | Purpose: Audit workshop', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-47ff2bce', 'cdb-af6960c2', 'CLIENT_VISIT', '2026-02-28', 'IBS HI Factory', '- Mr. Harald Swienty', 'Client Visit: NEM', 'Attendees: - Mr. Harald Swienty | Purpose: - Discuss potiential project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-4d85eb8b', 'cdb-46241fe2', 'CLIENT_VISIT', '2026-03-04', 'IBS HI Factory', '', 'Client Visit: 2JFE', 'Purpose: - Greetings', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-38c0f5f6', 'cdb-bd3867f4', 'CLIENT_VISIT', '2026-03-12', 'IBS HI Factory', '- Mr. Vob Joseff', 'Client Visit: WNC', 'Attendees: - Mr. Vob Joseff | Purpose: - Discuss potiential project', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-5c7fcdd2', 'cdb-799d129e', 'CLIENT_VISIT', '2026-03-31', 'IBS HI Factory', '', 'Client Visit: Shinwa', 'Purpose: - Shinwa introduces Teisa and visit IBS workshop', 'Visit completed', '', 'CDB Import');

INSERT OR IGNORE INTO sale_customer_interactions (id, customer_id, interaction_type, interaction_date, location, attendees_customer, subject, summary, outcome, next_action, recorded_by)
  VALUES ('visit-1453778c', 'cdb-50a9fad0', 'CLIENT_VISIT', '2026-04-18', 'IBS HI Factory', '- Mr. Ivan', 'Client Visit: Braden', 'Attendees: - Mr. Ivan | Purpose: - update current project 090.', 'Visit completed', '', 'CDB Import');

-- Total: 142 client visits, 19 new visit-only customers