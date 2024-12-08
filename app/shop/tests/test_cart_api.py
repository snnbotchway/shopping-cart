import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from shop.models import Cart, CartItem, Product

CART_URL = reverse("shop:cart-list")


@pytest.mark.django_db
class TestCartApi:
    def test_list_cart_items(self, api_client, sample_user, other_user):
        """Test that the user can only see their own cart items."""
        cart = baker.make(Cart, user=sample_user)
        other_cart = baker.make(Cart, user=other_user)
        baker.make(CartItem, cart=cart, _quantity=3)
        baker.make(CartItem, cart=other_cart, _quantity=2)
        api_client.force_authenticate(sample_user)

        response = api_client.get(CART_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_cart_item(self, api_client, sample_user):
        """Test that the user can create a cart item."""
        product = baker.make(Product)
        api_client.force_authenticate(sample_user)

        response = api_client.post(CART_URL, data={"product": product.pk, "quantity": 1})

        assert response.status_code == status.HTTP_201_CREATED
        assert CartItem.objects.filter(cart__user=sample_user, product=product).exists()
