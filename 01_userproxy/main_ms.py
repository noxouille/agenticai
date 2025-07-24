import os
import sys

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

import asyncio

load_dotenv(override=True)

# Append the project root to sys.path for module discovery
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

# Create an assistant agent with a given name, LLM configuration, and system prompt.
assistant = AssistantAgent(
    name="Assistant",  # Name of the assistant
    model_client=model_client,
    system_message="You are a helpful AI assistant.",  # Instruction for the assistant
    model_client_stream =True
)

message = TextMessage(content="Tell me a joke.", source="user")


agent = UserProxyAgent("User")

async def main():
    response = await agent.on_messages([message], cancellation_token=CancellationToken())
    assert isinstance(response.chat_message, TextMessage)
    print(f"Your query: {response.chat_message.content}")

if __name__ == "__main__":
    asyncio.run(main())

# user_proxy.chat_with_assistant(assistant, message="Tell me a joke.")