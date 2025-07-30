import os
from dotenv import load_dotenv

load_dotenv()

GENERATION_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
AGENT_MODEL = "google/gemma-3n-E4B-it"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
API_KEY = os.getenv("TOGETHERAI_API_KEY")

config_list = [
  {
    "model": AGENT_MODEL,
    "api_type":"together",
    "api_key": API_KEY,
    "stream": False,
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