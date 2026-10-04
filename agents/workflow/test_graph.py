import pytest
from langgraph.graph import StateGraph, END
from agents.common.state import TripPlanningState, BaseAgent, AgentResult, WorkflowStatus

class DummyAgentA(BaseAgent):
    name = "DummyAgentA"
    async def execute(self, state: TripPlanningState) -> AgentResult:
        return AgentResult(agent_name=self.name, status="success", data={"did_a": True})

class DummyAgentB(BaseAgent):
    name = "DummyAgentB"
    async def execute(self, state: TripPlanningState) -> AgentResult:
        return AgentResult(agent_name=self.name, status="success", data={"did_b": True})

async def node_a(state: TripPlanningState):
    agent = DummyAgentA()
    result = await agent.execute(state)
    return {"agent_results": [result]}

async def node_b(state: TripPlanningState):
    # Verify handoff: Agent B can see Agent A's results in state
    assert len(state.get("agent_results", [])) == 1
    assert state["agent_results"][0].agent_name == "DummyAgentA"
    
    agent = DummyAgentB()
    result = await agent.execute(state)
    return {"agent_results": [result], "workflow_status": WorkflowStatus.COMPLETED}

@pytest.mark.asyncio
async def test_connectivity_check_c8():
    """Verify state handoff between agents in a LangGraph workflow."""
    workflow = StateGraph(TripPlanningState)
    workflow.add_node("AgentA", node_a)
    workflow.add_node("AgentB", node_b)
    
    workflow.set_entry_point("AgentA")
    workflow.add_edge("AgentA", "AgentB")
    workflow.add_edge("AgentB", END)
    
    app = workflow.compile()
    
    initial_state = {"workflow_status": WorkflowStatus.RUNNING, "agent_results": []}
    
    # ponytail: native LangGraph async invoke is the simplest way to run and test
    final_state = await app.ainvoke(initial_state)
    
    assert final_state["workflow_status"] == WorkflowStatus.COMPLETED
    assert len(final_state["agent_results"]) == 2
    assert final_state["agent_results"][0].agent_name == "DummyAgentA"
    assert final_state["agent_results"][1].agent_name == "DummyAgentB"
