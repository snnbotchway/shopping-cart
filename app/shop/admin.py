from django.contrib import admin

from .models import Cart, CartItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price"]
    search_fields = ["name", "category"]
    ordering = ["name"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity"]
    search_fields = ["cart__user__email", "product__name"]
    ordering = ["cart__user__email", "product__name"]


class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "updated_at"]
    search_fields = ["user__email"]
    ordering = ["user__email"]
    inlines = [CartItemInline]
