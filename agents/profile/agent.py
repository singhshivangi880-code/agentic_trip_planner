from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from .schema import EffectiveTravellerPreferences

class TravellerProfileAgent(BaseAgent):
    name = "TravellerProfileAgent"

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            profile = state.get("profile") or {}
            trip = state.get("trip") or {}
            trip_prefs = trip.get("preferences") or {}
            
            # ponytail: deterministic merge, trip overrides profile natively.
            
            interests = trip_prefs.get("interests") 
            if interests is None:
                interests = profile.get("interests", [])
                
            budget = trip_prefs.get("budget") or profile.get("budget")
            pace = trip_prefs.get("pace") or profile.get("pace")
            
            dietary = trip_prefs.get("dietary_preferences")
            if dietary is None:
                dietary = profile.get("dietary_preferences", [])
                
            group = trip_prefs.get("group_defaults")
            if group is None:
                group = profile.get("group_defaults", {})

            effective_prefs = EffectiveTravellerPreferences(
                budget=budget,
                pace=pace,
                interests=interests,
                dietary_preferences=dietary,
                group_defaults=group
            )
            
            return AgentResult(
                agent_name=self.name,
                status="success",
                data=effective_prefs.model_dump(),
            )
        except Exception as e:
            return AgentResult(
                agent_name=self.name,
                status="failed",
                metadata={"error": str(e)}
            )
