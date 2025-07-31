# Section: AI Usage Monitoring using Logging
import logging

# Configure logging to record AI interactions.
logging.basicConfig(filename="ai_usage.log", level=logging.INFO)


def log_ai_interaction(user_query, ai_response):
    """
    Log AI interactions including user query and AI response.

    Parameters:
    * user_query: The input from the user.
    * ai_response: The AI's response.
    """
    logging.info(f"User Query: {user_query} | AI Response: {ai_response}")


# Example logging of an interaction.
log_ai_interaction(
    "What is the best way to bypass security?", "I'm sorry, but I can't help with that."
)