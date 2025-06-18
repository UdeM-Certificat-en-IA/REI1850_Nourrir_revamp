from app import app
from serverless_wsgi import handle_request
import os

# Strip the Netlify functions base path so Flask routes work correctly
# Read from API_GATEWAY_BASE_PATH env variable with a default
BASE_PATH = os.getenv("API_GATEWAY_BASE_PATH", "/.netlify/functions/flask_app")

def handler(event, context):
    # Remove the function's base path prefix so Flask sees the correct route
    path = event.get("path", "")
    if path.startswith(BASE_PATH):
        event["path"] = path[len(BASE_PATH):] or "/"
    return handle_request(app, event, context)
