from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_share():
    trip_data = {
        "title": "Test Share Trip",
        "destination": "Paris"
    }
    trip_res = client.post("/api/v1/trips/", json=trip_data)
    if trip_res.status_code == 422:
        # Trip validation requires specific fields
        trip_data = {
            "destination": "Japan",
            "start_date": "2027-02-08",
            "end_date": "2027-02-18",
            "duration_days": 10
        }
        trip_res = client.post("/api/v1/trips/", json=trip_data)
    
    trip_id = trip_res.json()["id"]

    # Create share link
    share_res = client.post("/api/v1/share/", json={"trip_id": trip_id})
    assert share_res.status_code == 200
    token = share_res.json()["token"]
    assert token

    # Get shared trip using token
    get_res = client.get(f"/api/v1/share/{token}")
    assert get_res.status_code == 200
    shared_trip = get_res.json()
    
    assert shared_trip["destination"] == "Japan"
    assert "days" in shared_trip
    assert "days" in shared_trip

def test_get_invalid_share():
    res = client.get("/api/v1/share/invalid-token")
    assert res.status_code == 404
