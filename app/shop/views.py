from core.permissions import IsAdminUserOrReadOnly
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from shop.filters import ProductFilter

from .models import Cart, CartItem, Product, ProductImageSet
from .serializers import (
    CartItemCreateSerializer,
    CartItemSerializer,
    CartItemUpdateSerializer,
    ProductImageSetSerializer,
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    """Manage products in the database"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action == "upload_images":
            return ProductImageSetSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["post"], parser_classes=[MultiPartParser])
    def upload_images(self, request, pk=None):
        product = self.get_object()
        image_set, _ = ProductImageSet.objects.get_or_create(product=product)
        serializer = self.get_serializer(image_set, data=request.FILES, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartViewSet(viewsets.ViewSet):
    """Manage cart and cart items in the database"""

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=CartItemSerializer(many=True), description="Get all cart items")
    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=CartItemCreateSerializer,
        responses=CartItemSerializer,
        description="Add a product to the cart",
    )
    def create(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})

        if not created:
            return Response({"error": "Product already in cart"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=CartItemUpdateSerializer,
        responses=CartItemSerializer,
        description="Update the quantity of a product in the cart",
    )
    def update(self, request, pk=None):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, id=pk)

        serializer = CartItemUpdateSerializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)

    @extend_schema(responses=CartItemSerializer(many=True), description="Remove a product from the cart")
    def destroy(self, request, pk=None):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, id=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
