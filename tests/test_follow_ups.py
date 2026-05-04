"""Tests for /api/v1/follow-ups — CRUD + overdue + reschedule."""

from datetime import datetime, timedelta


def _make_opp(client, admin_headers):
    r = client.post(
        "/api/v1/opportunities",
        headers=admin_headers,
        json={
            "project_name": "Follow-up Test",
            "customer_name": "Follow-up Cust",
            "product_group": "HRSG",
            "stage": "PROSPECT",
        },
    )
    assert r.status_code == 200, r.text
    return r.json()["id"]


def test_follow_ups_requires_auth(client):
    r = client.get("/api/v1/follow-ups")
    assert r.status_code == 401


def test_follow_ups_list(client, admin_headers):
    r = client.get("/api/v1/follow-ups", headers=admin_headers)
    assert r.status_code == 200
    body = r.json()
    assert "total" in body and "items" in body


def test_follow_up_overdue_pagination(client, admin_headers):
    r = client.get("/api/v1/follow-ups/overdue", headers=admin_headers)
    assert r.status_code == 200
    body = r.json()
    # Standard pagination contract — UNIFIED step 6
    assert "total" in body and "items" in body
    assert "limit" in body and "offset" in body


def test_follow_up_create(client, admin_headers):
    opp_id = _make_opp(client, admin_headers)
    next_dt = (datetime.utcnow() + timedelta(days=3)).isoformat()
    r = client.post(
        "/api/v1/follow-ups",
        headers=admin_headers,
        json={
            "opportunity_id": opp_id,
            "schedule_type": "CALL",
            "next_follow_up": next_dt,
        },
    )
    assert r.status_code == 200, r.text


def test_follow_up_invalid_body_missing_opp(client, admin_headers):
    r = client.post(
        "/api/v1/follow-ups",
        headers=admin_headers,
        json={
            "schedule_type": "CALL",
            "next_follow_up": "2026-12-01T10:00:00",
        },
    )
    assert r.status_code == 422


def test_follow_up_create_unknown_opp(client, admin_headers):
    r = client.post(
        "/api/v1/follow-ups",
        headers=admin_headers,
        json={
            "opportunity_id": "00000000-0000-0000-0000-000000000000",
            "schedule_type": "CALL",
            "next_follow_up": "2026-12-01T10:00:00",
        },
    )
    assert r.status_code == 404
