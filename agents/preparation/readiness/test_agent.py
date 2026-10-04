import pytest
from agents.preparation.readiness.agent import ReadinessAgent
from agents.common.state import TripPlanningState, WorkflowStatus
from unittest.mock import patch, AsyncMock
import os
from dotenv import load_dotenv
load_dotenv('.env')

@pytest.mark.asyncio
async def test_readiness_agent_success():
    with patch("agents.common.gemini.client.GeminiClient.generate_structured", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {
            "visa_requirement": {
                "is_visa_required": False,
                "details": "Visa free for 90 days",
                "official_link": "https://gov.uk",
                "is_volatile": True
            },
            "documents": [{"document_name": "Passport", "description": "6 months validity"}],
            "insurance_reminder": "Get health insurance",
            "connectivity_checklist": ["Type G adapter"],
            "currency_checklist": ["GBP"],
            "travel_advisory": "Normal precautions",
            "advisory_link": "https://travel.state.gov"
        }
        
        agent = ReadinessAgent()
        state = TripPlanningState(
            trip={"intent": {"destination": "London", "start_date": "2026-10-01", "end_date": "2026-10-03"}},
            profile={"nationality": "US"}, constraints={}, research={}, recommendations=[],
            itinerary={}, replanning_request=None,
            bookings=[], locked_items=[], rejected_items=[], pending_decision=None,
            validation_results={}, workflow_status=WorkflowStatus.RUNNING, retry_counts={}, agent_results=[]
        )
        
        res = await agent.execute(state)
        assert res.status == "success"
        assert res.data["readiness"]["visa_requirement"]["is_volatile"] is True
        assert res.data["readiness"]["visa_requirement"]["official_link"] == "https://gov.uk"
