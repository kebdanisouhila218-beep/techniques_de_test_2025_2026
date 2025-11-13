# tests/test_app.py

import pytest
from triangulator.app import app
import requests
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

# --- Tests d'API ---

def test_triangularion_valid_id(client, mocker):
    # Mock la réponse du PointSetManager
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = (
        b'\x03\x00\x00\x00' +  # 3 points
        b'\x00\x00\x00\x00' * 6  # 3 fois (0.0, 0.0)
    )
    mocker.patch("requests.get", return_value=mock_response)

    response = client.post("/triangulate", json={"pointset_id": "123"})
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/octet-stream"
    # Plus tard, tu vérifieras que le contenu binaire est valide

def test_triangularion_invalid_id(client, mocker):
    mock_response = Mock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)

    response = client.post("/triangulate", json={"pointset_id": "999"})
    assert response.status_code == 404

def test_triangularion_no_id(client):
    response = client.post("/triangulate", json={})
    assert response.status_code == 400

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}