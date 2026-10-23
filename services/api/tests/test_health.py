from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_api_root_discloses_read_only_mode():
    response = client.get("/api/v1")
    assert response.status_code == 200
    assert response.json()["mode"] == "read-only"
    assert response.json()["trading_execution"] == "disabled"
