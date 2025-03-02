from django.contrib import admin

from .models import Coupon, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "paid", "created", "updated", "get_total_price")
    search_fields = ("user__username", "id")
    list_filter = ("paid", "created")
    inlines = [OrderItemInline]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "get_cost")
    search_fields = ("order__id", "product__name")


admin.site.register(Coupon)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
