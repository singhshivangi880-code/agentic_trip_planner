from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from agents.preparation.readiness.schema import ReadinessPlan
from agents.preparation.readiness.prompt import READINESS_SYSTEM_PROMPT

class ReadinessAgent(BaseAgent):
    name = "ReadinessAgent"
    
    def __init__(self):
        self.client = GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            profile = state.get("profile", {})
            trip = state.get("trip", {}).get("intent", {})
            
            nationality = profile.get("nationality", "Unknown")
            destination = trip.get("destination", "Unknown")
            
            if destination == "Unknown":
                return AgentResult(agent_name=self.name, status="failed", metadata={"error": "Destination is unknown"})
                
            user_prompt = f"Nationality: {nationality}\nDestination: {destination}\nPlease generate the readiness plan."
            
            readiness_data = await self.client.generate_structured(
                prompt=user_prompt,
                schema=ReadinessPlan,
                system_instruction=READINESS_SYSTEM_PROMPT
            )
            
            if not readiness_data:
                return AgentResult(agent_name=self.name, status="failed", metadata={"error": "Failed to generate readiness plan"})
            
            # Enforce the volatile rule
            if "visa_requirement" in readiness_data:
                readiness_data["visa_requirement"]["is_volatile"] = True
            
            plan = ReadinessPlan(**readiness_data)
            
            return AgentResult(
                agent_name=self.name,
                status="success",
                data={"readiness": plan.model_dump()}
            )
        except Exception as e:
            return AgentResult(agent_name=self.name, status="failed", metadata={"error": str(e)})
