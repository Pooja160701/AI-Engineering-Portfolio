import pytest
from api.client.api_client import APIClient
from jsonschema import validate

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

@pytest.mark.api
@pytest.mark.regression
def test_product_schema_validation():
    client = APIClient()
    response = client.get("/products/1")

    product_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "title": {"type": "string"},
            "price": {"type": "number"},
            "description": {"type": "string"},
            "category": {"type": "string"},
            "image": {"type": "string"}
        },
        "required": ["id", "title", "price"]
    }

    validate(instance=response.json(), schema=product_schema)

@pytest.mark.api
@pytest.mark.smoke
def test_products_response_time():
    client = APIClient()
    response = client.get("/products")

    assert response.elapsed.total_seconds() < 2