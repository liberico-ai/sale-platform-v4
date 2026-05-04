# SYSTEM COMPLETENESS AUDIT — Sale Platform v4
**Ngày: 04/05/2026** | **Phiên bản: 1.0** | **Tác giả: AI Chief of Staff**

---

## MỤC ĐÍCH

Tài liệu này audit TOÀN BỘ hệ thống Sale Platform v4 ở mức **"chạy được hàng ngày cho Sale team"** — không chỉ kiểm tra endpoint tồn tại mà đánh giá **workflow end-to-end**, **UI completeness**, và **missing glue features** giữa các module.

Yêu cầu từ Chairman: *"Hệ thống phải chạy đầy đủ, bạn audit kỹ. Tôi chỉ liệt kê tính năng chính, có các tính năng để chạy và kết nối tôi có thể miss."*

---

## PHƯƠNG PHÁP

- Đọc toàn bộ 25 routers (146 endpoints)
- Đọc toàn bộ 6 trang frontend HTML
- Kiểm tra 8 services, 4 workers
- Kiểm tra models/ directory (3 files imported, 27 inline models)
- Map từng user workflow end-to-end: user mở trình duyệt → login → thực hiện task hàng ngày → logout

---

## TÓM TẮT THỰC TRẠNG

| Metric | Số liệu |
|--------|---------|
| Backend routers | 25 (146 endpoints) |
| Frontend pages | 6 HTML files (1 SPA + 5 standalone) |
| Tables | 32 + 2 views |
| Records | ~6,700 |
| DELETE endpoints | **0 trên toàn hệ thống** |
| Edit forms trong UI | **1** (customer create only, không có edit) |
| Screens có full CRUD | **0** |
| Inline Pydantic models | 27 (nên ở models/) |

---

## PHẦN A: BACKEND — AUDIT TỪNG MODULE

### A1. Customers (routers/customers.py) — ⚠️ GẦN ĐẦY ĐỦ

**Có:** List (filter, pagination) • Search (UNION contacts) • Duplicates • Detail (with sub-resources) • Create • Update • Soft-delete (admin)

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A1.1 | Merge duplicates endpoint | HIGH | 992 customers từ 5 sources, có duplicate detection nhưng không merge được |
| A1.2 | Bulk status update | MED | Change ACTIVE/INACTIVE cho nhiều customer cùng lúc |
| A1.3 | Customer activity timeline | HIGH | Unified view: emails + interactions + tasks + quotations + follow-ups theo thời gian |
| A1.4 | Customer health score | MED | Tổng hợp tần suất liên hệ, pipeline value, payment history → score |
| A1.5 | Contact search/filter trên list endpoint | LOW | Hiện chỉ filter by region/status, thiếu filter by contact email/name |

---

### A2. Contacts (routers/contacts.py) — ⚠️ THIẾU DELETE + SEARCH

**Có:** List • Duplicate detection • Detail • Create • Update

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A2.1 | DELETE (soft-delete) | HIGH | 2,990 contacts, không xóa được contact sai/trùng |
| A2.2 | Search/filter by name, email, phone | HIGH | List endpoint không có search, chỉ list toàn bộ |
| A2.3 | Bulk import validation preview | MED | Import CSV nhưng không preview trước khi commit |
| A2.4 | Contact communication history | MED | Xem tất cả email/interaction liên quan đến contact cụ thể |
| A2.5 | vCard export | LOW | Export contact card chuẩn |

---

### A3. Opportunities (routers/opportunities.py) — ⚠️ THIẾU DELETE + TRANSITION API

**Có:** List (filter) • Stale detection • Create • Update (with state machine) • Detail

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A3.1 | DELETE (soft-delete) | HIGH | Opportunity tạo nhầm không xóa được |
| A3.2 | Dedicated stage transition endpoint `POST /{id}/transition` | HIGH | UI cần endpoint rõ ràng, trả về allowed_next_stages + side effects |
| A3.3 | `allowed_next_stages` trong list response | HIGH | UI render transition buttons inline mà không fetch từng detail |
| A3.4 | Clone/duplicate opportunity | MED | Tạo opportunity mới từ template opportunity cũ |
| A3.5 | Win/Loss side effects | CRITICAL | WON → auto-create contract + commission. LOST → require loss_reason, log competitor |
| A3.6 | Opportunity-to-Quotation link on create | HIGH | QuotationCreate không có opportunity_id field |
| A3.7 | Bulk stage update | MED | Di chuyển nhiều opportunity qua stage cùng lúc |
| A3.8 | Pipeline weighted value recalculation trigger | LOW | Khi win_probability thay đổi, recalc tổng weighted |

---

### A4. Quotations (routers/quotations.py) — ⚠️ THIẾU WORKFLOW ACTIONS

**Có:** List history • Win-rate • Detail • Revisions • Create • Update • Revise

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A4.1 | DELETE (soft-delete) | MED | Quotation draft sai không xóa được |
| A4.2 | `opportunity_id` trong QuotationCreate | CRITICAL | Hiện không link được quotation → opportunity khi tạo mới |
| A4.3 | WON action endpoint `POST /{id}/win` | CRITICAL | Win cần side effects: update opp stage, create contract, trigger commission calc |
| A4.4 | LOST action endpoint `POST /{id}/lose` | HIGH | Lost cần: require reason, update opp, log competitor |
| A4.5 | SEND action `POST /{id}/send` | HIGH | Mark as SENT, log email, update date |
| A4.6 | PDF/DOCX generation từ quote template | MED | Render quotation thành file gửi khách |
| A4.7 | Comparison view giữa revisions | LOW | So sánh rev A vs rev B highlight differences |
| A4.8 | Approval workflow trước khi gửi | MED | Manager approve quotation trước khi chuyển SENT |

---

### A5. Tasks (routers/tasks.py) — ⚠️ THIẾU DELETE + DETAIL

**Có:** List • Board (kanban) • My tasks • Create (with email/opp link) • Update (state machine) • Escalate

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A5.1 | DELETE (soft-delete) | HIGH | Task tạo nhầm không xóa được |
| A5.2 | GET /{task_id} detail endpoint | CRITICAL | Không có detail endpoint, board chỉ trả summary |
| A5.3 | Task comments/notes | HIGH | Log progress, blockers, decisions trên task |
| A5.4 | Task due date integration với SLA engine | HIGH | Create task → auto-calc due_date từ sla_engine.py (hiện disconnected) |
| A5.5 | Sub-tasks | MED | Break task thành các bước nhỏ |
| A5.6 | Bulk status update | MED | Close all tasks khi opportunity WON/LOST |
| A5.7 | Recurring tasks | LOW | Tạo task tự động hàng tuần/tháng |
| A5.8 | `/my` lấy user từ auth context | HIGH | Hiện dùng query param `current_user` — security concern |

---

### A6. Emails (routers/emails.py) — ✅ TƯƠNG ĐỐI ĐẦY ĐỦ

**Có:** List (filter) • Detail • Sync • Update (read/actioned) • Create-task • Labels • Full emails • Follow-ups view • Compose (DRAFT) • Render reply • Project activity

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A6.1 | Email search (full-text) | HIGH | Hiện chỉ filter by type/status, không search body/subject |
| A6.2 | Bulk mark read/actioned | MED | Mark 20 emails cùng lúc |
| A6.3 | Email thread complete view | MED | Hiện chỉ link by thread_id, không aggregate thành conversation |
| A6.4 | Attachment metadata | LOW | Hiện không track attachments |
| A6.5 | AI re-classification override | LOW | User sửa classification sai → feedback loop |

---

### A7. Contracts (routers/contracts.py) — ⚠️ THIẾU WRITE ENDPOINTS

**Có:** List • Detail • Milestones (CRUD partial) • Settlements (create only) • Change orders (read only) • KHKD targets (read only)

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A7.1 | Settlement UPDATE endpoint | CRITICAL | Tạo được settlement nhưng không update status OPEN→APPROVED→CLOSED |
| A7.2 | Change order CRUD | HIGH | Read-only, không tạo/sửa change orders |
| A7.3 | KHKD target CRUD | HIGH | Read-only, không update targets khi revise |
| A7.4 | Contract status state machine | HIGH | Status changes không validated, chỉ audit-logged |
| A7.5 | Contract-to-Opportunity FK | MED | Hiện dùng fuzzy name matching, rất fragile |
| A7.6 | Contract completion % auto-calc | MED | Từ milestone statuses → overall progress |
| A7.7 | DELETE for sub-resources | LOW | Milestone/settlement tạo nhầm không xóa được |
| A7.8 | Contract renewal/extension | LOW | Clone contract cũ → contract mới |

---

### A8. Follow-ups (routers/follow_ups.py) — ⚠️ THIẾU NHIỀU

**Có:** List • Overdue • Create • Update

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A8.1 | GET /{follow_up_id} detail | HIGH | Không có detail endpoint |
| A8.2 | DELETE | MED | Follow-up tạo nhầm không xóa |
| A8.3 | Customer-only follow-ups | HIGH | Hiện bắt buộc opportunity_id, không follow-up cho customer chung |
| A8.4 | Status validation via state machine | MED | Hiện accept bất kỳ string nào |
| A8.5 | Reminder delivery (email/notification) | HIGH | Schedule tồn tại nhưng không gửi reminder |
| A8.6 | Calendar view endpoint | MED | Follow-ups theo ngày/tuần/tháng |
| A8.7 | Snooze/postpone action | LOW | Dời follow-up nhanh 1 ngày/1 tuần |

---

### A9. Commissions (routers/commissions.py) — ⚠️ THIẾU APPROVAL GATE

**Có:** List • By-salesperson aggregate • Detail • Auto-calculate • Manual create • Update

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A9.1 | Admin-only gate cho APPROVED/PAID transitions | CRITICAL | Hiện require_write, không require_admin — bất kỳ user write có thể approve |
| A9.2 | State machine integration | HIGH | Transitions hardcoded inline, không dùng central state_machine.py |
| A9.3 | Batch approval | MED | Approve nhiều commissions cùng lúc |
| A9.4 | DB-driven commission tiers | MED | Hiện hardcoded 0.5%-2%, không config được |
| A9.5 | Commission report/summary | LOW | Tổng commission by period, by salesperson |
| A9.6 | DELETE/VOID endpoint | MED | Commission tính sai không void được riêng |

---

### A10. Inter-department Tasks (routers/inter_dept.py) — ⚠️ THIẾU WORKFLOW CHAIN

**Có:** List • Board (kanban) • Detail • Create • Update • Escalate

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A10.1 | Auto-create next step khi step hoàn thành | HIGH | step_number/total_steps tồn tại nhưng không auto-advance |
| A10.2 | State machine consolidation | MED | Inline transitions, nên merge vào central state_machine.py |
| A10.3 | DELETE | MED | IDT tạo nhầm không xóa |
| A10.4 | Template cho common inter-dept flows | LOW | Pre-defined step sequences cho common requests |

---

### A11. Intelligence (routers/intelligence.py) — ⚠️ READ-ONLY

**Có:** Market signals list/detail • Product opportunities list • Digital content list • Product categories

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A11.1 | Signal acknowledge/dismiss action | HIGH | User đánh dấu đã xem/bỏ qua signal |
| A11.2 | Convert signal → opportunity | HIGH | From market signal, tạo opportunity mới |
| A11.3 | Product opportunity CRUD | MED | Thêm/sửa product opportunities |
| A11.4 | Digital content CRUD | MED | Upload/manage marketing materials |
| A11.5 | Signal source management | LOW | Config nguồn signals |

---

### A12. Dashboard (routers/dashboard.py) — ✅ TƯƠNG ĐỐI ĐẦY ĐỦ

**Có:** Pipeline summary • By-product • By-quarter • Tasks summary • Email summary • Executive • Summary (33-table aggregate) • My dashboard

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A12.1 | Date range filter | HIGH | Tất cả dashboard queries không có date range |
| A12.2 | Drill-down links | MED | Click KPI card → filtered list |
| A12.3 | Dashboard data export | MED | Export summary to CSV/PDF |
| A12.4 | Comparison period (MoM, YoY) | LOW | So sánh với kỳ trước |
| A12.5 | Custom dashboard layout | LOW | User tự chọn widgets |

---

### A13. Reports (routers/reports.py) — ⚠️ CONFIG ONLY, KHÔNG GENERATE

**Có:** Config CRUD • Run (bump counter) • Audit log read

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A13.1 | Actual report generation engine | CRITICAL | `/run` chỉ bump run_count, không generate báo cáo |
| A13.2 | Export to XLSX/PDF/HTML | CRITICAL | Config fields tồn tại nhưng không render |
| A13.3 | Scheduled report delivery | HIGH | DAILY/WEEKLY/MONTHLY configs nhưng không wire vào scheduler |
| A13.4 | Report template system | MED | Pre-built templates cho PIPELINE, SLA, KHKD |
| A13.5 | DELETE config | LOW | Config tạo thử không xóa được |

---

### A14. IO/Import-Export (routers/io_router.py) — ⚠️ HẠN CHẾ

**Có:** Import customers/contacts (CSV) • Export customers/contacts/opportunities/quotations (CSV)

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A14.1 | XLSX import | HIGH | Hầu hết source data là Excel |
| A14.2 | Import opportunities, tasks, contracts | HIGH | Chỉ import customers/contacts |
| A14.3 | Export tasks, contracts, milestones, commissions, follow-ups | MED | Chỉ export 4 entity types |
| A14.4 | Import preview/dry-run with UI | MED | Dry-run mode tồn tại nhưng không có UI |
| A14.5 | Progress tracking cho large imports | LOW | Không biết tiến độ import file lớn |

---

### A15. Templates (routers/templates.py) — ⚠️ THIẾU RENDER

**Có:** Quote template CRUD • Email template CRUD • Seed defaults

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A15.1 | Template render/preview endpoint | HIGH | Store template nhưng không render với variables |
| A15.2 | DELETE | MED | Template cũ không xóa được |
| A15.3 | Template clone/duplicate | LOW | Copy template làm base cho bản mới |
| A15.4 | Variable validation | LOW | Check template variables vs available data fields |

---

### A16. Notifications (routers/notifications.py) — ⚠️ THIẾU TRIGGERS

**Có:** List • Count • Mark read • Mark all read

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A16.1 | Notification triggers cho events chính | CRITICAL | Chỉ inter_dept gọi notify.py. THIẾU: opportunity stage change, task assigned, SLA breach, follow-up due, commission status, quotation sent |
| A16.2 | Notification preferences per user | HIGH | User chọn loại notification muốn nhận |
| A16.3 | Email notification delivery | MED | Hiện chỉ in-app, không gửi email |
| A16.4 | DELETE/dismiss notification | LOW | Mark read tồn tại nhưng không dismiss/delete |

---

### A17. Search (routers/search.py) — ✅ OK

**Có:** Global search across 5 entity types (customer, contact, opportunity, quotation, email)

**Thiếu:**
| # | Feature | Mức độ | Lý do cần |
|---|---------|--------|-----------|
| A17.1 | Search result deep links | HIGH | Trả entity_id nhưng UI không navigate được |
| A17.2 | Search filters (by entity type, date range) | MED | Hiện search tất cả, không filter |
| A17.3 | Recent searches | LOW | Lưu search history |
| A17.4 | Search suggestions/autocomplete | LOW | Gợi ý khi gõ |

---

### A18. Services Layer — CROSS-CUTTING GAPS

| # | Service | Gap | Mức độ |
|---|---------|-----|--------|
| A18.1 | state_machine.py | Chỉ cover 3 entities (opp, task, quotation). Thiếu: contract, settlement, follow-up, commission, IDT → cần consolidate TẤT CẢ transitions vào 1 service | CRITICAL |
| A18.2 | notify.py | Chỉ được gọi từ 1 router (inter_dept). Cần trigger từ 10+ events | CRITICAL |
| A18.3 | sla_engine.py | Không connected vào task creation. Workers dùng nhưng service layer bị bypass | HIGH |
| A18.4 | audit.py | changed_by luôn = None vì identity resolution yếu. Cần extract user_id từ API key context | HIGH |
| A18.5 | gmail_service.py | DRAFT only (đúng rule #8) nhưng thiếu: attachment handling, template rendering | MED |

---

## PHẦN B: FRONTEND — AUDIT TỪNG TRANG

### B1. sale_dashboard.html (Main SPA) — ⚠️ THIẾU HÀNH ĐỘNG

Trang SPA chính với 7 screens. Đây là trang user sẽ dùng hàng ngày.

| Screen | Xem | Tạo | Sửa | Xóa | Transition | Gap Level |
|--------|-----|-----|-----|-----|------------|-----------|
| Dashboard | ✅ 8 KPIs | ❌ | ❌ | ❌ | ❌ | MED — thiếu drill-down, date filter |
| My Day | ✅ 4 KPIs | ❌ | ❌ | ❌ | ❌ | HIGH — items không clickable |
| Customers | ✅ List + detail | ✅ Create | ❌ No edit | ❌ | ❌ | CRITICAL — detail read-only |
| Pipeline | ✅ List + detail | ❌ No create | ❌ No edit | ❌ | ❌ No buttons | CRITICAL — shows stages but can't move |
| Quotations | ✅ List + stats | ✅ Create | ❌ No edit | ❌ | ❌ | CRITICAL — no detail view, no status flow |
| Tasks | ✅ Kanban | ❌ No create | ❌ No edit | ❌ | ❌ No drag | CRITICAL — completely static |
| Search | ✅ Results | — | — | — | — | HIGH — results don't link anywhere |

**Tổng kết SPA:** Hầu hết screens là READ-ONLY. User chỉ có thể: login, xem dashboard, tạo customer, tạo quotation, search (nhưng results dead-end), mark notifications read. **Không thể thực hiện bất kỳ workflow nào end-to-end.**

---

### B2. Standalone Pages — PHÂN MẢNH

| Page | Điểm mạnh | Điểm yếu |
|------|-----------|-----------|
| **email-hub.html** | 3-panel Outlook-style, filters, thread view, create-task, link-to-opp | No compose/reply, no search, no bulk actions |
| **task-board.html** | Kanban 5 columns, drag-drop, create task, filter by dept/assignee | No detail view, no edit, no comments |
| **project-board.html** | Rich cards, stage transition buttons, detail modal with milestones | No create opp, no edit fields, no pagination |
| **pipeline.html** | 4 analytics sections, KHKD comparison, funnel | Entirely read-only, targets hardcoded |
| **index.html** | Dev tool: create opp/task/user, API tester | Raw API key visible, no production UX |

**Frontend Architecture Problems:**
1. **2 design systems:** SPA (dark theme) vs standalone pages (light theme) — user confusion
2. **No shared navigation:** sale_dashboard.html self-contained, standalone pages only link "Home" → index.html
3. **Auth inconsistency:** SPA uses sessionStorage login, standalone pages expose raw API key input
4. **Feature duplication + fragmentation:** Tasks exist in SPA (broken kanban) AND task-board.html (working kanban). Pipeline exists in SPA (broken) AND project-board.html (working with transitions)

---

## PHẦN C: WORKFLOW END-TO-END — CÁI GÌ CHẠY ĐƯỢC?

Đánh giá 10 daily workflows của Sale team:

### W1. "Sáng đến công ty, xem tổng quan pipeline"
- **Luồng:** Login SPA → Dashboard → xem KPIs
- **Status:** ✅ WORKS nhưng chỉ đọc, không drill-down

### W2. "Nhận RFQ email, tạo opportunity mới"
- **Luồng:** Email hub → đọc email → tạo opportunity → link email
- **Status:** ❌ BROKEN — Email hub không link đến SPA. SPA không có create opportunity. Index.html có create nhưng không link email.

### W3. "Tạo quotation cho opportunity"
- **Luồng:** Pipeline → chọn opportunity → Create quotation
- **Status:** ❌ BROKEN — SPA quotation create không có opportunity_id field. Không navigate được từ pipeline → quotation.

### W4. "Chuyển opportunity từ QUOTED → NEGOTIATION"
- **Luồng:** Pipeline → chọn opportunity → click transition button
- **Status:** ⚠️ PARTIAL — project-board.html (standalone) CÓ transition buttons. sale_dashboard.html (SPA) KHÔNG CÓ.

### W5. "Giao task cho team member từ opportunity"
- **Luồng:** Pipeline → opportunity detail → Create task
- **Status:** ❌ BROKEN — Không có "Create task" button trong bất kỳ opportunity detail view nào. Task creation chỉ ở task-board.html (standalone) hoặc index.html (dev).

### W6. "Xem task board, cập nhật trạng thái"
- **Luồng:** Tasks → drag task → new status
- **Status:** ⚠️ PARTIAL — task-board.html (standalone) CÓ drag-drop. sale_dashboard.html (SPA) kanban KHÔNG drag-drop.

### W7. "Log cuộc gọi khách hàng"
- **Luồng:** Customer → detail → Add interaction
- **Status:** ❌ BROKEN — Customer detail is read-only. Không có "Add interaction" button. Backend có endpoint nhưng không có UI.

### W8. "Follow-up khách hàng quá hạn"
- **Luồng:** Dashboard → follow-up overdue → action
- **Status:** ❌ BROKEN — Dashboard shows follow-up count nhưng không link đến list. Không có follow-up management screen.

### W9. "Export pipeline report cho sếp"
- **Luồng:** Dashboard/Reports → export PDF/XLSX
- **Status:** ❌ BROKEN — Report engine không generate. Chỉ CSV export cho 4 entity types.

### W10. "Commission review cuối tháng"
- **Luồng:** Commissions → review → approve → mark paid
- **Status:** ❌ NO UI — Backend endpoints tồn tại nhưng không có trang commission nào.

**Kết quả: 1/10 workflows chạy đầy đủ. 2/10 chạy partial. 7/10 broken hoặc không có UI.**

---

## PHẦN D: MISSING "GLUE" FEATURES — KẾT NỐI GIỮA CÁC MODULE

Đây là các features không thuộc module nào cụ thể nhưng THIẾU sẽ khiến hệ thống rời rạc:

| # | Glue Feature | From → To | Mức độ | Mô tả |
|---|-------------|-----------|--------|-------|
| D1 | Create Opportunity from Email | Email → Opportunity | CRITICAL | Nhận RFQ email → 1 click tạo opportunity với pre-filled customer, subject |
| D2 | Create Quotation from Opportunity | Opportunity → Quotation | CRITICAL | Từ opp detail → 1 click tạo quotation kế thừa customer, project, value |
| D3 | Create Task from Opportunity | Opportunity → Task | HIGH | Từ opp detail → tạo task (follow-up, costing, review) |
| D4 | Create Follow-up from Customer/Opportunity | Customer/Opp → Follow-up | HIGH | Lên lịch follow-up trực tiếp từ context |
| D5 | Create Contract from Won Opportunity | Opportunity WON → Contract | CRITICAL | Auto-create contract skeleton khi opportunity WON |
| D6 | Calculate Commission from Won Opportunity | Opportunity WON → Commission | HIGH | Auto-trigger commission calculation |
| D7 | Convert Market Signal to Opportunity | Intelligence → Opportunity | MED | Từ signal → tạo opportunity mới |
| D8 | Navigate Search Result to Detail | Search → Any entity | HIGH | Click search result → open detail view |
| D9 | Customer 360° View | All modules → Customer | HIGH | Unified view: contacts, opps, quotations, tasks, emails, interactions, follow-ups, contracts |
| D10 | Opportunity 360° View | All modules → Opportunity | HIGH | Unified view: quotation revisions, tasks, emails, milestones, follow-ups |
| D11 | Notification → Source navigation | Notification → Any entity | MED | Click notification → navigate đến entity liên quan |
| D12 | Dashboard KPI → Filtered list | Dashboard → List views | MED | Click "5 overdue tasks" → task list filtered overdue |

---

## PHẦN E: FRONTEND CONSOLIDATION PLAN

### Recommendation: Hợp nhất tất cả vào sale_dashboard.html (SPA)

**Hiện tại:** 6 pages rời rạc, user phải nhớ URL nào để làm gì.

**Đề xuất:** Mở rộng SPA thành 14 screens:

| # | Screen | Route | Cần thêm | Priority |
|---|--------|-------|----------|----------|
| 1 | Dashboard | #dashboard | Date filter, drill-down links | P1 |
| 2 | My Day | #my | Clickable items, quick-create task | P1 |
| 3 | Customers | #customers | Edit modal, add contact, add interaction, 360° view | P1 |
| 4 | Pipeline | #pipeline | Create opp, edit fields, stage transition buttons, create quotation from opp | P1 |
| 5 | Quotations | #quotations | Detail modal, edit, status flow (DRAFT→SENT→WON/LOST), revision management | P1 |
| 6 | Tasks | #tasks | Port task-board.html drag-drop, create, detail view, edit, comments | P1 |
| 7 | Emails | #emails | Port email-hub.html 3-panel layout, compose, search | P1 |
| 8 | Contracts | #contracts | List, detail, milestone tracking, settlement management | P2 |
| 9 | Follow-ups | #followups | Calendar view, create, edit, overdue alerts | P2 |
| 10 | Search | #search | Fix dead-end links, entity type filters | P1 |
| 11 | Commissions | #commissions | List, calculate, approve, pay | P2 |
| 12 | Reports | #reports | Config, generate, download, schedule | P2 |
| 13 | Inter-dept | #inter-dept | Port inter_dept board | P3 |
| 14 | Settings | #settings | User profile, notification preferences, SLA config | P3 |

**Navigation consolidation:**
- Sidebar: Dashboard, My Day, Customers, Pipeline, Quotations, Tasks, Emails, Contracts, Reports (P1+P2)
- Topbar: Search, Notifications, User menu (settings, logout)
- Context menus: Right-click / "..." button cho entity actions

---

## PHẦN F: TỔNG HỢP GAPS — PRIORITIZED ACTION ITEMS

### CRITICAL (Hệ thống không thể daily-use nếu thiếu)

| # | Item | Backend | Frontend | Est. Hours |
|---|------|---------|----------|------------|
| F1 | Consolidate state machine (all 7 entity types) | ✅ Cần | — | 4h |
| F2 | Notification triggers (10+ events) | ✅ Cần | — | 4h |
| F3 | Opportunity WIN/LOSS side effects (→ contract, commission) | ✅ Cần | — | 6h |
| F4 | Quotation → Opportunity link + WIN/LOSS/SEND actions | ✅ Cần | — | 4h |
| F5 | Settlement UPDATE endpoint | ✅ Cần | — | 2h |
| F6 | Commission approval require_admin gate | ✅ Cần | — | 1h |
| F7 | Report generation engine (at least XLSX) | ✅ Cần | — | 8h |
| F8 | SPA: Customer edit + 360° view | — | ✅ Cần | 6h |
| F9 | SPA: Pipeline create/edit/transition | — | ✅ Cần | 6h |
| F10 | SPA: Quotation detail + status flow | — | ✅ Cần | 6h |
| F11 | SPA: Tasks port from task-board.html (drag-drop, create, detail) | — | ✅ Cần | 6h |
| F12 | SPA: Emails port from email-hub.html | — | ✅ Cần | 8h |
| | **CRITICAL subtotal** | | | **~61h** |

### HIGH (Daily-use chạy nhưng thiếu nhiều chức năng)

| # | Item | Backend | Frontend | Est. Hours |
|---|------|---------|----------|------------|
| F13 | Soft-delete endpoints (all entities) | ✅ | — | 4h |
| F14 | Task detail endpoint + SLA integration | ✅ | — | 3h |
| F15 | Follow-up: customer-only, detail, reminders | ✅ | — | 4h |
| F16 | Change order CRUD + KHKD target CRUD | ✅ | — | 4h |
| F17 | Glue: Create-from-context (D1-D6) | ✅ | ✅ | 8h |
| F18 | Contact search/filter + delete | ✅ | — | 2h |
| F19 | Email full-text search | ✅ | — | 3h |
| F20 | Dashboard date range filter | ✅ | ✅ | 3h |
| F21 | Search results → detail navigation | — | ✅ | 3h |
| F22 | Intelligence: acknowledge, convert-to-opp | ✅ | — | 3h |
| F23 | Audit changed_by from auth context | ✅ | — | 2h |
| F24 | SPA: Contracts screen | — | ✅ | 6h |
| F25 | SPA: Follow-ups screen | — | ✅ | 4h |
| | **HIGH subtotal** | | | **~49h** |

### MEDIUM (Professional polish)

| # | Item | Backend | Frontend | Est. Hours |
|---|------|---------|----------|------------|
| F26 | Import: XLSX + opportunities/tasks | ✅ | — | 6h |
| F27 | Export: tasks/contracts/commissions/follow-ups + XLSX format | ✅ | — | 4h |
| F28 | Template render/preview | ✅ | — | 3h |
| F29 | Commission: batch approve, DB tiers | ✅ | — | 3h |
| F30 | IDT: auto-advance workflow steps | ✅ | — | 2h |
| F31 | SLA: DB-driven config, per-customer override | ✅ | — | 3h |
| F32 | Customer merge duplicates | ✅ | ✅ | 4h |
| F33 | Dashboard comparison period | ✅ | ✅ | 3h |
| F34 | SPA: Commissions screen | — | ✅ | 4h |
| F35 | SPA: Reports screen | — | ✅ | 4h |
| F36 | Inline models → models/ consolidation | ✅ | — | 4h |
| F37 | Notification preferences per user | ✅ | ✅ | 3h |
| F38 | Request logging middleware | ✅ | — | 2h |
| | **MEDIUM subtotal** | | | **~45h** |

---

## PHẦN G: RECOMMENDED EXECUTION ORDER

### Phase 1A — Backend Foundation (Tuần 1-2, ~25h)
1. F1: Consolidate state machine
2. F2: Notification triggers
3. F6: Commission admin gate
4. F13: Soft-delete all entities
5. F23: Audit changed_by fix
6. F14: Task detail + SLA
7. F18: Contact search + delete
8. F5: Settlement update

### Phase 1B — Backend Workflows (Tuần 2-3, ~24h)
9. F3: Opportunity WIN/LOSS side effects
10. F4: Quotation actions (link + WIN/LOSS/SEND)
11. F15: Follow-up improvements
12. F16: Change order + KHKD CRUD
13. F17: Create-from-context endpoints (D1-D6)
14. F19: Email search
15. F22: Intelligence actions

### Phase 1C — Frontend SPA Consolidation (Tuần 3-5, ~40h)
16. F8: Customer edit + 360°
17. F9: Pipeline create/edit/transition
18. F10: Quotation detail + flow
19. F11: Tasks port
20. F12: Emails port
21. F20: Dashboard date filter
22. F21: Search → detail navigation

### Phase 2 — Reports + Polish (Tuần 5-7, ~36h)
23. F7: Report generation engine
24. F24: Contracts screen
25. F25: Follow-ups screen
26. F34: Commissions screen
27. F35: Reports screen
28. F26-F27: Import/export expansion

### Phase 3 — Professional Features (Tuần 7-9, ~24h)
29. F28-F38: Template render, SLA config, merge duplicates, comparison, models consolidation, middleware, etc.

---

## PHẦN H: SO SÁNH VỚI UNIFIED_CLAUDE_CODE_COMMAND.md

UNIFIED_CLAUDE_CODE_COMMAND.md hiện có 18 steps, ~65.5h. Audit này phát hiện thêm:

| Category | UNIFIED covers | Audit finds thêm | Gap |
|----------|---------------|-------------------|-----|
| Backend CRUD gaps | Partial (Step 8-9) | Full per-entity analysis | +20h backend |
| State machine | Step 1 (consolidate 3) | Need 7 entity types | +2h |
| Notifications | Step 3 (trigger 5 events) | Need 10+ events | +2h |
| Opportunity side effects | Not covered | WIN→contract+commission, LOSS→reason | +6h |
| Frontend SPA | Step 14 (improve 5 screens) | Need 14 screens, full CRUD each | +30h |
| Reports engine | Not covered | Config→Generate→Export→Schedule | +8h |
| Glue features (D1-D12) | Partial (D1-D3 mentioned) | 12 cross-module links | +4h |
| **TOTAL additional** | | | **~72h** |

**Kết luận:** UNIFIED_CLAUDE_CODE_COMMAND cần update thêm ~72h effort, nâng tổng từ ~65h lên ~137h cho hệ thống hoàn chỉnh daily-use.

---

## PHỤ LỤC: TOÀN BỘ ENDPOINTS HIỆN CÓ (146)

<details>
<summary>Click để xem danh sách đầy đủ 146 endpoints</summary>

### Auth (2)
- `GET /auth/me`
- `GET /auth/info`

### Customers (11)
- `GET /customers` — List (region, status filter, pagination)
- `GET /customers/search` — UNION search with contacts
- `GET /customers/duplicates` — Token-overlap algorithm
- `GET /customers/{id}` — Detail with sub-resources
- `GET /customers/{id}/contacts`
- `GET /customers/{id}/interactions`
- `GET /customers/{id}/quotations`
- `GET /customers/{id}/contracts`
- `POST /customers` — Create (auto-code, duplicate check)
- `PATCH /customers/{id}` — Update (code uniqueness, audit)
- `DELETE /customers/{id}` — Soft delete (admin only)

### Contacts (5)
- `GET /contacts` — List
- `GET /contacts/duplicates` — Email/phone normalization
- `GET /contacts/{id}` — Detail
- `POST /contacts` — Create (auto-demote primary)
- `PATCH /contacts/{id}` — Update

### Opportunities (5)
- `GET /opportunities` — List (stage, product, assigned filter)
- `GET /opportunities/stale` — Stale detection
- `GET /opportunities/{id}` — Detail with allowed_next_stages
- `POST /opportunities` — Create
- `PATCH /opportunities/{id}` — Update (state machine validated)

### Quotations (8)
- `GET /quotations` — List history
- `GET /quotations/win-rate` — Win rate stats
- `GET /quotations/{id}` — Detail
- `GET /quotations/revisions/list` — All revisions
- `GET /quotations/by-opportunity/{opp_id}/revisions`
- `POST /quotations` — Create
- `PATCH /quotations/{id}` — Update
- `POST /quotations/{id}/revise` — Create revision

### Tasks (6)
- `GET /tasks` — List
- `GET /tasks/board` — Kanban data
- `GET /tasks/my` — Personal tasks (query param user)
- `POST /tasks` — Create (with email/opp link)
- `PATCH /tasks/{id}` — Update (state machine)
- `POST /tasks/{id}/escalate`

### Emails (11)
- `GET /emails` — List (type, status, date filter)
- `GET /emails/{id}` — Detail
- `POST /emails/sync` — Trigger Gmail sync
- `PATCH /emails/{id}` — Update (read/actioned)
- `POST /emails/{id}/create-task` — Create task from email
- `GET /emails/labels` — Label list
- `GET /emails/full` — Full email records
- `GET /emails/follow-ups` — Follow-up view
- `POST /emails/compose` — Create DRAFT
- `POST /emails/render-reply` — Render reply template
- `GET /emails/project-activity` — Activity view

### Contracts (15)
- `GET /contracts` — List active
- `GET /contracts/{id}` — Detail
- `GET /contracts/{id}/milestones`
- `GET /contracts/{id}/settlements`
- `GET /contracts/milestones` — Global milestones
- `GET /contracts/milestones/{id}`
- `GET /contracts/settlements` — Global settlements
- `GET /contracts/settlements/{id}`
- `GET /contracts/change-orders`
- `GET /contracts/khkd-targets`
- `POST /contracts` — Create
- `PATCH /contracts/{id}` — Update
- `POST /contracts/{id}/milestones` — Create milestone
- `PATCH /contracts/{id}/milestones/{id}` — Update milestone
- `POST /contracts/{id}/settlements` — Create settlement

### Follow-ups (4)
- `GET /follow-ups` — List
- `GET /follow-ups/overdue`
- `POST /follow-ups` — Create
- `PATCH /follow-ups/{id}` — Update

### Commissions (6)
- `GET /commissions` — List
- `GET /commissions/by-salesperson`
- `GET /commissions/{id}` — Detail
- `POST /commissions/calculate` — Auto-calc
- `POST /commissions` — Manual create
- `PATCH /commissions/{id}` — Update

### Inter-dept Tasks (6)
- `GET /inter-dept` — List
- `GET /inter-dept/board` — Kanban
- `GET /inter-dept/{id}` — Detail
- `POST /inter-dept` — Create
- `PATCH /inter-dept/{id}` — Update
- `POST /inter-dept/{id}/escalate`

### Intelligence (5 + 2 aliases)
- `GET /intelligence/signals` (alias `/market-signals`)
- `GET /intelligence/market-signals/{id}`
- `GET /intelligence/products` (alias `/product-opportunities`)
- `GET /intelligence/digital-content`
- `GET /intelligence/product-categories`

### Dashboard (8)
- `GET /dashboard/pipeline`
- `GET /dashboard/pipeline/by-product`
- `GET /dashboard/pipeline/by-quarter`
- `GET /dashboard/tasks`
- `GET /dashboard/emails`
- `GET /dashboard/executive`
- `GET /dashboard/summary`
- `GET /dashboard/my`

### Mailboxes (4)
- `GET /mailboxes` — List
- `POST /mailboxes` — Create
- `PATCH /mailboxes/{id}` — Update
- `POST /mailboxes/{id}/oauth` — OAuth flow

### Users (4)
- `GET /users` — List
- `POST /users` — Create
- `POST /users/seed-defaults`
- `PATCH /users/{id}` — Update

### Notifications (4)
- `GET /notifications` — List
- `GET /notifications/count`
- `PATCH /notifications/{id}/read`
- `PATCH /notifications/read-all`

### Search (1)
- `GET /search` — Global search 5 entity types

### PM Integration (6)
- `GET /pm/project/{opp_id}/status`
- `POST /pm/project/{opp_id}/create-task`
- `GET /pm/project/{opp_id}/timeline`
- `POST /pm/project/{opp_id}/draft-reply`
- `POST /pm/project/{opp_id}/approve-draft`
- `GET /pm/sync-log`

### IO (7)
- `POST /io/import/customers` — CSV import
- `POST /io/import/contacts` — CSV import
- `GET /io/export/customers` — CSV
- `GET /io/export/contacts` — CSV
- `GET /io/export/opportunities` — CSV
- `GET /io/export/quotations` — CSV
- `GET /io/import/log`

### Reports (8)
- `GET /reports/configs` — List
- `GET /reports/configs/{id}`
- `POST /reports/configs` — Create
- `PATCH /reports/configs/{id}` — Update
- `POST /reports/configs/{id}/run`
- `GET /reports/audit-log`
- `GET /reports/audit-log/{entity_type}/{entity_id}`
- `GET /reports/audit-log/summary`

### Templates (9)
- `GET /templates/quote`
- `GET /templates/quote/{id}`
- `POST /templates/quote`
- `PATCH /templates/quote/{id}`
- `GET /templates/email`
- `GET /templates/email/{type}`
- `POST /templates/email`
- `PATCH /templates/email/{type}`
- `POST /templates/email/seed-defaults`

### Files (4)
- `GET /files` — List NAS links
- `GET /files/{id}`
- `POST /files` — Create link
- `DELETE /files/{id}`

### Interactions (4)
- `GET /interactions`
- `GET /interactions/{id}`
- `POST /interactions`
- `PATCH /interactions/{id}`

### Health (1)
- `GET /health`

</details>

---

*Document generated by AI Chief of Staff. Cần review bởi Chairman trước khi merge vào UNIFIED_CLAUDE_CODE_COMMAND.md.*
