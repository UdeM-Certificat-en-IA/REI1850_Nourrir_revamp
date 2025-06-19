import os
import sys
from unittest import mock
import pytest

# Ensure local app module is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import query_ollama, get_response_with_fallback


def test_query_ollama_openai_structure():
    messages = [{"role": "user", "content": "Hello"}]
    response_data = {
        "choices": [
            {"message": {"content": "Hi there"}}
        ]
    }
    with mock.patch("app.requests.post") as mock_post:
        mock_resp = mock.Mock(status_code=200)
        mock_resp.json.return_value = response_data
        mock_post.return_value = mock_resp
        result = query_ollama(messages)
    assert result == "Hi there"


def test_get_response_with_fallback_uses_secondary_model():
    messages = [{"role": "user", "content": "Hi"}]
    # First call to query_ollama will raise, second will succeed
    with mock.patch("app.query_ollama", side_effect=[Exception("boom"), "ok"]):
        with mock.patch("app.requests.get") as mock_get:
            mock_get.return_value = mock.Mock(status_code=200, json=lambda: {
                "data": [{"id": "primary"}, {"id": "secondary"}]
            })
            result = get_response_with_fallback(messages, initial_model="primary")
    assert result == "ok"
