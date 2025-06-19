import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app

ASSET_PATHS = [
    "NEW_Images/phase1_semis_nourrir.png",
    "NEW_Images/tableau_bord_suivi_nourrir.png",
    "NEW_Images/phase2_croissance_nourrir.png",
    "NEW_Images/feedback_evaluation_nourrir.png",
    "NEW_Images/coaching_accompagnement_nourrir.png",
    "NEW_Images/phase3_recolte_nourrir.png",
    "NEW_Images/plan_croissance_personnalise_nourrir.png",
    "NEW_Images/reconnaissance_celebration_nourrir.png",
    "NEW_Images/phase4_renouvellement_nourrir.png",
    "NEW_Images/retrospectives_collectives_nourrir.png",
    "NEW_Images/parcours_soutien_nourrir.png",
    "NEW_Images/meeting_office_nourrir.png",
    "NEW_Images/thumbnail_gestion_performance_nourrir.png",
    "NEW_Images/ia_ethique_nourrir.png",
]

@pytest.fixture

def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("path", ASSET_PATHS)
def test_asset_served(client, path):
    resp = client.get(f"/assets/{path}")
    assert resp.status_code == 200
    assert resp.data  # ensure file not empty
