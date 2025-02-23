from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="نامک")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام محصول")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="نامک")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    image = models.ImageField(
        upload_to="products/%Y/%m/%d", blank=True, verbose_name="تصویر"
    )
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="دسته‌بندی",
    )
    available = models.BooleanField(default=True, verbose_name="موجود")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="به‌روز شده در")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
