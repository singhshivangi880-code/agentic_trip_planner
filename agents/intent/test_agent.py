import pytest
from agents.intent.agent import IntentAgent
from agents.intent.schema import TripIntent
from agents.common.gemini.client import MockGeminiClient
from agents.common.state import TripPlanningState, WorkflowStatus

@pytest.mark.asyncio
async def test_intent_agent_success():
    mock_client = MockGeminiClient()
    mock_intent = TripIntent(
        destination="Japan",
        duration=10,
        interests=["food"]
    )
    mock_client.set_mock_response(TripIntent, mock_intent)
    
    agent = IntentAgent(gemini_client=mock_client)
    
    state = TripPlanningState(
        trip={"destination": "Japan", "duration_days": 10},
        profile={},
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
    
    result = await agent.execute(state)
    
    assert result.status == "success"
    assert result.data["destination"] == "Japan"
    assert result.data["duration"] == 10
    assert "food" in result.data["interests"]
