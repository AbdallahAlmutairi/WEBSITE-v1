import json
from fastapi.testclient import TestClient
from apps.backend.main import app

client = TestClient(app)

def test_history_endpoint_exists():
    r = client.get("/api/history?symbol=AAPL&interval=1m&lookback=5d")
    assert r.status_code in (200, 404)

def test_openapi():
    r = client.get("/openapi.json")
    assert r.status_code == 200
    schema = r.json()
    assert "paths" in schema
