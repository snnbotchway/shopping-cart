from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")

app_name = "shop"

urlpatterns = [
    path("", include(router.urls)),
]
