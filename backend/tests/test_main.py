import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def get_token() -> str:
    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_success():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 300


def test_login_wrong_password():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401


def test_login_unknown_user():
    response = client.post(
        "/token",
        data={"username": "nobody", "password": "admin123"},
    )
    assert response.status_code == 401


def test_refresh_token():
    token = get_token()
    auth_header = "Bearer " + token
    response = client.post(
        "/token/refresh",
        headers={"Authorization": auth_header},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 300


def test_refresh_token_without_auth():
    response = client.post("/token/refresh")
    assert response.status_code == 401


def test_refresh_token_invalid():
    invalid_header = "Bearer invalid.token.here"
    response = client.post(
        "/token/refresh",
        headers={"Authorization": invalid_header},
    )
    assert response.status_code == 401
