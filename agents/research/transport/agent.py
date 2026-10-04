import json
from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from tools.transport import search_transport
from apps.backend.app.core.redis import Cache
from .schema import TransportList
from .prompt import TRANSPORT_RESEARCH_PROMPT

class TransportAgent(BaseAgent):
    name = "TransportAgent"

    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            intent = state.get("trip", {}).get("intent") or {}
            origin = intent.get("origin", "")
            destination = intent.get("destination", "")
            
            if not origin or not destination:
                return AgentResult(agent_name=self.name, status="success", data={"skipped": True, "reason": "Missing origin/destination"})

            cache_key = f"research:transport:{origin}:{destination}"
            
            cached_result = await Cache.get(cache_key)
            if cached_result:
                return AgentResult(agent_name=self.name, status="success", data=cached_result, metadata={"cached": True})

            trans_res = await search_transport(origin, destination, "2026-01-01")
            
            research_context = json.dumps({"transport_data": trans_res.data}, indent=2)
            context = f"Origin: {origin}, Destination: {destination}"

            prompt = TRANSPORT_RESEARCH_PROMPT.format(
                context=context,
                research_context=research_context
            )
            
            res = await self.gemini_client.generate_structured(prompt=prompt, schema=TransportList)
            
            result_data = {
                "results": res.model_dump(),
                "sources": [{"source_url": trans_res.source, "retrieved_at": trans_res.retrieved_at}]
            }
            
            await Cache.set(cache_key, result_data, ttl=86400 * 7)
            
            return AgentResult(agent_name=self.name, status="success", data=result_data)
        except Exception as e:
            return AgentResult(agent_name=self.name, status="failed", metadata={"error": str(e)})
