from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ping_endpoint():
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_ready_endpoint_ok(monkeypatch):
    monkeypatch.setattr("app.main.check_dependencies", lambda: {"database": "ok", "redis": "ok"})
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_endpoint_degraded(monkeypatch):
    monkeypatch.setattr("app.main.check_dependencies", lambda: {"database": "ok", "redis": "error: ConnectionError"})
    response = client.get("/health/ready")
    assert response.status_code == 503
    assert response.json()["checks"]["redis"].startswith("error")
