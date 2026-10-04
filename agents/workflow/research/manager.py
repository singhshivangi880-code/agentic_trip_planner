import asyncio
from agents.common.state import BaseAgent, TripPlanningState, AgentResult
from agents.research.destination.agent import DestinationAgent
from agents.research.attractions.agent import AttractionAgent
from agents.research.experiences.agent import ExperienceAgent
from agents.research.food.agent import FoodAgent
from agents.research.transport.agent import TransportAgent
from agents.research.weather.agent import WeatherAgent

class ResearchManager(BaseAgent):
    name = "ResearchManager"

    def __init__(self, gemini_client=None):
        self.destination_agent = DestinationAgent(gemini_client)
        self.attraction_agent = AttractionAgent(gemini_client)
        self.experience_agent = ExperienceAgent(gemini_client)
        self.food_agent = FoodAgent(gemini_client)
        self.transport_agent = TransportAgent(gemini_client)
        self.weather_agent = WeatherAgent(gemini_client)

    async def execute(self, state: TripPlanningState) -> AgentResult:
        try:
            # Ponytail: run them all concurrently
            # use return_exceptions=True so a single failure doesn't crash the manager
            results = await asyncio.gather(
                self.destination_agent.execute(state),
                self.attraction_agent.execute(state),
                self.experience_agent.execute(state),
                self.food_agent.execute(state),
                self.transport_agent.execute(state),
                self.weather_agent.execute(state),
                return_exceptions=True
            )

            research_data = {}
            for res in results:
                # If an exception was raised, skip it
                if isinstance(res, Exception):
                    continue
                # If the agent returned a success result, store it
                if res.status == "success":
                    if not res.data.get("skipped"):
                        research_data[res.agent_name] = res.data

            return AgentResult(
                agent_name=self.name,
                status="success",
                data={"research": research_data}
            )
        except Exception as e:
            return AgentResult(
                agent_name=self.name,
                status="failed",
                metadata={"error": str(e)}
            )
