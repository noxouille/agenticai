# Section: Flask API Rate Limiting
from flask import Flask, request, jsonify
from flask_limiter import Limiter

# Create Flask application instance.
app = Flask(__name__)
# Initialize rate limiter using the remote address as key.
limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr
)

@app.route("/ai-service", methods=["POST"])
@limiter.limit("5 per minute")  # Limit to 5 requests per minute per IP.
def ai_service():
    """
    API endpoint for AI service.

    Processes a JSON payload with a query and returns an AI response.
    """
    query = request.json.get("query")
    response = "AI response here"  # Placeholder for actual AI response logic.
    return jsonify({"response": response})


if __name__ == "__main__":
    # Run the Flask application.
    app.run()