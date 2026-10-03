import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# ponytail: simple test cases against the live/test sqlite db through FastAPI TestClient/AsyncClient
@pytest.mark.asyncio
async def test_trip_api_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # POST invalid
        resp_invalid = await ac.post("/api/v1/trips", json={
            "destination": "Japan",
            "start_date": "2027-02-18",
            "end_date": "2027-02-08", # invalid order
            "duration_days": 10
        })
        assert resp_invalid.status_code == 422 # RequestValidationError -> 422 or customized VALIDATION_ERROR

        # POST success
        resp = await ac.post("/api/v1/trips", json={
            "destination": "Japan",
            "duration_days": 10
        })
        assert resp.status_code == 201
        trip = resp.json()
        assert trip["destination"] == "Japan"
        assert trip["duration_days"] == 10
        assert trip["status"] == "draft"
        trip_id = trip["id"]
        
        # GET success
        resp_get = await ac.get(f"/api/v1/trips/{trip_id}")
        assert resp_get.status_code == 200
        assert resp_get.json()["id"] == trip_id
        
        # GET not found
        resp_not_found = await ac.get("/api/v1/trips/00000000-0000-0000-0000-000000000000")
        assert resp_not_found.status_code == 404
        
        # PATCH success
        resp_patch = await ac.patch(f"/api/v1/trips/{trip_id}", json={
            "status": "planning"
        })
        assert resp_patch.status_code == 200
        assert resp_patch.json()["status"] == "planning"
