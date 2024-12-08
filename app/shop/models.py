from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    category = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
