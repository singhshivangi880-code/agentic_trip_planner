import pytest
from unittest.mock import AsyncMock
from agents.workflow.research.manager import ResearchManager
from agents.common.state import TripPlanningState, WorkflowStatus
from agents.common.gemini.client import MockGeminiClient
from agents.common.state import AgentResult

@pytest.mark.asyncio
async def test_research_manager_success():
    mock_client = MockGeminiClient()
    manager = ResearchManager(gemini_client=mock_client)
    
    manager.destination_agent.execute = AsyncMock(return_value=AgentResult(status="success", data={"destination": "Japan"}, agent_name="DestinationAgent"))
    manager.attraction_agent.execute = AsyncMock(return_value=AgentResult(status="success", data={"attractions": []}, agent_name="AttractionAgent"))
    manager.experience_agent.execute = AsyncMock(return_value=AgentResult(status="success", data={"experiences": []}, agent_name="ExperienceAgent"))
    manager.food_agent.execute = AsyncMock(return_value=AgentResult(status="success", data={"food": []}, agent_name="FoodAgent"))
    manager.transport_agent.execute = AsyncMock(return_value=AgentResult(status="success", data={"transport": []}, agent_name="TransportAgent"))
    manager.weather_agent.execute = AsyncMock(return_value=AgentResult(status="success", data={"weather": []}, agent_name="WeatherAgent"))
    
    state = TripPlanningState(trip={"intent": {"destination": "Japan", "origin": "NY"}}, profile={}, constraints={}, research=[], recommendations=[], itinerary={}, bookings=[], locked_items=[], rejected_items=[], pending_decision=None, validation_results={}, workflow_status=WorkflowStatus.RUNNING, retry_counts={}, agent_results=[])
    
    result = await manager.execute(state)
    
    assert result.status == "success"
    assert "DestinationAgent" in result.data["research"]
    assert "WeatherAgent" in result.data["research"]

@pytest.mark.asyncio
async def test_research_manager_partial_failure():
    mock_client = MockGeminiClient()
    manager = ResearchManager(gemini_client=mock_client)
    
    manager.destination_agent.execute = AsyncMock(return_value=AgentResult(status="success", data={"destination": "Japan"}, agent_name="DestinationAgent"))
    manager.attraction_agent.execute = AsyncMock(side_effect=Exception("API Error"))
    manager.experience_agent.execute = AsyncMock(return_value=AgentResult(status="failed", data={}, agent_name="ExperienceAgent"))
    manager.food_agent.execute = AsyncMock(return_value=AgentResult(status="success", data={"skipped": True}, agent_name="FoodAgent"))
    manager.transport_agent.execute = AsyncMock(return_value=AgentResult(status="success", data={"transport": []}, agent_name="TransportAgent"))
    manager.weather_agent.execute = AsyncMock(return_value=AgentResult(status="success", data={"weather": []}, agent_name="WeatherAgent"))
    
    state = TripPlanningState(trip={}, profile={}, constraints={}, research=[], recommendations=[], itinerary={}, bookings=[], locked_items=[], rejected_items=[], pending_decision=None, validation_results={}, workflow_status=WorkflowStatus.RUNNING, retry_counts={}, agent_results=[])
    
    result = await manager.execute(state)
    
    assert result.status == "success"
    # Destination, Transport, Weather should be in research data
    assert "DestinationAgent" in result.data["research"]
    assert "TransportAgent" in result.data["research"]
    assert "WeatherAgent" in result.data["research"]
    
    # Attraction raised exception (filtered out), Experience failed (filtered out), Food skipped (filtered out)
    assert "AttractionAgent" not in result.data["research"]
    assert "ExperienceAgent" not in result.data["research"]
    assert "FoodAgent" not in result.data["research"]
