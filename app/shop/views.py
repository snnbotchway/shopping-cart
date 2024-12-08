from core.permissions import IsAdminUserOrReadOnly
from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Manage products in the database"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUserOrReadOnly]
