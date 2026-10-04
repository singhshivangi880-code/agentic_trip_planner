import json
from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from .schema import Itinerary
from .prompt import ITINERARY_PROMPT

class ItineraryAgent(BaseAgent):
    name = "ItineraryAgent"

    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            intent = state.get("trip", {}).get("intent", {})
            recs = state.get("recommendations", [])
            
            if not intent:
                return AgentResult(
                    agent_name=self.name,
                    status="success",
                    data={"skipped": True, "reason": "No trip intent available"}
                )

            prompt = ITINERARY_PROMPT.format(
                intent=json.dumps(intent, indent=2),
                recommendations=json.dumps(recs, indent=2)
            )
            
            itinerary_res = await self.gemini_client.generate_structured(
                prompt=prompt,
                schema=Itinerary
            )
            
            return AgentResult(
                agent_name=self.name,
                status="success",
                data=itinerary_res.model_dump()
            )
        except Exception as e:
            return AgentResult(
                agent_name=self.name,
                status="failed",
                metadata={"error": str(e)}
            )
