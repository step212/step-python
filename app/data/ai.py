from app.data.agent import base_agent
from agents import Runner, Agent

class AI:
    def __init__(self):
        self.base_agent = base_agent

    def get_base_agent(self) -> Agent:
        return self.base_agent

    async def get_base_agent_response(self, message: str) -> str:
        response = await Runner.run(self.base_agent, message)
        return response.final_output






