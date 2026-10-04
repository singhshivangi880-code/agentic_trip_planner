import json
from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from .schema import TripIntent
from .prompt import INTENT_EXTRACTION_PROMPT

class IntentAgent(BaseAgent):
    name = "IntentAgent"

    def __init__(self, gemini_client: GeminiClient = None):
        # ponytail: default dependency injection
        self.gemini_client = gemini_client or GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        trip = state.get("trip", {})
        profile = state.get("profile", {})
        
        # ponytail: simpler to just dump the dicts than to build complex prompts
        prompt = INTENT_EXTRACTION_PROMPT.format(
            request=json.dumps(trip, indent=2),
            profile=json.dumps(profile, indent=2)
        )
        
        try:
            intent = await self.gemini_client.generate_structured(
                prompt=prompt,
                schema=TripIntent
            )
            return AgentResult(
                agent_name=self.name,
                status="success",
                data=intent.model_dump(),
            )
        except Exception as e:
            return AgentResult(
                agent_name=self.name,
                status="failed",
                metadata={"error": str(e)}
            )
