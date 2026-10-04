import pytest
from agents.replanning.agent import ReplanningAgent
from agents.common.state import TripPlanningState, WorkflowStatus
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_replanning_agent_success():
    with patch("agents.common.gemini.client.GeminiClient.generate_structured", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {
            "day_index": 1,
            "date": "2026-10-01",
            "theme_or_area": "Tokyo",
            "items": [{
                "title": "Museum", "description": "Added", 
                "start_time": "14:00", "end_time": "16:00", 
                "location": "Loc", "item_type": "Activity"
            }]
        }
        
        agent = ReplanningAgent()
        state = TripPlanningState(
            trip={"intent": {"start_date": "2026-10-01", "end_date": "2026-10-03"}},
            profile={}, constraints={}, research=[], recommendations=[],
            itinerary={
                "days": [{
                    "day_index": 1,
                    "date": "2026-10-01",
                    "theme_or_area": "Tokyo",
                    "items": []
                }]
            },
            replanning_request={"target_day": 1, "instruction": "Add a museum at 2pm"},
            bookings=[], locked_items=[], rejected_items=[], pending_decision=None,
            validation_results={}, workflow_status=WorkflowStatus.RUNNING, retry_counts={}, agent_results=[]
        )
        
        res = await agent.execute(state)
        assert res.status == "success"
        assert len(res.data["itinerary"]["days"][0]["items"]) == 1
        assert res.data["itinerary"]["days"][0]["items"][0]["title"] == "Museum"
