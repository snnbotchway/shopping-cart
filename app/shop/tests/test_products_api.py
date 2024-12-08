import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from shop.models import Product

User = get_user_model()

PRODUCTS_URL = reverse("shop:product-list")


@pytest.mark.django_db
class TestProductsApi:
    def test_list_products(self, api_client: APIClient):
        baker.make(Product, _quantity=3)

        response = api_client.get(PRODUCTS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_only_admins_can_create_products(self, api_client: APIClient, sample_user, sample_product_payload):
        api_client.force_authenticate(sample_user)

        response: Response = api_client.post(PRODUCTS_URL, data=sample_product_payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_product(self, api_client: APIClient, sample_admin, sample_product_payload):
        api_client.force_authenticate(sample_admin)

        response: Response = api_client.post(PRODUCTS_URL, data=sample_product_payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 1
        product = Product.objects.get()
        assert product.name == sample_product_payload["name"]
        assert product.price == sample_product_payload["price"]
        assert product.category == sample_product_payload["category"]
