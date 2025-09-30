from app.data.ai import AI
from app.biz.tool import do_some_work
from agents.mcp import MCPServerStreamableHttp

class AIBiz:
    def __init__(self):
        self.ai = AI()
        self.agent = self.ai.get_base_agent()
        self.agent.tools.append(do_some_work)
        self.mcp_server = None

    async def initialize_mcp_server(self):
        """Initialize the MCP server and add it to the agent"""
        self.mcp_server = MCPServerStreamableHttp(
            name="Streamable HTTP Python Server",
            params={
                "url": "http://localhost:3000/mcp",
            },
        )

        # Connect to the MCP server
        await self.mcp_server.connect()

        # Add the MCP server to the agent's mcp_servers list
        if not hasattr(self.agent, 'mcp_servers'):
            self.agent.mcp_servers = []
        self.agent.mcp_servers.append(self.mcp_server)
        
        print("MCP server initialized, connected, and added to agent")
        return self.mcp_server

    async def get_base_agent_response(self, message: str) -> str:
        return await self.ai.get_base_agent_response(message)


