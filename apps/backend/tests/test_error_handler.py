from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from app.core.exceptions import AppException, register_exception_handlers
from app.core.logging import log_requests_middleware

app = FastAPI()
app.middleware("http")(log_requests_middleware)
register_exception_handlers(app)


class Payload(BaseModel):
    destination: str
    duration_days: int


@app.get("/custom-error")
def trigger_custom_error():
    raise AppException(code="INVALID_INPUT", message="Bad request payload", status_code=400)


@app.get("/generic-error")
def trigger_generic_error():
    raise RuntimeError("Unexpected failure")


@app.post("/validate")
def validate(payload: Payload):
    return payload


client = TestClient(app, raise_server_exceptions=False)


def test_custom_app_exception():
    response = client.get("/custom-error")
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "INVALID_INPUT"
    assert data["error"]["message"] == "Bad request payload"
    assert "request_id" in data["error"]


def test_generic_exception():
    response = client.get("/generic-error")
    assert response.status_code == 500
    data = response.json()
    assert data["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert "request_id" in data["error"]


def test_validation_error_uses_envelope():
    response = client.post("/validate", json={"destination": "Japan"}, headers={"X-Request-ID": "req-123"})
    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert error["request_id"] == "req-123"
    assert any(d["field"].endswith("duration_days") for d in error["details"])


def test_not_found_uses_envelope():
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "NOT_FOUND"
    assert "request_id" in error
