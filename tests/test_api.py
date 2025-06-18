import os
import sys
from unittest import mock
import json
import pytest

# Ensure local app module is loaded
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_models_endpoint(client):
    fake_models = {"data": [{"id": "m1"}, {"id": "m2"}]}
    with mock.patch("app.requests.get") as mock_get:
        mock_resp = mock.Mock(status_code=200)
        mock_resp.json.return_value = fake_models
        mock_get.return_value = mock_resp
        resp = client.get("/models")
    assert resp.status_code == 200
    assert resp.is_json
    assert resp.get_json()["models"] == ["m1", "m2"]


def test_performance_section(client):
    resp = client.get("/performance/01_purpose_scope")
    assert resp.status_code == 200
    # Page is in French; ensure a key heading exists
    assert b"Objet et port\xc3\xa9e" in resp.data


def test_performance_invalid_section(client):
    with pytest.raises(Exception):
        client.get("/performance/unknown_section")
