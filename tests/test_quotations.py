"""Tests for /api/v1/quotations — state machine + CRUD."""


def test_quotations_requires_auth(client):
    r = client.get("/api/v1/quotations")
    assert r.status_code == 401


def test_quotations_list(client, admin_headers):
    r = client.get("/api/v1/quotations", headers=admin_headers)
    assert r.status_code == 200
    data = r.json()
    assert "total" in data and "items" in data and "limit" in data and "offset" in data


def test_quotation_create(client, admin_headers):
    r = client.post(
        "/api/v1/quotations",
        headers=admin_headers,
        json={
            "project_name": "Test Quotation Flow",
            "customer_name": "Test Customer",
            "value_usd": 100000,
            "incharge": "tester",
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["status"] == "DRAFT"
    assert "id" in data and "quotation_no" in data


def test_quotation_invalid_body(client, admin_headers):
    # Missing both customer_id and customer_code/customer_name → 400
    r = client.post(
        "/api/v1/quotations",
        headers=admin_headers,
        json={"project_name": "Missing customer info"},
    )
    assert r.status_code == 400


def test_quotation_state_machine_draft_to_won(client, admin_headers):
    # Create DRAFT
    r = client.post(
        "/api/v1/quotations",
        headers=admin_headers,
        json={
            "project_name": "State Machine Test",
            "customer_name": "Test SM",
            "value_usd": 50000,
        },
    )
    assert r.status_code == 200
    q_id = r.json()["id"]

    # DRAFT → SENT
    r = client.patch(
        f"/api/v1/quotations/{q_id}",
        headers=admin_headers,
        json={"status": "SENT"},
    )
    assert r.status_code == 200, r.text

    # SENT → WON
    r = client.patch(
        f"/api/v1/quotations/{q_id}",
        headers=admin_headers,
        json={"status": "WON"},
    )
    assert r.status_code == 200, r.text


def test_quotation_invalid_transition(client, admin_headers):
    # DRAFT → WON should fail (must go through SENT first)
    r = client.post(
        "/api/v1/quotations",
        headers=admin_headers,
        json={
            "project_name": "Invalid Transition",
            "customer_name": "ITC",
            "value_usd": 10000,
        },
    )
    assert r.status_code == 200
    q_id = r.json()["id"]

    r = client.patch(
        f"/api/v1/quotations/{q_id}",
        headers=admin_headers,
        json={"status": "WON"},
    )
    assert r.status_code == 422, r.text
