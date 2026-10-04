import pytest
import os
from dotenv import load_dotenv
load_dotenv('.env')

from agents.preparation.packing.agent import PackingAgent
from agents.common.state import TripPlanningState, WorkflowStatus
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_packing_agent_success():
    with patch("agents.common.gemini.client.GeminiClient.generate_structured", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {
            "categories": [
                {
                    "category_name": "Clothing",
                    "items": [
                        {"name": "Jacket", "reason": "Cold weather", "is_essential": True}
                    ]
                }
            ],
            "assumptions_made": ["Assuming you have basic toiletries"]
        }
        
        agent = PackingAgent()
        state = TripPlanningState(
            trip={"intent": {"destination": "London", "start_date": "2026-10-01", "end_date": "2026-10-03"}},
            profile={}, constraints={}, 
            research={"weather": {"forecast": "Rainy and cold"}}, 
            recommendations=[],
            itinerary={
                "days": [{
                    "day_index": 1,
                    "date": "2026-10-01",
                    "theme_or_area": "London",
                    "items": [{"title": "Hiking", "item_type": "Activity"}]
                }]
            },
            replanning_request=None,
            bookings=[], locked_items=[], rejected_items=[], pending_decision=None,
            validation_results={}, workflow_status=WorkflowStatus.RUNNING, retry_counts={}, agent_results=[]
        )
        
        res = await agent.execute(state)
        assert res.status == "success"
        assert res.data["packing_list"]["categories"][0]["items"][0]["name"] == "Jacket"
