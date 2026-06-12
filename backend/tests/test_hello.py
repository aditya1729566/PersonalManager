from fastapi.testclient import TestClient
from backend.main import app


def test_hello():
    client = TestClient(app)
    r = client.get("/api/hello")
    assert r.status_code == 200
    assert r.json() == {"message": "hello world"}
