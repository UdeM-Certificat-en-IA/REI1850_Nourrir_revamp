#!/usr/bin/env python3
"""
Simple smoke test for the RH chatbot n8n webhook endpoint.
Sends a sample POST request and ensures a 200 response.
"""
import unittest
import uuid
import requests


def call_rh_n8n():
    """Send a sample request to the webhook and return the response."""
    url = (
        'https://n8n.artemis-ai.ca:8443/webhook/'
        '3856912a-4b68-441b-ba1a-beb4e64356e0/chat'
    )
    payload = {
        "message": "Quelle est la politique de télétravail chez NourrIR?",
        "sessionId": str(uuid.uuid4()),
        "system_prompt": (
            "Tu es l'assistant RH de NourrIR. Réponds de façon concise."
        )
    }
    return requests.post(url, json=payload, timeout=30)


class TestRHWebhook(unittest.TestCase):
    def test_rh_n8n(self):
        resp = call_rh_n8n()
        self.assertEqual(resp.status_code, 200)
        # Attempt to parse JSON and print information for debugging
        try:
            data = resp.json()
        except ValueError:
            data = resp.text
        print("Response:", data)


if __name__ == '__main__':

    test_rh_n8n()
