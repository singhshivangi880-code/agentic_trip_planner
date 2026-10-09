from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_submit_decision_success():
    response = client.post(
        "/api/v1/trips/12345/decisions",
        json={
            "decision_id": "dec-1",
            "selected_option": "approve"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "dec-1" in data["message"]
    assert "12345" in data["message"]

def test_submit_decision_missing_option():
    response = client.post(
        "/api/v1/trips/12345/decisions",
        json={
            "decision_id": "dec-1"
        }
    )
    assert response.status_code == 422 # Pydantic validation error
