from django.contrib.auth import get_user_model
from django.db import models

from home.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="کاربر",
    )
    paid = models.BooleanField(default=False, verbose_name="پرداخت")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    def __str__(self):
        return f"سفارش {self.id} - کاربر: {self.user}"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ["paid", "-updated"]


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="مورد سفارش"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="محصول",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} در سفارش {self.order.id}"

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = "مورد سفارش"
        verbose_name_plural = "موارد سفارش"
