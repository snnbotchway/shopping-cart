from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price"]
    search_fields = ["name", "category"]
    ordering = ["name"]
