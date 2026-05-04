"""Tests for /api/v1/contacts — CRUD + duplicate detection + soft delete."""

import uuid


def _make_customer(client, admin_headers, name=None):
    name = name or f"Contact Test Cust {uuid.uuid4().hex[:6]}"
    r = client.post(
        "/api/v1/customers",
        headers=admin_headers,
        json={"name": name},
    )
    assert r.status_code == 200, r.text
    return r.json()["id"]


def test_contacts_requires_auth(client):
    r = client.get("/api/v1/contacts")
    assert r.status_code == 401


def test_contacts_list(client, admin_headers):
    r = client.get("/api/v1/contacts", headers=admin_headers)
    assert r.status_code == 200
    body = r.json()
    assert "total" in body and "items" in body


def test_contact_create(client, admin_headers):
    customer_id = _make_customer(client, admin_headers)
    r = client.post(
        "/api/v1/contacts",
        headers=admin_headers,
        json={
            "customer_id": customer_id,
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "is_primary": True,
        },
    )
    assert r.status_code == 200, r.text


def test_contact_invalid_body_missing_customer_id(client, admin_headers):
    r = client.post(
        "/api/v1/contacts",
        headers=admin_headers,
        json={"name": "Detached Contact"},
    )
    # Pydantic validation rejects missing required customer_id
    assert r.status_code == 422


def test_contact_duplicate_email_per_customer(client, admin_headers):
    customer_id = _make_customer(client, admin_headers)
    payload = {
        "customer_id": customer_id,
        "name": "Dupe Tester",
        "email": "dupe@example.com",
    }
    r = client.post("/api/v1/contacts", headers=admin_headers, json=payload)
    assert r.status_code == 200, r.text

    # Second insert with same (customer_id, email) → 409
    r = client.post("/api/v1/contacts", headers=admin_headers, json=payload)
    assert r.status_code == 409, r.text
    body = r.json()
    assert body["code"] == "DUPLICATE"


def test_contact_primary_demotes_others(client, admin_headers):
    customer_id = _make_customer(client, admin_headers)

    # First contact: is_primary
    r = client.post(
        "/api/v1/contacts",
        headers=admin_headers,
        json={
            "customer_id": customer_id,
            "name": "First Primary",
            "email": "first@example.com",
            "is_primary": True,
        },
    )
    first_id = r.json()["id"]

    # Second contact: is_primary should demote first
    r = client.post(
        "/api/v1/contacts",
        headers=admin_headers,
        json={
            "customer_id": customer_id,
            "name": "Second Primary",
            "email": "second@example.com",
            "is_primary": True,
        },
    )
    assert r.status_code == 200, r.text

    # First contact should now be non-primary
    r = client.get(f"/api/v1/contacts/{first_id}", headers=admin_headers)
    assert r.json()["contact"]["is_primary"] == 0
