from fastapi.testclient import TestClient
from backend.main import app


def test_login_success():
    client = TestClient(app)
    r = client.post("/api/login", json={"username": "user", "password": "password"})
    assert r.status_code == 200
    assert r.json() == {"success": True}
    assert "session" in r.cookies


def test_login_failure():
    client = TestClient(app)
    r = client.post("/api/login", json={"username": "user", "password": "wrong"})
    assert r.status_code == 401


def test_logout():
    client = TestClient(app)
    r = client.post("/api/login", json={"username": "user", "password": "password"})
    assert r.status_code == 200
    r2 = client.post("/api/logout")
    assert r2.status_code == 200
    assert r2.json() == {"success": True}
