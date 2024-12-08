from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CartViewSet, ProductViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("cart", CartViewSet, basename="cart")

app_name = "shop"

urlpatterns = [
    path("", include(router.urls)),
]
