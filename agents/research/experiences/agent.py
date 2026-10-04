import json
from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from tools.search import search
from apps.backend.app.core.redis import Cache
from .schema import ExperienceList
from .prompt import EXPERIENCE_RESEARCH_PROMPT

class ExperienceAgent(BaseAgent):
    name = "ExperienceAgent"

    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            intent = state.get("trip", {}).get("intent") or {}
            destination = intent.get("destination", "")
            if not destination:
                return AgentResult(agent_name=self.name, status="success", data={"skipped": True, "reason": "No destination in intent"})

            cache_key = f"research:experiences:{destination}"
            
            cached_result = await Cache.get(cache_key)
            if cached_result:
                return AgentResult(agent_name=self.name, status="success", data=cached_result, metadata={"cached": True})

            search_res = await search(query=f"Local experiences and workshops in {destination}")
            
            research_context = json.dumps({"search_data": search_res.data}, indent=2)

            prompt = EXPERIENCE_RESEARCH_PROMPT.format(
                context=destination,
                research_context=research_context
            )
            
            experiences_res = await self.gemini_client.generate_structured(
                prompt=prompt,
                schema=ExperienceList
            )
            
            result_data = {
                "results": experiences_res.model_dump(),
                "sources": [{"source_url": search_res.source, "retrieved_at": search_res.retrieved_at}]
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
