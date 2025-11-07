import pytest
from triangulator.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_triangulate_route_returns_501(client):
    """
    Vérifie que l'API renvoie 501 (non implémenté)
    """
    response = client.post('/triangulate', data=b"fake_data")
    assert response.status_code == 501
