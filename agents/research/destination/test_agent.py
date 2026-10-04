import pytest
from unittest.mock import patch, AsyncMock
from agents.research.destination.agent import DestinationAgent
from agents.research.destination.schema import DestinationOverview, CityCandidate, Seasonality, TravelConsideration
from agents.common.gemini.client import MockGeminiClient
from agents.common.state import TripPlanningState, WorkflowStatus

@pytest.fixture
def mock_cache():
    with patch("agents.research.destination.agent.Cache") as mock:
        mock.get = AsyncMock(return_value=None)
        mock.set = AsyncMock()
        yield mock

@pytest.mark.asyncio
async def test_destination_agent_success(mock_cache):
    mock_client = MockGeminiClient()
    mock_overview = DestinationOverview(
        destination="Japan",
        overview="Great place",
        cities=[CityCandidate(name="Tokyo", description="Capital", pros=["Food"], cons=["Crowded"])],
        seasonality=Seasonality(best_time_to_visit="Spring", weather_expected="Mild"),
        considerations=[TravelConsideration(category="Visas", details="Visa free for US citizens")]
    )
    mock_client.set_mock_response(DestinationOverview, mock_overview)
    
    agent = DestinationAgent(gemini_client=mock_client)
    
    state = TripPlanningState(
        trip={"intent": {"destination": "Japan"}},
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
    assert result.data["overview"]["destination"] == "Japan"
    assert len(result.data["sources"]) == 2
    mock_cache.get.assert_called_once_with("research:destination:Japan")
    mock_cache.set.assert_called_once()

@pytest.mark.asyncio
async def test_destination_agent_cached(mock_cache):
    cached_data = {"overview": {"destination": "Japan"}, "sources": []}
    mock_cache.get = AsyncMock(return_value=cached_data)
    
    mock_client = MockGeminiClient()
    agent = DestinationAgent(gemini_client=mock_client)
    state = TripPlanningState(
        trip={"intent": {"destination": "Japan"}},
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
    assert result.metadata.get("cached") is True
    assert result.data == cached_data
