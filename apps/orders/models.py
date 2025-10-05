from django.contrib.auth import get_user_model
from django.db import models

from apps.pages.models import BaseModel
from apps.products.models import ProductModel

User = get_user_model()


class OrderModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    unique_id = models.CharField(max_length=10, unique=True)
    note = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    total_products = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.user.full_name

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderItemModel(BaseModel):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        ProductModel, on_delete=models.SET_NULL,
        related_name='order_items',
        null=True, blank=True
    )

    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'

