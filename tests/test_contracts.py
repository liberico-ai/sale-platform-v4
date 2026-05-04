"""Tests for /api/v1/contracts — CRUD + milestones + settlements."""


def test_contracts_requires_auth(client):
    r = client.get("/api/v1/contracts")
    assert r.status_code == 401


def test_contracts_list(client, admin_headers):
    r = client.get("/api/v1/contracts", headers=admin_headers)
    assert r.status_code == 200
    body = r.json()
    assert "total" in body and "items" in body


def test_contract_create(client, admin_headers):
    r = client.post(
        "/api/v1/contracts",
        headers=admin_headers,
        json={
            "po_number": "PO-TEST-0001",
            "customer_name": "Test Contract Customer",
            "project_name": "Contract Test",
            "contract_status": "ACTIVE",
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["po_number"] == "PO-TEST-0001"
    assert data["status"] == "ACTIVE"


def test_contract_invalid_body_missing_customer(client, admin_headers):
    r = client.post(
        "/api/v1/contracts",
        headers=admin_headers,
        json={"po_number": "PO-NOCUST-0001"},
    )
    assert r.status_code == 400


def test_contract_milestone_requires_opportunity_id(client, admin_headers):
    r = client.post(
        "/api/v1/contracts",
        headers=admin_headers,
        json={
            "po_number": "PO-MS-0001",
            "customer_name": "Milestone Test Cust",
            "project_name": "Milestone Test Project",
        },
    )
    contract_id = r.json()["id"]

    # No opportunity_id resolvable from new contract → 400
    r = client.post(
        f"/api/v1/contracts/{contract_id}/milestones",
        headers=admin_headers,
        json={
            "milestone_type": "DELIVERY",
            "title": "First milestone",
            "planned_date": "2026-06-01",
        },
    )
    assert r.status_code == 400, r.text
