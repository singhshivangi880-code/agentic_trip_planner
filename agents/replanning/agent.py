from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.common.gemini.client import GeminiClient
from agents.itinerary.schema import Itinerary, TripDay
from agents.validation.validators.engine import validate_itinerary
import json

class ReplanningAgent(BaseAgent):
    name = "ReplanningAgent"
    
    def __init__(self):
        self.client = GeminiClient()

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            itinerary_data = state.get("itinerary", {})
            replanning_request = state.get("replanning_request", {})
            
            if not itinerary_data or not replanning_request:
                return AgentResult(agent_name=self.name, status="failed", metadata={"error": "Missing itinerary or replanning request"})

            target_day_index = replanning_request.get("target_day")
            instruction = replanning_request.get("instruction")
            
            if target_day_index is None or not instruction:
                 return AgentResult(agent_name=self.name, status="failed", metadata={"error": "Invalid request"})
            
            itinerary = Itinerary(**itinerary_data)
            
            # 1 & 2: Extract the affected day
            target_day = None
            for d in itinerary.days:
                if d.day_index == target_day_index:
                    target_day = d
                    break
                    
            if not target_day:
                return AgentResult(agent_name=self.name, status="failed", metadata={"error": "Day not found"})

            # 3. Prompt Gemini to fix this specific day
            from agents.replanning.prompt import REPLANNING_SYSTEM_PROMPT
            user_prompt = f"Original Day:\n{target_day.model_dump_json(indent=2)}\n\nInstruction:\n{instruction}"
            
            updated_day_data = await self.client.generate_structured(
                prompt=user_prompt,
                schema=TripDay,
                system_instruction=REPLANNING_SYSTEM_PROMPT
            )
            
            if not updated_day_data:
                return AgentResult(agent_name=self.name, status="failed", metadata={"error": "Failed to generate updated day"})

            # Reconstruct and validate
            updated_day = updated_day_data
            
            # Replace day in itinerary
            for i, d in enumerate(itinerary.days):
                if d.day_index == target_day_index:
                    itinerary.days[i] = updated_day
                    break
                    
            # 6. Revalidate
            intent = state.get("trip", {}).get("intent", {})
            result = validate_itinerary(itinerary, intent.get("start_date", "2026-01-01"), intent.get("end_date", "2026-12-31"))
            
            if not result.is_valid:
                return AgentResult(
                    agent_name=self.name,
                    status="failed",
                    metadata={"error": "Replanned itinerary is invalid", "validation_errors": result.errors}
                )
            
            return AgentResult(
                agent_name=self.name,
                status="success",
                data={"itinerary": itinerary.model_dump()}
            )
        except Exception as e:
            return AgentResult(agent_name=self.name, status="failed", metadata={"error": str(e)})
