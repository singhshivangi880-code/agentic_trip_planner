from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.validation.validators.engine import validate_itinerary
from agents.itinerary.schema import Itinerary

class ValidationAgent(BaseAgent):
    name = "ValidationAgent"

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            itinerary_data = state.get("itinerary", {})
            if not itinerary_data:
                return AgentResult(
                    agent_name=self.name,
                    status="success",
                    data={"skipped": True, "reason": "No itinerary available to validate"}
                )
            
            intent = state.get("trip", {}).get("intent", {})
            start_date = intent.get("start_date")
            end_date = intent.get("end_date")

            if not start_date or not end_date:
                return AgentResult(
                    agent_name=self.name,
                    status="failed",
                    metadata={"error": "Trip bounds missing from intent."}
                )

            itinerary = Itinerary(**itinerary_data)
            
            result = validate_itinerary(itinerary, start_date, end_date)
            
            if not result.is_valid:
                return AgentResult(
                    agent_name=self.name,
                    status="failed",
                    data={"errors": result.errors, "warnings": result.warnings}
                )

            return AgentResult(
                agent_name=self.name,
                status="success",
                data={"valid": True, "warnings": result.warnings}
            )
        except Exception as e:
            return AgentResult(
                agent_name=self.name,
                status="failed",
                metadata={"error": str(e)}
            )
