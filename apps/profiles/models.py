from django.db import models

from apps.common.utils import generate_unique_code

from apps.accounts.models import User
from apps.common.models import BaseModel
from apps.shop.models import Product

DELIVERY_STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("PACKING", "PACKING"),
    ("SHIPPING", "SHIPPING"),
    ("ARRIVING", "ARRIVING"),
    ("SUCCESS", "SUCCESS"),
)

PAYMENT_STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("PROCESSING", "PROCESSING"),
    ("SUCCESSFUL", "SUCCESSFUL"),
    ("CANCELLED", "CANCELLED"),
    ("FAILED", "FAILED"),
)


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    tx_ref = models.CharField(max_length=100, blank=True, null=True)
    delivery_status = models.CharField(
        max_length=20,
        default="PENDING",
        choices=DELIVERY_STATUS_CHOICES
    )
    payment_status = models.CharField(
        max_length=20,
        default="PENDING",
        choices=PAYMENT_STATUS_CHOICES
    )

    date_delivered = models.DateTimeField(null=True, blank=True)

    full_name = models.CharField(max_length=1000, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=1000, null=True)
    city = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=100, null=True)
    zipcode = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user}'s order"

    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            self.tx_ref = generate_unique_code(Order, "tx_ref")
        super().save(*args, **kwargs)


class OrderItem(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(
        Order,
        related_name="order_items",
        null=True,
        on_delete=models.CASCADE,
        blank=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-created_at"]

    @property
    def get_total(self):
        return self.product.price_current * self.quantity

    def __str__(self):
        return str(self.product.name)


