import pytest
from fastapi.testclient import TestClient

from app.main import app
from .helpers import clear_notes


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        clear_notes(test_client)
        yield test_client
        clear_notes(test_client)
