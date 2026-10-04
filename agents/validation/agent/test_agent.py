import pytest
from agents.validation.agent.agent import ValidationAgent
from agents.common.state import TripPlanningState, WorkflowStatus

@pytest.mark.asyncio
async def test_validation_agent_success():
    agent = ValidationAgent()
    state = TripPlanningState(
        trip={"intent": {"start_date": "2026-10-01", "end_date": "2026-10-03"}},
        profile={}, constraints={}, research=[], recommendations=[],
        itinerary={
            "days": [{
                "day_index": 1,
                "date": "2026-10-01",
                "theme_or_area": "Tokyo",
                "items": [{
                    "title": "A", "description": "A", 
                    "start_time": "09:00", "end_time": "10:00", 
                    "location": "Loc", "item_type": "Activity"
                }]
            }]
        },
        bookings=[], locked_items=[], rejected_items=[], pending_decision=None,
        validation_results={}, workflow_status=WorkflowStatus.RUNNING, retry_counts={}, agent_results=[]
    )
    
    res = await agent.execute(state)
    assert res.status == "success"
    assert res.data["valid"] is True

@pytest.mark.asyncio
async def test_validation_agent_failed():
    agent = ValidationAgent()
    state = TripPlanningState(
        trip={"intent": {"start_date": "2026-10-01", "end_date": "2026-10-03"}},
        profile={}, constraints={}, research=[], recommendations=[],
        itinerary={
            "days": [{
                "day_index": 1,
                "date": "2026-10-01",
                "theme_or_area": "Tokyo",
                "items": [{
                    "title": "A", "description": "A", 
                    "start_time": "10:00", "end_time": "09:00",
                    "location": "Loc", "item_type": "Activity"
                }]
            }]
        },
        bookings=[], locked_items=[], rejected_items=[], pending_decision=None,
        validation_results={}, workflow_status=WorkflowStatus.RUNNING, retry_counts={}, agent_results=[]
    )
    
    res = await agent.execute(state)
    assert res.status == "failed"
    assert "errors" in res.data
    assert len(res.data["errors"]) > 0
