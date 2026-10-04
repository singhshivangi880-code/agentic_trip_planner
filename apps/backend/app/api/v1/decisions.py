from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional
from app.core.security import rate_limit
from app.api.v1.trips import require_trip_owner

router = APIRouter(prefix="/trips/{trip_id}/decisions", tags=["decisions"])

class DecisionSubmitRequest(BaseModel):
    decision_id: str = Field(description="ID of the checkpoint")
    selected_option: str = Field(description="The option the user selected")
    context: Optional[str] = None

class DecisionResponse(BaseModel):
    status: str
    message: str

@router.post("", response_model=DecisionResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(require_trip_owner), rate_limit(times=20, seconds=60)])
def submit_decision(trip_id: str, request: DecisionSubmitRequest):
    # Ponytail: For now, this is a mock endpoint to represent resuming the LangGraph workflow.
    if not request.selected_option:
        raise HTTPException(status_code=400, detail="selected_option is required")
        
    # Later: Langgraph update state logic goes here
    # e.g., graph.update_state({"configurable": {"thread_id": trip_id}}, {"pending_decision": request.selected_option})
    
    return DecisionResponse(
        status="success",
        message=f"Decision {request.decision_id} for trip {trip_id} recorded."
    )
