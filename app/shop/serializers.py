from rest_framework import serializers

from .models import Cart, CartItem, Product, ProductImageSet


class ProductImageSetSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(required=False)
    mobile = serializers.ImageField(required=False)
    tablet = serializers.ImageField(required=False)
    desktop = serializers.ImageField(required=False)

    class Meta:
        model = ProductImageSet
        fields = ["thumbnail", "mobile", "tablet", "desktop"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSetSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "price",
            "description",
            "images",
        ]
        read_only_fields = ["id", "images"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "updated_at", "items"]


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]
        read_only_fields = ["cart", "product"]
