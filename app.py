"""
NourrIR Flask Application
=========================

This Flask application serves as the backend for the NourrIR project,
providing routes for static pages, chatbot interactions via Ollama,
and other API endpoints.

It includes:
- Basic HTML page rendering.
- A proxy for Ollama chat completions (`/nurih-ami`).
- An endpoint to list available Ollama models (`/models`).
- Specific chatbot UIs for HR and testing n8n webhooks.
- Comprehensive logging and error handling.
"""
# nourrir_flask/app.py

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests
import logging

# Configure basic logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler() # Log to console
        # You could add logging.FileHandler("app.log") here as well
    ]
)
logger = logging.getLogger(__name__)

# Configuration for Ollama chat API endpoints
# For OpenAI-compatible API (v1): set OLLAMA_CHAT_URL to e.g. "https://ollama.artemis-ai.ca/v1/chat/completions"
# and OLLAMA_MODELS_URL to "https://ollama.artemis-ai.ca/v1/models".
# Fallback to legacy Ollama API (/api/chat and /api/models).
OLLAMA_CHAT_URL = os.getenv(
    "OLLAMA_CHAT_URL",
    os.getenv("OLLAMA_URL", "http://192.168.2.10:11434/api/chat")
)
OLLAMA_MODELS_URL = os.getenv(
    "OLLAMA_MODELS_URL",
    os.getenv("MODELS_URL", "http://192.168.2.10:11434/api/models")
)
# Model identifier, must match an available model from /models
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini") # Changed default model

# Log the final determined Ollama configuration
logger.info(f"Using Ollama Chat URL: {OLLAMA_CHAT_URL}")
logger.info(f"Using Ollama Models URL: {OLLAMA_MODELS_URL}")
logger.info(f"Using Default Ollama Model: {OLLAMA_MODEL}")

# Default system prompt for NuRiH Ami
SYSTEM_PROMPT = (
    "Tu es NurrIA, une intelligence artificielle bienveillante et experte en bien-être, nutrition et créativité chez NourrIR. "
    "Sois amicale, inclusive, brève et adaptée à tous publics."
)

def query_ollama(messages: list, model: str = OLLAMA_MODEL, chat_url: str = OLLAMA_CHAT_URL, timeout: int = 60) -> str | None:
    """
    Sends messages to the Ollama chat API and returns the assistant's content.

    Args:
        messages: A list of message objects to send to Ollama.
        model: The Ollama model to use for the chat completion.
        chat_url: The URL of the Ollama chat API.
        timeout: The timeout in seconds for the request.

    Returns:
        The content of the assistant's response as a string, or None if an error occurs
        or the response structure is unexpected.
    
    Raises:
        requests.exceptions.HTTPError: If Ollama returns an HTTP error status.
        requests.exceptions.RequestException: For other network-related issues.
    """
    payload = {"model": model, "messages": messages, "stream": False}
    # Redact or summarize sensitive parts of messages if necessary before logging
    # For now, logging the full message content for debug purposes.
    logger.debug(f"Sending to Ollama ({chat_url}) with model {model}: {messages}")
    
    try:
        resp = requests.post(chat_url, json=payload, timeout=timeout)
        resp.raise_for_status() # Raises HTTPError for bad responses (4XX or 5XX)
        data = resp.json()
        logger.debug(f"Ollama raw response status: {resp.status_code}")
        # Log first 500 chars of response to avoid flooding logs with huge responses
        logger.debug(f"Ollama raw response data (first 500 chars): {str(data)[:500]}")

        # OpenAI-compatible response parsing
        if isinstance(data, dict) and "choices" in data:
            choices = data.get("choices", [])
            if choices and isinstance(choices[0], dict):
                msg = choices[0].get("message", {})
                content = msg.get("content")
                if content is not None:
                    logger.debug(f"Extracted content (OpenAI format): {content[:100]}...")
                    return content
        # Fallback to legacy Ollama API format
        if isinstance(data, dict) and "message" in data:
            content = data.get("message", {}).get("content", "")
            if content: # Ensure content is not empty
                logger.debug(f"Extracted content (Legacy Ollama format): {content[:100]}...")
                return content
        
        logger.warning(f"Unexpected response structure from Ollama: {data}")
        return None # Return None if no valid content found or structure is unexpected
    except requests.exceptions.HTTPError as e:
        logger.error(f"Ollama request failed with HTTPError: {e}", exc_info=True)
        logger.error(f"Ollama response content for HTTPError: {e.response.text if e.response else 'No response content'}")
        raise # Re-raise to be caught by the route's error handler
    except requests.exceptions.RequestException as e: # Catches ConnectionError, Timeout, etc.
        logger.error(f"Ollama request failed with RequestException: {e}", exc_info=True)
        raise # Re-raise
    except Exception as e: # Catch any other unexpected errors, e.g., JSONDecodeError
        logger.error(f"An unexpected error occurred in query_ollama: {e}", exc_info=True)
        raise # Re-raise


app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Static Page Routes ---

@app.route("/")
def home():
    """Serves the main home page (index.html)."""
    return render_template("index.html")

@app.route("/politique")
def politique():
    """Serves the integration policy page (politique.html)."""
    return render_template("politique.html")

@app.route("/contact")
def contact():
    """Serves the HR contact page (contact.html)."""
    return render_template("contact.html")

@app.route("/coulisses")
def coulisses():
    """Serves the 'Les Coulisses' page (coulisses.html)."""
    return render_template("coulisses.html")

# --- Chatbot UI Routes ---

@app.route("/rh-chatbot")
def rh_chatbot():
    """Serves the dedicated HR chatbot page (rh_chatbot.html)."""
    return render_template("rh_chatbot.html")

@app.route("/test-zone")
def test_zone():
    """Serves the n8n webhook test zone page (test_zone_chatbot.html)."""
    return render_template("test_zone_chatbot.html")

# --- API Endpoints ---

@app.route("/nuria-chat", methods=["POST"]) # Renamed route
def nuria_chat(): # Renamed function
    """
    Handles chat messages from the frontend, proxies them to the Ollama API,
    and returns the AI's response.
    Accepts JSON with "message", optionally "system_prompt" and "model".
    Returns JSON with "response" or "error" and "details".
    """
    try:
        data = request.get_json(silent=True) # silent=True prevents raising an exception on bad JSON
        if not data or "message" not in data or not data["message"]: # Check if data is None or message is empty
            logger.warning("/nuria-chat: Received empty or malformed request.") # Updated log message
            return jsonify({"error": "Aucun message reçu ou format incorrect.", "details": "Request payload was missing or 'message' field was empty."}), 400

        user_msg = data["message"]
        # Consider redacting or summarizing user_msg if it can be very long or sensitive
        logger.info(f"/nuria-chat: Received message (first 100 chars): '{user_msg[:100]}...'") # Updated log message
        
        # Allow overriding system prompt or model from request for more flexibility (e.g. for RH chatbot)
        system_prompt = data.get("system_prompt", SYSTEM_PROMPT)
        model_to_use = data.get("model", OLLAMA_MODEL)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ]

        answer = query_ollama(messages, model=model_to_use) # Pass model if specified
        
        if not answer: # query_ollama might return None if content extraction fails
            logger.warning(f"/nuria-chat: No answer from Ollama or failed to extract content for user message: {user_msg[:100]}...") # Updated log message
            return jsonify({"error": "Désolé, je n'ai pas pu générer de réponse.", "details": "Failed to get a valid response from the AI model."}), 500

        logger.info(f"/nuria-chat: Sending response (first 100 chars): '{str(answer)[:100]}...'") # Updated log message
        return jsonify({"response": answer})

    except requests.exceptions.ConnectionError as e:
        logger.error(f"/nuria-chat: Ollama connection error: {e}", exc_info=True) # Updated log message
        return jsonify({"error": "Connexion à l'assistant IA impossible. Veuillez réessayer plus tard.", "details": "Connection to AI service failed."}), 502
    except requests.exceptions.Timeout as e:
        logger.error(f"/nuria-chat: Ollama timeout: {e}", exc_info=True) # Updated log message
        return jsonify({"error": "L'assistant IA n'a pas répondu à temps. Veuillez réessayer.", "details": "Request to AI service timed out."}), 504
    except requests.exceptions.HTTPError as e: # Raised by resp.raise_for_status() in query_ollama
        logger.error(f"/nuria-chat: Ollama HTTP error: {e}", exc_info=True) # Updated log message
        return jsonify({"error": "Erreur de communication avec l'assistant IA.", "details": f"AI service returned HTTP {e.response.status_code}."}), e.response.status_code if e.response else 500
    except Exception as e:
        logger.error(f"/nuria-chat: An unexpected error occurred: {e}", exc_info=True) # Updated log message
        return jsonify({"error": "Une erreur inattendue est survenue sur le serveur.", "details": str(e)}), 500

@app.route("/models", methods=["GET"])
def list_models():
    """
    Proxy endpoint to fetch available models from the configured Ollama API.
    This allows the frontend to get a list of models without directly exposing the Ollama URL.
    """
    logger.info(f"/models: Request received for model list from {OLLAMA_MODELS_URL}")
    try:
        resp = requests.get(OLLAMA_MODELS_URL, timeout=10) # Short timeout for model listing
        resp.raise_for_status()
        data = resp.json()
        logger.debug(f"/models: Raw response from Ollama: {str(data)[:500]}") # Log part of the response
        
        models = []
        # Handle different possible structures for model listing (OpenAI-like vs legacy Ollama)
        if isinstance(data, dict) and "data" in data and isinstance(data["data"], list): # OpenAI /v1/models format
            for entry in data["data"]:
                if isinstance(entry, dict):
                    model_id = entry.get("id") or entry.get("name") # 'id' for OpenAI, 'name' sometimes used
                    if model_id:
                        models.append(model_id)
        elif isinstance(data, dict) and "models" in data and isinstance(data["models"], list): # Legacy /api/tags or /api/models format
             for entry in data["models"]:
                if isinstance(entry, dict):
                    model_name = entry.get("name") # Usually 'name' in legacy
                    if model_name:
                        models.append(model_name)
        else:
            logger.warning(f"/models: Unexpected data structure for models: {data}")

        logger.info(f"/models: Successfully fetched {len(models)} models. Models: {models}")
        return jsonify(models=models)
    except requests.exceptions.RequestException as e:
        logger.error(f"/models: Error connecting to Ollama models endpoint: {e}", exc_info=True)
        return jsonify({"error": "Impossible de récupérer la liste des modèles IA.", "details": str(e)}), 502
    except Exception as e:
        logger.error(f"/models: An unexpected error occurred while listing models: {e}", exc_info=True)
        return jsonify({"error": "Une erreur inattendue est survenue lors de la récupération des modèles.", "details": str(e)}), 500

# --- Static Asset Serving ---

@app.route('/assets/<path:filename>')
def serve_assets(filename: str):
    """Serves static files from the 'static/assets' directory."""
    return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)

@app.route('/favicon.ico')
def favicon():
    """Serves the favicon.ico from the static folder."""
    return send_from_directory(app.static_folder, 'favicon.ico')

# --- Main Application Execution ---

if __name__ == "__main__":
    # Note: Flask's default debug mode is generally not recommended for production.
    # Use a production-ready WSGI server (e.g., Gunicorn, Waitress) in production.
    app.run(debug=True, host="0.0.0.0", port=8080)
