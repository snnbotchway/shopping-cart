import pytest


@pytest.fixture
def sample_product_payload():
    return {"name": "Test Product", "price": 10.00, "category": "Test Category"}
