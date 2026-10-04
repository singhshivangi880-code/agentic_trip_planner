import pytest
from unittest.mock import patch, AsyncMock
from agents.research.transport.agent import TransportAgent
from agents.research.transport.schema import TransportList, TransportOption
from agents.common.gemini.client import MockGeminiClient
from agents.common.state import TripPlanningState, WorkflowStatus

@pytest.fixture
def mock_cache():
    with patch("agents.research.transport.agent.Cache") as mock:
        mock.get = AsyncMock(return_value=None)
        mock.set = AsyncMock()
        yield mock

@pytest.mark.asyncio
async def test_transport_agent_success(mock_cache):
    mock_client = MockGeminiClient()
    mock_result = TransportList(
        options=[
            TransportOption(mode="Train", departure="Tokyo", arrival="Kyoto", duration_hours=2.5, booking_information="JR Pass", is_stale_data=False, confidence=0.9)
        ]
    )
    mock_client.set_mock_response(TransportList, mock_result)
    
    agent = TransportAgent(gemini_client=mock_client)
    state = TripPlanningState(trip={"intent": {"origin": "Tokyo", "destination": "Kyoto"}}, profile={}, constraints={}, research=[], recommendations=[], itinerary={}, bookings=[], locked_items=[], rejected_items=[], pending_decision=None, validation_results={}, workflow_status=WorkflowStatus.RUNNING, retry_counts={}, agent_results=[])
    
    result = await agent.execute(state)
    assert result.status == "success"
    assert result.data["results"]["options"][0]["mode"] == "Train"
