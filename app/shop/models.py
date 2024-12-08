import os

from config.storage import OVERWRITE_STORAGE
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class ImageUploadPaths:
    base_path = os.path.join("uploads", "products")

    @staticmethod
    def _get_extension(filename):
        return filename.split(".")[-1]

    @classmethod
    def thumbnail(cls, instance: "Product", filename: str) -> str:
        extension = ImageUploadPaths._get_extension(filename)
        return os.path.join(cls.base_path, str(instance.product.id), f"thumbnail.{extension}")

    @classmethod
    def mobile(cls, instance: "Product", filename: str) -> str:
        extension = ImageUploadPaths._get_extension(filename)
        return os.path.join(cls.base_path, str(instance.product.id), f"mobile.{extension}")

    @classmethod
    def tablet(cls, instance: "Product", filename: str) -> str:
        extension = ImageUploadPaths._get_extension(filename)
        return os.path.join(cls.base_path, str(instance.product.id), f"tablet.{extension}")

    @classmethod
    def desktop(cls, instance: "Product", filename: str) -> str:
        extension = ImageUploadPaths._get_extension(filename)
        return os.path.join(cls.base_path, str(instance.product.id), f"desktop.{extension}")


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    category = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProductImageSet(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="images")
    thumbnail = models.ImageField(upload_to=ImageUploadPaths.thumbnail, blank=True, null=True, storage=OVERWRITE_STORAGE)
    mobile = models.ImageField(upload_to=ImageUploadPaths.mobile, blank=True, null=True, storage=OVERWRITE_STORAGE)
    tablet = models.ImageField(upload_to=ImageUploadPaths.tablet, blank=True, null=True, storage=OVERWRITE_STORAGE)
    desktop = models.ImageField(upload_to=ImageUploadPaths.desktop, blank=True, null=True, storage=OVERWRITE_STORAGE)

    def __str__(self):
        return f"ProductImageSet for {self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10_000_000)])

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"

    class Meta:
        unique_together = ("cart", "product")
