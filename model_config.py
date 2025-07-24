import os
from dotenv import load_dotenv
from autogen import LLMConfig

load_dotenv()

config_list = [
  {
    "model": "gpt-4o-mini",
    "api_key": os.getenv("OPENAI_API_KEY"),
    "base_url": os.getenv("OPENAI_API_BASE")
  }
]

# agent_config = {
#   "seed": 42,
#   "temperature": 0.7,
#   "request_timeout": 120,
#   "max_retries": 3,
# }


# llm config
llm_config= {
        "config_list": config_list,
        "timeout": 600,
        "cache_seed": None,
        "temperature": 0.7,
        "seed": 42 # for reproducibility
    }