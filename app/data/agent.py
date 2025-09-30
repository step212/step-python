from app.configs.config import settings
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, OpenAIResponsesModel, set_tracing_disabled

deepseek_api_key = settings.DEEPSEEK_API_KEY

set_tracing_disabled(True)

# Initialize the DeepSeek client
client = AsyncOpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key=deepseek_api_key
)

# Configure the model
model_config_chat = OpenAIChatCompletionsModel(
    model="deepseek-chat",
    openai_client=client
)

model_config_reasoner = OpenAIChatCompletionsModel(
    model="deepseek-reasoner",
    openai_client=client
)

base_agent = Agent(
    name="Basic Agent", 
    handoff_description="Basic agent for basic questions",
    instructions="可以通过MCP查询表hero的信息来获取英雄的信息",
    model=model_config_chat
)






