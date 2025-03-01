from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sub_category", "is_sub_category", "slug")
    list_filter = ("sub_category",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "available", "created_at", "updated_at")
    list_filter = ("available", "category")
    search_fields = ("name", "description", "slug")
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created_at"
    raw_id_fields = ("category",)
