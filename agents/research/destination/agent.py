import json
from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from tools.search import search, fetch
from apps.backend.app.core.redis import Cache
from .schema import DestinationOverview
from .prompt import DESTINATION_RESEARCH_PROMPT

class DestinationAgent(BaseAgent):
    name = "DestinationAgent"

    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            intent = state.get("trip", {}).get("intent") or {}
            destination = intent.get("destination", "")
            if not destination:
                return AgentResult(agent_name=self.name, status="success", data={"skipped": True, "reason": "No destination in intent"})

            cache_key = f"research:destination:{destination}"
            
            # Check cache first (Task 14.5)
            cached_result = await Cache.get(cache_key)
            if cached_result:
                return AgentResult(agent_name=self.name, status="success", data=cached_result, metadata={"cached": True})

            # Research workflow (Task 14.2)
            search_res = await search(query=f"Travel guide for {destination}", location=destination)
            
            # fetch the first url from search if possible (we are mocking, so we'll just mock a fetch)
            url = "http://example.com/guide"
            fetch_res = await fetch(url)
            
            # Source capture (Task 14.3)
            sources = [
                {"source_url": "mock_search", "source_name": "Search API", "retrieved_at": search_res.retrieved_at},
                {"source_url": url, "source_name": "Guide Page", "retrieved_at": fetch_res.retrieved_at}
            ]
            
            research_context = json.dumps({
                "search_data": search_res.data,
                "fetch_data": fetch_res.data
            }, indent=2)

            # Gemini synthesis
            prompt = DESTINATION_RESEARCH_PROMPT.format(
                intent=json.dumps(intent, indent=2),
                research_context=research_context
            )
            
            overview = await self.gemini_client.generate_structured(
                prompt=prompt,
                schema=DestinationOverview
            )
            
            result_data = {
                "overview": overview.model_dump(),
                "sources": sources
            }
            
            # Cache the result
            await Cache.set(cache_key, result_data, ttl=86400 * 7) # 1 week
            
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
