import pytest
from unittest.mock import patch, AsyncMock
from agents.research.attractions.agent import AttractionAgent
from agents.research.attractions.schema import AttractionList, AttractionResult, AttractionCategory, LocationInfo
from agents.common.gemini.client import MockGeminiClient
from agents.common.state import TripPlanningState, WorkflowStatus

@pytest.fixture
def mock_cache():
    with patch("agents.research.attractions.agent.Cache") as mock:
        mock.get = AsyncMock(return_value=None)
        mock.set = AsyncMock()
        yield mock

@pytest.mark.asyncio
async def test_attraction_agent_success(mock_cache):
    mock_client = MockGeminiClient()
    mock_result = AttractionList(
        attractions=[
            AttractionResult(
                name="Tokyo Tower",
                category=AttractionCategory(primary="Landmark", tags=["Sightseeing"]),
                estimated_duration_hours=2.0,
                location=LocationInfo(name="Tokyo Tower", address="Minato, Tokyo"),
                opening_hours=["9AM-11PM"],
                confidence=0.95
            )
        ]
    )
    mock_client.set_mock_response(AttractionList, mock_result)
    
    agent = AttractionAgent(gemini_client=mock_client)
    
    state = TripPlanningState(
        trip={"intent": {"destination": "Tokyo"}},
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
    assert result.data["results"]["attractions"][0]["name"] == "Tokyo Tower"
    assert len(result.data["sources"]) == 1
    mock_cache.get.assert_called_once_with("research:attractions:Tokyo")
    mock_cache.set.assert_called_once()

@pytest.mark.asyncio
async def test_attraction_agent_cached(mock_cache):
    cached_data = {"results": {"attractions": []}, "sources": []}
    mock_cache.get = AsyncMock(return_value=cached_data)
    
    mock_client = MockGeminiClient()
    agent = AttractionAgent(gemini_client=mock_client)
    state = TripPlanningState(
        trip={"intent": {"destination": "Tokyo"}},
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
