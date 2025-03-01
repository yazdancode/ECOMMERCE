from django.urls import path

from . import views

app_name = "orders"
urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart"),
    path(
        "add_to_cart/<int:product_id>/", views.CartAddView.as_view(), name="add_to_cart"
    ),
    path(
        "cart/remove/<int:product_id>/",
        views.CartRemoveView.as_view(),
        name="cart_remove",
    ),
]
