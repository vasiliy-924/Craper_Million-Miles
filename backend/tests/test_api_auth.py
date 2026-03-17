"""API tests for auth endpoints."""

import pytest


def test_login_success(client):
    """POST /auth/login with admin/admin123 returns 200 and access_token."""
    resp = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"


def test_login_invalid_password(client):
    """POST with wrong password returns 401."""
    resp = client.post(
        "/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert resp.status_code == 401
    assert "Invalid" in resp.json().get("detail", "")


def test_login_invalid_username(client):
    """POST with unknown user returns 401."""
    resp = client.post(
        "/auth/login",
        json={"username": "nonexistent", "password": "admin123"},
    )
    assert resp.status_code == 401
    assert "Invalid" in resp.json().get("detail", "")


def test_login_empty_credentials(client):
    """POST with empty credentials returns 401 (auth fails before validation)."""
    resp = client.post(
        "/auth/login",
        json={"username": "", "password": ""},
    )
    assert resp.status_code in (401, 422)
