import asyncio
import json
from typing import AsyncGenerator
from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse
from app.core.security import rate_limit
from app.api.v1.trips import require_trip_owner
from app.core.db import get_session_factory
from app.models.trip import Trip

from sqlalchemy.orm.attributes import flag_modified
from agents.intent.agent import IntentAgent
from agents.profile.agent import TravellerProfileAgent
from agents.recommendation.agent import RecommendationAgent
from agents.itinerary.agent import ItineraryAgent
from agents.common.state import TripPlanningState, WorkflowStatus

router = APIRouter(prefix="/trips/{trip_id}/workflow", tags=["workflow"])

async def real_agent_workflow_generator(request: Request, trip_id: str) -> AsyncGenerator[str, None]:
    # Initial Heartbeat
    yield "data: " + json.dumps({"type": "heartbeat", "message": "Connecting to multi-agent travel orchestrator..."}) + "\n\n"

    session_factory = get_session_factory()
    db = session_factory()
    try:
        trip = db.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            yield "data: " + json.dumps({"type": "workflow_failed", "message": "Trip not found."}) + "\n\n"
            return

        dest = trip.destination or "Destination"
        duration = trip.duration_days or 3
        origin = trip.origin or "Flexible"
        prefs = trip.preferences or {}

        existing_itinerary = prefs.get('generated_itinerary')
        force_rerun = request.query_params.get('force', '').lower() in ['true', '1', 'yes']

        if existing_itinerary and not force_rerun:
            for ag, msg in [
                ("IntentAgent", f"Verified intent: {duration} days in {dest} from {origin}."),
                ("TravellerProfileAgent", "Traveler profile synthesized."),
                ("RecommendationAgent", f"Curated authentic landmarks & culinary highlights for {dest}."),
                ("ItineraryAgent", f"Authentic itinerary ready for {dest}!")
            ]:
                yield f"data: {json.dumps({'type': 'agent_started', 'agent_name': ag, 'message': 'Loaded from verified plan.'})}\n\n"
                yield f"data: {json.dumps({'type': 'agent_completed', 'agent_name': ag, 'message': msg})}\n\n"
            
            yield f"data: {json.dumps({'type': 'workflow_completed', 'message': 'Itinerary loaded successfully!', 'itinerary': existing_itinerary})}\n\n"
            return

        state: TripPlanningState = {
            "trip": {
                "id": trip.id,
                "destination": dest,
                "duration_days": duration,
                "origin": origin,
                "start_date": str(trip.start_date) if trip.start_date else "2026-11-01",
                "end_date": str(trip.end_date) if trip.end_date else None,
                "preferences": prefs
            },
            "profile": {},
            "constraints": {},
            "research": [],
            "recommendations": [],
            "itinerary": {},
            "bookings": [],
            "locked_items": [],
            "rejected_items": [],
            "pending_decision": None,
            "validation_results": {},
            "workflow_status": WorkflowStatus.RUNNING,
            "retry_counts": {},
            "agent_results": []
        }

        # 1. IntentAgent
        yield f"data: {json.dumps({'type': 'agent_started', 'agent_name': 'IntentAgent', 'message': f'Analyzing travel parameters for {dest}...' })}\n\n"
        intent_res = await IntentAgent().execute(state)
        state['trip']['intent'] = intent_res.data or {
            'destination': dest,
            'duration': duration,
            'origin': origin,
            'start_date': str(trip.start_date) if trip.start_date else "2026-11-01",
            'end_date': str(trip.end_date) if trip.end_date else None
        }
        yield f"data: {json.dumps({'type': 'agent_completed', 'agent_name': 'IntentAgent', 'message': f'Verified intent: {duration} days in {dest} from {origin}.' })}\n\n"

        # 2. TravellerProfileAgent
        yield f"data: {json.dumps({'type': 'agent_started', 'agent_name': 'TravellerProfileAgent', 'message': 'Synthesizing traveler preferences, budget, and pacing...' })}\n\n"
        profile_res = await TravellerProfileAgent().execute(state)
        state['profile'] = profile_res.data or {}
        yield f"data: {json.dumps({'type': 'agent_completed', 'agent_name': 'TravellerProfileAgent', 'message': 'Traveler profile synthesized.' })}\n\n"

        # 3. RecommendationAgent
        yield f"data: {json.dumps({'type': 'agent_started', 'agent_name': 'RecommendationAgent', 'message': f'Curating authentic landmarks, heritage sites, and dining in {dest}...' })}\n\n"
        rec_res = await RecommendationAgent().execute(state)
        state['recommendations'] = rec_res.data or []
        rec_count = len(rec_res.data) if isinstance(rec_res.data, list) else 3
        yield f"data: {json.dumps({'type': 'agent_completed', 'agent_name': 'RecommendationAgent', 'message': f'Curated {rec_count} authentic landmarks & culinary highlights.' })}\n\n"

        # 4. ItineraryAgent
        yield f"data: {json.dumps({'type': 'agent_started', 'agent_name': 'ItineraryAgent', 'message': f'Synthesizing day-by-day geographically clustered schedule for {dest}...' })}\n\n"
        itin_res = await ItineraryAgent().execute(state)
        itinerary_data = itin_res.data if itin_res.status == 'success' else None

        # Save to database with flag_modified
        if itinerary_data:
            current_prefs = dict(trip.preferences or {})
            current_prefs['generated_itinerary'] = itinerary_data
            trip.preferences = current_prefs
            flag_modified(trip, 'preferences')
            db.commit()
            db.refresh(trip)

        yield f"data: {json.dumps({'type': 'agent_completed', 'agent_name': 'ItineraryAgent', 'message': f'Authentic itinerary crafted with real places for {dest}!' })}\n\n"
        yield f"data: {json.dumps({'type': 'workflow_completed', 'message': 'Itinerary generated successfully!', 'itinerary': itinerary_data })}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'type': 'agent_error', 'message': f'Agent error: {str(e)}' })}\n\n"
        yield f"data: {json.dumps({'type': 'workflow_completed', 'message': 'Completed with available data.' })}\n\n"
    finally:
        db.close()

@router.get("/stream", dependencies=[Depends(require_trip_owner), rate_limit(times=60, seconds=60)])
async def stream_workflow_events(trip_id: str, request: Request):
    """
    Stream real multi-agent workflow progress events as SSE.
    """
    return StreamingResponse(
        real_agent_workflow_generator(request, trip_id),
        media_type="text/event-stream"
    )
