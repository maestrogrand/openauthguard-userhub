from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.main import app

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
