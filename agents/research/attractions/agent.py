import json
from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from tools.places import get_place, get_opening_hours
from apps.backend.app.core.redis import Cache
from .schema import AttractionList
from .prompt import ATTRACTION_RESEARCH_PROMPT

class AttractionAgent(BaseAgent):
    name = "AttractionAgent"

    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            intent = state.get("trip", {}).get("intent") or {}
            destination = intent.get("destination", "")
            if not destination:
                return AgentResult(agent_name=self.name, status="success", data={"skipped": True, "reason": "No destination in intent"})

            cache_key = f"research:attractions:{destination}"
            
            cached_result = await Cache.get(cache_key)
            if cached_result:
                return AgentResult(agent_name=self.name, status="success", data=cached_result, metadata={"cached": True})

            # Mock fetching place data (in a real flow, a search tool would find place_ids first)
            place_res1 = await get_place("mock_id_1")
            hours_res1 = await get_opening_hours("mock_id_1")
            
            sources = [
                {"source_url": "mock_places_api", "source_name": "Places API", "retrieved_at": place_res1.retrieved_at}
            ]
            
            research_context = json.dumps({
                "places_data": [place_res1.data],
                "hours_data": [hours_res1.data]
            }, indent=2)

            prompt = ATTRACTION_RESEARCH_PROMPT.format(
                context=destination,
                research_context=research_context
            )
            
            attractions_res = await self.gemini_client.generate_structured(
                prompt=prompt,
                schema=AttractionList
            )
            
            result_data = {
                "results": attractions_res.model_dump(),
                "sources": sources
            }
            
            await Cache.set(cache_key, result_data, ttl=86400 * 7)
            
            return AgentResult(
                agent_name=self.name,
                status="success",
                data=result_data
            )
        except Exception as e:
            return AgentResult(
                agent_name=self.name,
                status="failed",
                metadata={"error": str(e)}
            )
