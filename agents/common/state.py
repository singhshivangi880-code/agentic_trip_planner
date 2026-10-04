from typing import TypedDict, Optional, Dict
from enum import Enum
import operator
from typing_extensions import Annotated
from pydantic import BaseModel

class WorkflowStatus(str, Enum):
    RUNNING = "RUNNING"
    WAITING_FOR_USER = "WAITING_FOR_USER"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class AgentResult(BaseModel):
    agent_name: str
    status: str  # "success" or "failed"
    data: dict = {}
    metadata: dict = {}

# ponytail: simple TypedDict for LangGraph state. using operator.add for lists to support graph append semantics
class TripPlanningState(TypedDict):
    trip: dict
    profile: dict
    constraints: dict
    research: Annotated[list, operator.add]
    recommendations: Annotated[list, operator.add]
    itinerary: dict
    bookings: list
    locked_items: list
    rejected_items: list
    pending_decision: Optional[dict]
    validation_results: dict
    workflow_status: WorkflowStatus
    retry_counts: dict
    agent_results: Annotated[list[AgentResult], operator.add]

class BaseAgent:
    """Base interface for all agents."""
    name: str

    async def execute(self, state: TripPlanningState) -> AgentResult:
        raise NotImplementedError
