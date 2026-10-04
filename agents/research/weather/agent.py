import json
from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from tools.weather import get_weather, get_forecast
from apps.backend.app.core.redis import Cache
from .schema import WeatherResult
from .prompt import WEATHER_RESEARCH_PROMPT

class WeatherAgent(BaseAgent):
    name = "WeatherAgent"

    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            intent = state.get("trip", {}).get("intent") or {}
            destination = intent.get("destination", "")
            
            if not destination:
                return AgentResult(agent_name=self.name, status="success", data={"skipped": True, "reason": "Missing destination"})

            cache_key = f"research:weather:{destination}"
            
            cached_result = await Cache.get(cache_key)
            if cached_result:
                return AgentResult(agent_name=self.name, status="success", data=cached_result, metadata={"cached": True})

            w_res = await get_weather(destination, "2026-01-01")
            f_res = await get_forecast(destination)
            
            research_context = json.dumps({"weather_data": w_res.data, "forecast_data": f_res.data}, indent=2)
            
            prompt = WEATHER_RESEARCH_PROMPT.format(
                context=destination,
                research_context=research_context
            )
            
            res = await self.gemini_client.generate_structured(prompt=prompt, schema=WeatherResult)
            
            result_data = {
                "results": res.model_dump(),
                "sources": [{"source_url": w_res.source, "retrieved_at": w_res.retrieved_at}]
            }
            
            await Cache.set(cache_key, result_data, ttl=86400 * 7)
            
            return AgentResult(agent_name=self.name, status="success", data=result_data)
        except Exception as e:
            return AgentResult(agent_name=self.name, status="failed", metadata={"error": str(e)})
