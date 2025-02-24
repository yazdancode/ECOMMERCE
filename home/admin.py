from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")  # نمایش فیلدها در لیست
    prepopulated_fields = {"slug": ("name",)}  # ایجاد خودکار slug از نام
    search_fields = ("name",)  # امکان جستجو بر اساس نام


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "available")  # نمایش در لیست
    list_filter = ("category", "available")  # فیلتر بر اساس دسته‌بندی و موجودی
    search_fields = ("name", "description")  # جستجو در نام و توضیحات
    prepopulated_fields = {"slug": ("name",)}  # ایجاد خودکار slug از نام
    list_editable = ("price", "available")  # امکان ویرایش قیمت و موجودی از لیست
