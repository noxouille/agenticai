# Section: Response Filtering using Toxicity Detector
from transformers import pipeline

# Initialize toxicity detector with a pre-trained model.
toxicity_detector = pipeline("text-classification", model="unitary/toxic-bert")


def filter_toxic_response(ai_response):
    """
    Evaluate AI response for toxicity and block if score exceeds threshold.

    Parameters:
    * ai_response: String containing the AI response.

    Returns:
    * Filtered response or a block message if toxicity is high.
    """
    toxicity_score = toxicity_detector(ai_response)[0]["score"]
    print(toxicity_score)
    if toxicity_score > 0.7:
        return "Blocked: AI response contains inappropriate content."
    return ai_response


# Example usage of filter_toxic_response
ai_response = "I think certain groups of people are inferior."
print(filter_toxic_response(ai_response))