import json
from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from .schema import RecommendationList
from .prompt import RECOMMENDATION_PROMPT

class RecommendationAgent(BaseAgent):
    name = "RecommendationAgent"

    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            profile = state.get("profile", {})
            research_data = state.get("research", [])
            
            if not research_data:
                return AgentResult(
                    agent_name=self.name,
                    status="success",
                    data={"skipped": True, "reason": "No research data available"}
                )

            prompt = RECOMMENDATION_PROMPT.format(
                profile=json.dumps(profile, indent=2),
                research=json.dumps(research_data, indent=2)
            )
            
            recommendations_res = await self.gemini_client.generate_structured(
                prompt=prompt,
                schema=RecommendationList
            )
            
            return AgentResult(
                agent_name=self.name,
                status="success",
                data=recommendations_res.model_dump()
            )
        except Exception as e:
            return AgentResult(
                agent_name=self.name,
                status="failed",
                metadata={"error": str(e)}
            )
