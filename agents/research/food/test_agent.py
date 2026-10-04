import pytest
from unittest.mock import patch, AsyncMock
from agents.research.food.agent import FoodAgent
from agents.research.food.schema import FoodList, FoodRecommendationResult
from agents.common.gemini.client import MockGeminiClient
from agents.common.state import TripPlanningState, WorkflowStatus

@pytest.fixture
def mock_cache():
    with patch("agents.research.food.agent.Cache") as mock:
        mock.get = AsyncMock(return_value=None)
        mock.set = AsyncMock()
        yield mock

@pytest.mark.asyncio
async def test_food_agent_success(mock_cache):
    mock_client = MockGeminiClient()
    mock_result = FoodList(
        recommendations=[
            FoodRecommendationResult(name="Sushi Dai", cuisine="Sushi", price_category="$$", location="Tsukiji", opening_information="5AM-2PM", confidence=0.95)
        ]
    )
    mock_client.set_mock_response(FoodList, mock_result)
    
    agent = FoodAgent(gemini_client=mock_client)
    state = TripPlanningState(trip={"intent": {"destination": "Tokyo"}}, profile={"dietary_preferences": ["seafood"]}, constraints={}, research=[], recommendations=[], itinerary={}, bookings=[], locked_items=[], rejected_items=[], pending_decision=None, validation_results={}, workflow_status=WorkflowStatus.RUNNING, retry_counts={}, agent_results=[])
    
    result = await agent.execute(state)
    assert result.status == "success"
    assert result.data["results"]["recommendations"][0]["name"] == "Sushi Dai"
