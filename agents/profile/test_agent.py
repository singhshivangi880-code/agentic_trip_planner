import pytest
from agents.profile.agent import TravellerProfileAgent
from agents.common.state import TripPlanningState, WorkflowStatus

def create_state(profile=None, trip=None):
    return TripPlanningState(
        trip=trip or {},
        profile=profile or {},
        constraints={},
        research=[],
        recommendations=[],
        itinerary={},
        bookings=[],
        locked_items=[],
        rejected_items=[],
        pending_decision=None,
        validation_results={},
        workflow_status=WorkflowStatus.RUNNING,
        retry_counts={},
        agent_results=[]
    )

@pytest.mark.asyncio
async def test_profile_only():
    agent = TravellerProfileAgent()
    state = create_state(profile={"budget": "budget", "pace": "relaxed"})
    res = await agent.execute(state)
    assert res.data["budget"] == "budget"
    assert res.data["pace"] == "relaxed"

@pytest.mark.asyncio
async def test_trip_only():
    agent = TravellerProfileAgent()
    state = create_state(trip={"preferences": {"budget": "luxury"}})
    res = await agent.execute(state)
    assert res.data["budget"] == "luxury"

@pytest.mark.asyncio
async def test_both_no_conflict():
    agent = TravellerProfileAgent()
    state = create_state(
        profile={"dietary_preferences": ["vegan"]},
        trip={"preferences": {"budget": "moderate"}}
    )
    res = await agent.execute(state)
    assert res.data["budget"] == "moderate"
    assert res.data["dietary_preferences"] == ["vegan"]

@pytest.mark.asyncio
async def test_conflicting_values():
    agent = TravellerProfileAgent()
    state = create_state(
        profile={"budget": "budget", "dietary_preferences": ["vegetarian"]},
        trip={"preferences": {"budget": "luxury", "dietary_preferences": []}}
    )
    res = await agent.execute(state)
    assert res.data["budget"] == "luxury"
    assert res.data["dietary_preferences"] == []

@pytest.mark.asyncio
async def test_missing_profile():
    agent = TravellerProfileAgent()
    state = create_state(profile=None, trip=None)
    res = await agent.execute(state)
    assert res.data["budget"] is None
