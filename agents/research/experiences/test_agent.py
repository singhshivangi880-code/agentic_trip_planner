import pytest
from unittest.mock import patch, AsyncMock
from agents.research.experiences.agent import ExperienceAgent
from agents.research.experiences.schema import ExperienceList, ExperienceResult
from agents.common.gemini.client import MockGeminiClient
from agents.common.state import TripPlanningState, WorkflowStatus

@pytest.fixture
def mock_cache():
    with patch("agents.research.experiences.agent.Cache") as mock:
        mock.get = AsyncMock(return_value=None)
        mock.set = AsyncMock()
        yield mock

@pytest.mark.asyncio
async def test_experience_agent_success(mock_cache):
    mock_client = MockGeminiClient()
    mock_result = ExperienceList(
        experiences=[
            ExperienceResult(name="Tea Ceremony", category="cultural", description="Traditional tea", tourist_or_offbeat="tourist", confidence=0.9)
        ]
    )
    mock_client.set_mock_response(ExperienceList, mock_result)
    
    agent = ExperienceAgent(gemini_client=mock_client)
    state = TripPlanningState(trip={"intent": {"destination": "Tokyo"}}, profile={}, constraints={}, research=[], recommendations=[], itinerary={}, bookings=[], locked_items=[], rejected_items=[], pending_decision=None, validation_results={}, workflow_status=WorkflowStatus.RUNNING, retry_counts={}, agent_results=[])
    
    result = await agent.execute(state)
    assert result.status == "success"
    assert result.data["results"]["experiences"][0]["name"] == "Tea Ceremony"
