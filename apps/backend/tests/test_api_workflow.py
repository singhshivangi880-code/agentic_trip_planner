import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_workflow_stream():
    with client.stream("GET", "/api/v1/trips/123/workflow/stream") as response:
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
        
        events_found = []
        for line in response.iter_lines():
            if line and line.startswith("data: "):
                events_found.append(line)
                
        assert len(events_found) >= 4
        assert "heartbeat" in events_found[0]
        
        # Verify specific events were yielded
        full_text = "".join(events_found)
        assert "agent_started" in full_text
        assert "IntentAgent" in full_text
        assert "workflow_completed" in full_text
