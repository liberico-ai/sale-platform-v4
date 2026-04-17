"""E2E Test Suite — 10 flows for IBS HI Sale Platform."""
import uuid


# ═══════════════════════════════════════════════════════════
# FLOW 1: Health + Customers
# ═══════════════════════════════════════════════════════════

def test_flow1_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["db_type"] == "sqlite"


def test_flow1_customers_list(client, admin_headers):
    r = client.get("/api/v1/customers", headers=admin_headers)
    assert r.status_code == 200
    data = r.json()
    assert "total" in data
    assert "items" in data


# ═══════════════════════════════════════════════════════════
# FLOW 2: Pipeline Lifecycle (PROSPECT → WON)
# ═══════════════════════════════════════════════════════════

def test_flow2_pipeline_lifecycle(client, admin_headers):
    # Create opportunity
    r = client.post("/api/v1/opportunities", headers=admin_headers, json={
        "project_name": "Test Pipeline Flow",
        "customer_name": "Test Customer",
        "product_group": "HRSG",
        "stage": "PROSPECT",
    })
    assert r.status_code == 200
    opp_id = r.json()["id"]

    # Progress through all stages
    stages = ["CONTACTED", "RFQ_RECEIVED", "COSTING", "QUOTED", "NEGOTIATION", "WON"]
    for stage in stages:
        r = client.patch(f"/api/v1/opportunities/{opp_id}", headers=admin_headers,
                         json={"stage": stage})
        assert r.status_code == 200, f"Failed transition to {stage}: {r.json()}"

    # Verify final state
    r = client.get(f"/api/v1/opportunities/{opp_id}", headers=admin_headers)
    assert r.status_code == 200
    assert r.json()["opportunity"]["stage"] == "WON"


# ═══════════════════════════════════════════════════════════
# FLOW 3: Invalid State Transition
# ═══════════════════════════════════════════════════════════

def test_flow3_invalid_transition(client, admin_headers):
    # Create at PROSPECT
    r = client.post("/api/v1/opportunities", headers=admin_headers, json={
        "project_name": "Invalid Transition Test",
        "customer_name": "Test",
        "product_group": "PV",
    })
    opp_id = r.json()["id"]

    # Try to jump directly to WON
    r = client.patch(f"/api/v1/opportunities/{opp_id}", headers=admin_headers,
                     json={"stage": "WON"})
    assert r.status_code == 422
    assert "detail" in r.json()


# ═══════════════════════════════════════════════════════════
# FLOW 4: Task Lifecycle (PENDING → IN_PROGRESS → COMPLETED)
# ═══════════════════════════════════════════════════════════

def test_flow4_task_lifecycle(client, admin_headers):
    # Create task
    r = client.post("/api/v1/tasks", headers=admin_headers, json={
        "task_type": "GENERAL",
        "title": "Test Task Flow",
        "from_dept": "SALE",
        "to_dept": "KTKH",
        "priority": "NORMAL",
    })
    assert r.status_code == 200
    task_id = r.json()["id"]

    # PENDING → IN_PROGRESS
    r = client.patch(f"/api/v1/tasks/{task_id}", headers=admin_headers,
                     json={"status": "IN_PROGRESS"})
    assert r.status_code == 200

    # IN_PROGRESS → COMPLETED
    r = client.patch(f"/api/v1/tasks/{task_id}", headers=admin_headers,
                     json={"status": "COMPLETED"})
    assert r.status_code == 200

    # COMPLETED → PENDING should fail (terminal state)
    r = client.patch(f"/api/v1/tasks/{task_id}", headers=admin_headers,
                     json={"status": "PENDING"})
    assert r.status_code == 422


# ═══════════════════════════════════════════════════════════
# FLOW 5: Dashboard Data (6 endpoints)
# ═══════════════════════════════════════════════════════════

def test_flow5_dashboard_pipeline(client, admin_headers):
    r = client.get("/api/v1/dashboard/pipeline", headers=admin_headers)
    assert r.status_code == 200


def test_flow5_dashboard_by_product(client, admin_headers):
    r = client.get("/api/v1/dashboard/pipeline/by-product", headers=admin_headers)
    assert r.status_code == 200


def test_flow5_dashboard_by_quarter(client, admin_headers):
    r = client.get("/api/v1/dashboard/pipeline/by-quarter", headers=admin_headers)
    assert r.status_code == 200


def test_flow5_dashboard_tasks(client, admin_headers):
    r = client.get("/api/v1/dashboard/tasks", headers=admin_headers)
    assert r.status_code == 200


def test_flow5_dashboard_emails(client, admin_headers):
    r = client.get("/api/v1/dashboard/emails", headers=admin_headers)
    assert r.status_code == 200


def test_flow5_dashboard_executive(client, admin_headers):
    r = client.get("/api/v1/dashboard/executive", headers=admin_headers)
    assert r.status_code == 200


# ═══════════════════════════════════════════════════════════
# FLOW 6: Mailbox Management
# ═══════════════════════════════════════════════════════════

def test_flow6_mailbox_management(client, admin_headers):
    # List mailboxes
    r = client.get("/api/v1/mailboxes", headers=admin_headers)
    assert r.status_code == 200

    # Create mailbox
    email = f"test-{uuid.uuid4().hex[:8]}@ibs.com.vn"
    r = client.post("/api/v1/mailboxes", headers=admin_headers, json={
        "email_address": email,
        "mailbox_type": "SHARED",
        "department": "SALE",
    })
    assert r.status_code == 200
    mb_id = r.json()["id"]

    # Update: disable sync
    r = client.patch(f"/api/v1/mailboxes/{mb_id}", headers=admin_headers,
                     json={"sync_enabled": False})
    assert r.status_code == 200

    # Deactivate
    r = client.patch(f"/api/v1/mailboxes/{mb_id}", headers=admin_headers,
                     json={"is_active": False})
    assert r.status_code == 200


# ═══════════════════════════════════════════════════════════
# FLOW 7: User Management
# ═══════════════════════════════════════════════════════════

def test_flow7_user_management(client, admin_headers):
    # List users
    r = client.get("/api/v1/users", headers=admin_headers)
    assert r.status_code == 200

    # Create user
    email = f"test-{uuid.uuid4().hex[:8]}@ibs.com.vn"
    r = client.post("/api/v1/users", headers=admin_headers, json={
        "user_name": "Test User",
        "email": email,
        "department": "SALE",
        "role": "MEMBER",
    })
    assert r.status_code == 200
    user_id = r.json()["id"]

    # Update role
    r = client.patch(f"/api/v1/users/{user_id}", headers=admin_headers,
                     json={"role": "MANAGER"})
    assert r.status_code == 200

    # Deactivate
    r = client.patch(f"/api/v1/users/{user_id}", headers=admin_headers,
                     json={"is_active": False})
    assert r.status_code == 200


# ═══════════════════════════════════════════════════════════
# FLOW 8: Auth Tier Enforcement
# ═══════════════════════════════════════════════════════════

def test_flow8_viewer_can_read_customers(client, viewer_headers):
    r = client.get("/api/v1/customers", headers=viewer_headers)
    assert r.status_code == 200


def test_flow8_viewer_can_read_dashboard(client, viewer_headers):
    r = client.get("/api/v1/dashboard/pipeline", headers=viewer_headers)
    assert r.status_code == 200


def test_flow8_viewer_blocked_from_opportunities(client, viewer_headers):
    r = client.post("/api/v1/opportunities", headers=viewer_headers, json={
        "project_name": "Blocked",
        "customer_name": "Blocked",
        "product_group": "PV",
    })
    assert r.status_code == 403


def test_flow8_viewer_blocked_from_tasks(client, viewer_headers):
    r = client.post("/api/v1/tasks", headers=viewer_headers, json={
        "task_type": "GENERAL",
        "title": "Blocked",
        "from_dept": "SALE",
        "to_dept": "SALE",
    })
    assert r.status_code == 403


def test_flow8_manager_can_create_opportunity(client, manager_headers):
    r = client.post("/api/v1/opportunities", headers=manager_headers, json={
        "project_name": "Manager Test",
        "customer_name": "Manager Customer",
        "product_group": "HRSG",
    })
    assert r.status_code == 200


def test_flow8_no_key_rejected(client):
    r = client.get("/api/v1/customers")
    assert r.status_code in (401, 403)


# ═══════════════════════════════════════════════════════════
# FLOW 9: NAS File Linking
# ═══════════════════════════════════════════════════════════

def test_flow9_nas_file_crud(client, admin_headers):
    entity_id = str(uuid.uuid4())

    # Create link
    r = client.post("/api/v1/nas-files", headers=admin_headers, json={
        "entity_type": "opportunity",
        "entity_id": entity_id,
        "nas_path": r"\\192.168.0.200\Sales\test.pdf",
        "file_name": "test.pdf",
        "file_type": "QUOTATION",
    })
    assert r.status_code == 201
    file_id = r.json()["id"]

    # List by entity
    r = client.get(f"/api/v1/nas-files?entity_type=opportunity&entity_id={entity_id}",
                   headers=admin_headers)
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    # Get single
    r = client.get(f"/api/v1/nas-files/{file_id}", headers=admin_headers)
    assert r.status_code == 200
    assert r.json()["file_name"] == "test.pdf"

    # Delete
    r = client.delete(f"/api/v1/nas-files/{file_id}", headers=admin_headers)
    assert r.status_code == 200

    # Verify deleted
    r = client.get(f"/api/v1/nas-files/{file_id}", headers=admin_headers)
    assert r.status_code == 404


def test_flow9_nas_invalid_entity_type(client, admin_headers):
    r = client.get("/api/v1/nas-files?entity_type=invalid&entity_id=x",
                   headers=admin_headers)
    assert r.status_code == 422


# ═══════════════════════════════════════════════════════════
# FLOW 10: Stale Deal Detection
# ═══════════════════════════════════════════════════════════

def test_flow10_stale_deals(client, admin_headers):
    # Create opportunity with old activity date
    r = client.post("/api/v1/opportunities", headers=admin_headers, json={
        "project_name": "Stale Deal Test",
        "customer_name": "Old Customer",
        "product_group": "DUCT",
    })
    opp_id = r.json()["id"]

    # Manually flag as stale via direct DB (simulate worker)
    import importlib, os
    _pkg = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
    db_mod = importlib.import_module(f"{_pkg}.database")
    execute = db_mod.execute
    execute("UPDATE sale_opportunities SET stale_flag = 1, last_activity_date = '2026-01-01T00:00:00' WHERE id = ?", [opp_id])

    # Check stale endpoint
    r = client.get("/api/v1/opportunities/stale", headers=admin_headers)
    assert r.status_code == 200
    data = r.json()
    stale_ids = [item["id"] for item in data["items"]]
    assert opp_id in stale_ids
