from django.db import models
from django.urls import reverse


class CategoryManager(models.Manager):
    def main_categories(self):
        """دریافت دسته‌بندی‌های اصلی (بدون والد)"""
        return self.filter(sub_category__isnull=True)

    def sub_categories(self):
        """دریافت دسته‌بندی‌های فرعی (دارای والد)"""
        return self.filter(sub_category__isnull=False)


class Category(models.Model):
    sub_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sub_categories",
        verbose_name="دسته‌بندی مادر",
    )
    name = models.CharField(max_length=255, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="نامک")

    objects = CategoryManager()

    def __str__(self):
        if self.sub_category:
            return f"{self.sub_category} > {self.name}"
        return self.name

    @property
    def is_sub_category(self):
        """بررسی می‌کند که آیا این دسته‌بندی زیرمجموعه‌ای دارد یا نه"""
        return self.sub_category is not None

    def get_absolute_url(self):
        """ایجاد لینک برای هر دسته‌بندی"""
        return reverse("home:category", args=[self.slug])

    class Meta:
        ordering = ("name",)
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام محصول")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="نامک")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی') 
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    image = models.ImageField(
        blank=True, null=True, upload_to="products/", verbose_name="تصویر"
    )
    category = models.ManyToManyField(
        Category,
        related_name="product_set",
        verbose_name="دسته‌بندی‌ها",
    )
    available = models.BooleanField(default=True, verbose_name="موجود")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="به‌روز شده در")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ایجاد لینک برای هر محصول"""
        return reverse("shop:product_detail", args=[self.slug])

    class Meta:
        ordering = ("name",)
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
