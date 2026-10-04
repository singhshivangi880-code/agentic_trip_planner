import pytest
from unittest.mock import patch, AsyncMock
from agents.research.weather.agent import WeatherAgent
from agents.research.weather.schema import WeatherResult
from agents.common.gemini.client import MockGeminiClient
from agents.common.state import TripPlanningState, WorkflowStatus

@pytest.fixture
def mock_cache():
    with patch("agents.research.weather.agent.Cache") as mock:
        mock.get = AsyncMock(return_value=None)
        mock.set = AsyncMock()
        yield mock

@pytest.mark.asyncio
async def test_weather_agent_success(mock_cache):
    mock_client = MockGeminiClient()
    mock_result = WeatherResult(typical_climate="Temperate", expected_temperature_c=22.0, expected_rain=False, weather_sensitive_activity_flag=False, confidence=0.9)
    mock_client.set_mock_response(WeatherResult, mock_result)
    
    agent = WeatherAgent(gemini_client=mock_client)
    state = TripPlanningState(trip={"intent": {"destination": "Tokyo"}}, profile={}, constraints={}, research=[], recommendations=[], itinerary={}, bookings=[], locked_items=[], rejected_items=[], pending_decision=None, validation_results={}, workflow_status=WorkflowStatus.RUNNING, retry_counts={}, agent_results=[])
    
    result = await agent.execute(state)
    assert result.status == "success"
    assert result.data["results"]["expected_temperature_c"] == 22.0
