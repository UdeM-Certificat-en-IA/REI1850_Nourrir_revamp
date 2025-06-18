import os
import sys
import pytest

# Ensure the project root is in PYTHONPATH so we can import freeze.py
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from freeze import freezer

@pytest.fixture(scope="session", autouse=True)
def ensure_build():
    """Generate the static build if it doesn't exist."""
    if not os.path.exists("build/index.html"):
        freezer.freeze()
