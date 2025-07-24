import os
import sys

# Import the autogen package for creating agents
import autogen
# import logging
# from autogen import Token # ERROR!

# Enable Debug Logging
# logging.basicConfig(level=logging.DEBUG)

# Append the project root to sys.path for module discovery
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Import configuration settings from model_config module
from model_config import *

# Create an assistant agent with a given name, LLM configuration, and system prompt.
assistant = autogen.AssistantAgent(
    name="Assistant",  # Name of the assistant
    llm_config=llm_config,  # Language model configuration
    system_message="You are a helpful AI assistant.",  # Instruction for the assistant
)

# Create a user proxy agent with parameters for human input mode and code execution configuration.
user_proxy = autogen.UserProxyAgent(
    name="User",  # Name of the user proxy
    human_input_mode="TERMINATE",  # Wait for human input before auto-reply
    max_consecutive_auto_reply=1,  # Maximum auto-replies allowed consecutively
    code_execution_config={  # Configuration for code execution environment
        "use_docker": False,  # Disable Docker usage
        "last_n_messages": 3,  # Include last 3 messages in context
        "work_dir": "workspace",  # Working directory for code execution
    },
)


# # Monitor conversation flow
# assistant.register_reply(lambda sender, message: print(f"{sender}: {message}"))

# # Create token counter
# token_counter = Token()
# # Register with agent
# assistant.register_token_counter(token_counter)


# Start a conversation by initiating a chat between the user proxy and the assistant agent
user_proxy.initiate_chat(assistant, message="Write a simple Python function to calculate factorial.")