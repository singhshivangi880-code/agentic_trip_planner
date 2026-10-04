import pytest
from agents.recommendation.agent import RecommendationAgent
from agents.recommendation.schema import RecommendationList, RecommendationItem
from agents.common.gemini.client import MockGeminiClient
from agents.common.state import TripPlanningState, WorkflowStatus

@pytest.mark.asyncio
async def test_recommendation_agent_success():
    mock_client = MockGeminiClient()
    mock_result = RecommendationList(
        recommendations=[
            RecommendationItem(
                name="Sushi Dai",
                category="food",
                reason="Matches seafood preference",
                score=95,
                time_of_day_suitability=["morning", "lunch"],
                tourist_or_offbeat="tourist"
            )
        ]
    )
    mock_client.set_mock_response(RecommendationList, mock_result)
    
    agent = RecommendationAgent(gemini_client=mock_client)
    state = TripPlanningState(
        trip={}, 
        profile={"dietary_preferences": ["seafood"]}, 
        constraints={}, 
        research=[{"food": {"results": {"recommendations": [{"name": "Sushi Dai"}]}}}], 
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
    assert len(result.data["recommendations"]) == 1
    assert result.data["recommendations"][0]["name"] == "Sushi Dai"
