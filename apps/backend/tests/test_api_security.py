from fastapi.testclient import TestClient
import os
os.environ["TESTING"] = "1"
from app.main import app as fastapi_app
import pytest

import app.core.security.rate_limit
app.core.security.rate_limit.redis_client = None

client = TestClient(fastapi_app)

def test_unauthorized_trip_access():
    # Attempt to fetch a random trip without a token
    res = client.get("/api/v1/trips/1234")
    assert res.status_code == 401
    assert "Authentication required" in res.text

def test_cross_user_trip_access():
    from app.core.db import get_session_factory
    from app.models.user import User as DBUser
    
    SessionLocal = get_session_factory()
    db = SessionLocal()
    # Insert test users if not exist
    if not db.query(DBUser).filter(DBUser.id == "user1").first():
        db.add(DBUser(id="user1", email="user1@example.com", name="User 1"))
    if not db.query(DBUser).filter(DBUser.id == "user2").first():
        db.add(DBUser(id="user2", email="user2@example.com", name="User 2"))
    db.commit()
    db.close()

    # Create trip as user1
    res1 = client.post(
        "/api/v1/trips",
        json={"destination": "Rome", "duration_days": 5},
        headers={"Authorization": "Bearer user1"}
    )
    assert res1.status_code == 201
    trip_id = res1.json()["id"]

    # Try to access as user2
    res2 = client.get(
        f"/api/v1/trips/{trip_id}",
        headers={"Authorization": "Bearer user2"}
    )
    assert res2.status_code == 403
    assert "Not authorized" in res2.text

    # Access as user1 should work
    res3 = client.get(
        f"/api/v1/trips/{trip_id}",
        headers={"Authorization": "Bearer user1"}
    )
    assert res3.status_code == 200
    
def test_dev_access_restricted():
    # Try dev endpoint as standard user
    res1 = client.get("/api/v1/dev/traces/123", headers={"Authorization": "Bearer user1"})
    assert res1.status_code == 403
    assert "Developer access required" in res1.text
    
    # Try as dev user
    # Note: the mock tracer actually attempts to connect to Jaeger, so we expect a 502 or 404 instead of 403
    res2 = client.get("/api/v1/dev/traces/123", headers={"Authorization": "Bearer dev-token"})
    assert res2.status_code in [404, 502]
