from langgraph.graph import StateGraph, END
from agents.common.state import TripPlanningState, WorkflowStatus

def trip_manager_node(state: TripPlanningState):
    """Dummy trip manager node to establish the START -> Node -> END path."""
    return {"workflow_status": WorkflowStatus.COMPLETED}

def create_workflow() -> StateGraph:
    """Creates the LangGraph workflow skeleton."""
    workflow = StateGraph(TripPlanningState)
    
    workflow.add_node("trip_manager", trip_manager_node)
    
    workflow.set_entry_point("trip_manager")
    workflow.add_edge("trip_manager", END)
    
    return workflow

# Compile the graph for execution
app = create_workflow().compile()
