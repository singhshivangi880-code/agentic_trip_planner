import pytest
from agents.itinerary.agent import ItineraryAgent
from agents.itinerary.schema import Itinerary, TripDay, ItineraryItem
from agents.common.gemini.client import MockGeminiClient
from agents.common.state import TripPlanningState, WorkflowStatus

@pytest.mark.asyncio
async def test_itinerary_agent_success():
    mock_client = MockGeminiClient()
    mock_result = Itinerary(
        days=[
            TripDay(
                day_index=1,
                date="2026-10-01",
                theme_or_area="Arrival and Central Tokyo",
                items=[
                    ItineraryItem(
                        title="Tsukiji Market Lunch",
                        description="Grab fresh sushi.",
                        start_time="12:00",
                        end_time="13:30",
                        location="Tsukiji",
                        item_type="Meal"
                    )
                ]
            )
        ]
    )
    mock_client.set_mock_response(Itinerary, mock_result)
    
    agent = ItineraryAgent(gemini_client=mock_client)
    state = TripPlanningState(
        trip={"intent": {"destination": "Tokyo", "start_date": "2026-10-01", "end_date": "2026-10-03"}}, 
        profile={}, 
        constraints={}, 
        research=[], 
        recommendations=[{"recommendations": [{"name": "Tsukiji Market", "category": "Food"}]}], 
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
    assert len(result.data["days"]) == 1
    assert result.data["days"][0]["items"][0]["title"] == "Tsukiji Market Lunch"
