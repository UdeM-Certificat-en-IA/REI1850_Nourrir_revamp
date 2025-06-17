#!/usr/bin/env python3
"""
Quick smoke test for the RH chatbot n8n webhook endpoint.
Sends a sample POST request and prints status and response.
"""
import requests
import uuid

def test_rh_n8n():
    # RH chatbot n8n webhook URL
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
    print(f"Sending POST to RH N8N webhook: {url}")
    try:
        resp = requests.post(url, json=payload, timeout=30)
        print(f"Status code: {resp.status_code}")
        try:
            data = resp.json()
            # Attempt to extract a meaningful answer, accounting for typical n8n response formats
            answer = None
            if isinstance(data, dict):
                for key in ("response", "answer", "output", "text", "message"):
                    if key in data and isinstance(data[key], str):
                        answer = data[key]
                        break
            if answer:
                print("Parsed answer:", answer)
            else:
                print("Response JSON:", data)
        except ValueError:
            print("Response text:", resp.text)
    except Exception as e:
        print("Error during request:", e)

if __name__ == '__main__':
    test_rh_n8n()
