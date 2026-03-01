import pytest
from api.client.api_client import APIClient

@pytest.mark.api
@pytest.mark.smoke
def test_get_all_products():
    client = APIClient()
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

@pytest.mark.api
@pytest.mark.regression
def test_get_single_product():
    client = APIClient()
    response = client.get("/products/1")

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == 1
    assert "title" in data

@pytest.mark.api
@pytest.mark.regression
def test_get_invalid_product():
    client = APIClient()
    response = client.get("/products/99999")

    assert response.status_code in [200, 404]