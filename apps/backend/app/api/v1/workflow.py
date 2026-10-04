import asyncio
import json
from typing import AsyncGenerator
from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse
from app.core.security import rate_limit
from app.api.v1.trips import require_trip_owner

router = APIRouter(prefix="/trips/{trip_id}/workflow", tags=["workflow"])

async def mock_event_generator(request: Request, trip_id: str) -> AsyncGenerator[str, None]:
    # Heartbeat
    yield "data: " + json.dumps({"type": "heartbeat", "message": "ping"}) + "\n\n"
    
    events = [
        {"type": "agent_started", "agent_name": "IntentAgent", "message": "Understanding your trip requirements..."},
        {"type": "agent_completed", "agent_name": "IntentAgent", "message": "Extracted start and end dates."},
        {"type": "agent_started", "agent_name": "DestinationResearchAgent", "message": "Searching for great places..."},
        {"type": "agent_completed", "agent_name": "DestinationResearchAgent", "message": "Found 3 top cities!"},
        {"type": "checkpoint_required", "message": "We need your input.", "data": {"question": "Do you prefer a faster or slower pace?", "options": ["Fast", "Slow"]}},
        {"type": "workflow_completed", "message": "Done!"}
    ]
    
    for event in events:
        if await request.is_disconnected():
            break
            
        await asyncio.sleep(0.1) # small delay for tests
        yield f"data: {json.dumps(event)}\n\n"

@router.get("/stream", dependencies=[Depends(require_trip_owner), rate_limit(times=20, seconds=60)])
async def stream_workflow_events(trip_id: str, request: Request):
    """
    Stream workflow progress events as SSE.
    """
    return StreamingResponse(
        mock_event_generator(request, trip_id),
        media_type="text/event-stream"
    )
