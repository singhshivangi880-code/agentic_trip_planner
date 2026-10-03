from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.core.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.core.logging import log_requests_middleware

app = FastAPI()
app.middleware("http")(log_requests_middleware)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/custom-error")
def trigger_custom_error():
    raise AppException(code="INVALID_INPUT", message="Bad request payload", status_code=400)


@app.get("/generic-error")
def trigger_generic_error():
    raise RuntimeError("Unexpected failure")


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
