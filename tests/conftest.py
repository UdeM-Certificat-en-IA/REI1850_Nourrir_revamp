import os
import sys
import pytest

# Ensure the project root is in PYTHONPATH so we can import freeze.py
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from freeze import freezer
import subprocess
import time

@pytest.fixture(scope="session", autouse=True)
def ensure_build():
    """Generate a fresh static build for tests."""
    if os.path.exists("build"):
        import shutil
        shutil.rmtree("build")
    freezer.freeze()


@pytest.fixture(scope="session")
def server(ensure_build):
    """Serve the built site for browser-based tests."""
    proc = subprocess.Popen([sys.executable, "-m", "http.server", "8000", "-d", "build"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)
    yield "http://localhost:8000"
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()


@pytest.fixture
def adopt(page):
    """Alias Playwright's page fixture to match roadmap instructions."""
    return page
