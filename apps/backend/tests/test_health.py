import pytest
from fastapi.testclient import TestClient
from apps.backend.main import app

client = TestClient(app)

def test_root_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
