import pytest
from fastapi.testclient import TestClient

from src.presentation.main import app


@pytest.fixture
def test_client():
    return TestClient(app)
