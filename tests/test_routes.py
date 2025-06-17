import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200

def test_politique(client):
    resp = client.get('/politique')
    assert resp.status_code == 200

def test_contact(client):
    resp = client.get('/contact')
    assert resp.status_code == 200

def test_performance(client):
    resp = client.get('/performance')
    assert resp.status_code == 200
