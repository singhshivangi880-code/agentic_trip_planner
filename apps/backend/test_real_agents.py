import asyncio
import os
import json

from agents.intent.agent import IntentAgent
from agents.profile.agent import TravellerProfileAgent
from agents.recommendation.agent import RecommendationAgent
from agents.itinerary.agent import ItineraryAgent
from agents.common.state import TripPlanningState, WorkflowStatus

async def run_pipeline():
    print("Testing real agent execution...")
    state: TripPlanningState = {
        "trip": {
            "destination": "Delhi",
            "duration_days": 3,
            "origin": "Pune"
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

    print("1. Running IntentAgent...")
    intent_agent = IntentAgent()
    r1 = await intent_agent.execute(state)
    print("IntentAgent result status:", r1.status)
    print("IntentAgent data:", r1.data)
    state["trip"]["intent"] = r1.data or {
        "destination": "Delhi",
        "duration": 3,
        "start_date": "2026-11-01",
        "end_date": "2026-11-03"
    }

    print("2. Running TravellerProfileAgent...")
    profile_agent = TravellerProfileAgent()
    r2 = await profile_agent.execute(state)
    print("ProfileAgent status:", r2.status)
    state["profile"] = r2.data or {}

    print("3. Running RecommendationAgent...")
    rec_agent = RecommendationAgent()
    r3 = await rec_agent.execute(state)
    print("RecommendationAgent status:", r3.status)
    print("Recommendations count:", len(r3.data or []))
    state["recommendations"] = r3.data or []

    print("4. Running ItineraryAgent...")
    itin_agent = ItineraryAgent()
    r4 = await itin_agent.execute(state)
    print("ItineraryAgent status:", r4.status)
    print("ItineraryAgent data:", json.dumps(r4.data, indent=2) if r4.data else "None")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
