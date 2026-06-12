from fastapi.testclient import TestClient
from backend.main import app


def test_kanban_put_get_flow(tmp_path):
    with TestClient(app) as client:
        # login to set session cookie
        r = client.post("/api/login", json={"username": "user", "password": "password"})
        assert r.status_code == 200

        payload = {"columns": [{"id": "c1", "title": "T", "cards": [{"id": "card1", "title": "Do"}]}]}
        r2 = client.put("/api/kanban", json=payload)
        assert r2.status_code == 200

        r3 = client.get("/api/kanban")
        assert r3.status_code == 200
        assert r3.json() == payload
