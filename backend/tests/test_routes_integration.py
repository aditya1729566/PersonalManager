from fastapi.testclient import TestClient
from backend.main import app


def test_static_root_served():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    # basic sanity: HTML should contain <html
    assert "<html" in r.text.lower()


def test_ai_route_integration(monkeypatch):
    client = TestClient(app)
    # ensure no API key so mock path is used
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    r = client.post("/api/ai/test", json={})
    assert r.status_code == 200
    j = r.json()
    assert j["mock"] is True
    assert "4" in j["result"]
