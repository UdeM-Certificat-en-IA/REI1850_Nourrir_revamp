import os
import sys
import pytest
from flask import url_for

# Ensure the application module is importable when running tests, even if the
# project root isn't automatically added to PYTHONPATH. This avoids failures
# caused by an installed package named ``app`` shadowing our local module.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
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
    resp = client.get('/politique/')
    assert resp.status_code == 200

def test_politique_redirect(client):
    resp = client.get('/politique')
    assert resp.status_code in (301, 302, 308)

def test_contact(client):
    resp = client.get('/contact')
    assert resp.status_code == 200

def test_performance(client):
    resp = client.get('/performance')
    assert resp.status_code == 200

def test_performance_stage_buttons(client):
    resp = client.get('/performance')
    html = resp.data.decode('utf-8')
    assert 'class="stage-button semis"' in html
    assert url_for('performance_section', section='01_phase1_semis') in html
    assert 'class="stage-button croissance"' in html
    assert url_for('performance_section', section='04_phase4_renouvellement') in html

def test_coulisses(client):
    resp = client.get('/coulisses')
    assert resp.status_code == 200

def test_rh_chatbot(client):
    resp = client.get('/rh-chatbot')
    assert resp.status_code == 200

def test_test_zone(client):
    resp = client.get('/test-zone')
    assert resp.status_code == 200

def test_test_page(client):
    resp = client.get('/test')
    assert resp.status_code == 200
