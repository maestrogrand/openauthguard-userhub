import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.main import app
from src.core.database import get_db

client = TestClient(app)


@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    yield db


app.dependency_overrides[get_db] = mock_db


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "up"
    assert "database" in data
    assert "version" in data
