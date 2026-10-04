import json
from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from tools.places import get_place
from apps.backend.app.core.redis import Cache
from .schema import FoodList
from .prompt import FOOD_RESEARCH_PROMPT

class FoodAgent(BaseAgent):
    name = "FoodAgent"

    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            intent = state.get("trip", {}).get("intent") or {}
            destination = intent.get("destination", "")
            profile = state.get("profile", {})
            dietary = profile.get("dietary_preferences", [])
            
            if not destination:
                return AgentResult(agent_name=self.name, status="success", data={"skipped": True, "reason": "No destination"})

            cache_key = f"research:food:{destination}:{'-'.join(dietary)}"
            
            cached_result = await Cache.get(cache_key)
            if cached_result:
                return AgentResult(agent_name=self.name, status="success", data=cached_result, metadata={"cached": True})

            place_res = await get_place("mock_restaurant_id")
            
            research_context = json.dumps({"places_data": [place_res.data]}, indent=2)
            context = f"Destination: {destination}, Dietary: {', '.join(dietary) if dietary else 'None'}"

            prompt = FOOD_RESEARCH_PROMPT.format(
                context=context,
                research_context=research_context
            )
            
            res = await self.gemini_client.generate_structured(prompt=prompt, schema=FoodList)
            
            result_data = {
                "results": res.model_dump(),
                "sources": [{"source_url": place_res.source, "retrieved_at": place_res.retrieved_at}]
            }
            
            await Cache.set(cache_key, result_data, ttl=86400 * 7)
            
            return AgentResult(agent_name=self.name, status="success", data=result_data)
        except Exception as e:
            return AgentResult(agent_name=self.name, status="failed", metadata={"error": str(e)})
