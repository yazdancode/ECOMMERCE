from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from home.models import Product
from orders.cart import Cart
from orders.forms import CartAddForm


class CartView(View):
    """
    نمایش سبد خرید برای کاربر
    """

    @staticmethod
    def get(request):
        cart = Cart(request)
        return render(request, "orders/cart.html", {"cart": cart})


class CartAddView(View):
    """افزودن محصول به سبد خرید"""

    @staticmethod
    def post(request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            quantity = int(cd["quantity"])  # اطمینان از تبدیل به عدد صحیح

            if quantity < 1:
                messages.error(request, "تعداد محصول باید حداقل ۱ باشد.")
            else:
                cart.add(product=product, quantity=quantity)
                messages.success(request, f"محصول {product.name} به سبد خرید اضافه شد.")

        next_url = request.GET.get("next") or reverse("orders:cart")
        return redirect(next_url)


class CartRemoveView(View):
    """
    حذف محصول از سبد خرید
    """

    @staticmethod
    def get(request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        cart.remove(product)
        messages.success(request, f"محصول {product.name} از سبد خرید حذف شد.")

        next_url = request.GET.get("next") or reverse("orders:cart")
        return redirect(next_url)
