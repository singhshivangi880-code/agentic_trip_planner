from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from agents.preparation.packing.schema import PackingList
from agents.preparation.packing.prompt import PACKING_SYSTEM_PROMPT
import json

class PackingAgent(BaseAgent):
    name = "PackingAgent"
    
    def __init__(self):
        self.client = GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            itinerary = state.get("itinerary", {})
            research = state.get("research", {})
            
            # Extract relevant context
            destination = state.get("trip", {}).get("intent", {}).get("destination", "Unknown")
            weather_data = research.get("weather", {})
            
            context = f"Destination: {destination}\n"
            context += f"Weather Context: {json.dumps(weather_data)}\n"
            
            # Extract high-level activities instead of raw full itinerary to save tokens
            activities = []
            if "days" in itinerary:
                for day in itinerary["days"]:
                    for item in day.get("items", []):
                        if item.get("item_type") == "Activity":
                            activities.append(item.get("title"))
                            
            context += f"Planned Activities: {', '.join(activities)}\n"
            
            user_prompt = f"Please generate a packing list based on the following context:\n{context}"
            
            packing_list_data = await self.client.generate_structured(
                prompt=user_prompt,
                schema=PackingList,
                system_instruction=PACKING_SYSTEM_PROMPT
            )
            
            if not packing_list_data:
                return AgentResult(agent_name=self.name, status="failed", metadata={"error": "Failed to generate packing list"})
            
            # Validate schema
            packing_list = PackingList(**packing_list_data)
            
            return AgentResult(
                agent_name=self.name,
                status="success",
                data={"packing_list": packing_list.model_dump()}
            )
        except Exception as e:
            return AgentResult(agent_name=self.name, status="failed", metadata={"error": str(e)})
