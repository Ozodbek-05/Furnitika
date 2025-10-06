from django.contrib.auth import get_user_model
from django.db import models
from apps.orders.id_generator import make_order_id
from apps.pages.models import BaseModel
from apps.products.models import ProductModel

User = get_user_model()

class OrderModel(BaseModel):
    PAYMENT_CHOICES = [
        ('uzum', 'Uzum Bank'),
        ('agrobank', 'Agrobank'),
        ('tbc', 'TBC Bank'),
        ('cash', 'Cash Payment'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    unique_id = models.CharField(max_length=10, unique=True, blank=True)  # ✅ blank=True qo‘shildi
    city = models.CharField(max_length=100, default="Tashkent")
    district = models.CharField(max_length=100, default="Unknown district")
    street = models.CharField(max_length=255, default="Unknown street")
    home_number = models.CharField(max_length=50, default="N/A")
    additional_info = models.TextField(blank=True, null=True)
    note = models.TextField(null=True, blank=True)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_products = models.PositiveSmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.unique_id:  # ✅ unique_id bo‘sh bo‘lsa generatsiya qilinadi
            self.unique_id = make_order_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.unique_id} ({self.user.username})"

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
        return f"{self.product.title} × {self.quantity}"

    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
