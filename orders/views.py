import datetime

import requests
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from home.models import Product
from orders.cart import Cart
from orders.forms import CartAddForm, CouponApplyForm
from orders.models import Coupon, Order, OrderItem


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
            quantity = int(cd["quantity"])

            if quantity < 1:
                messages.error(request, "تعداد محصول باید حداقل ۱ باشد.")
            elif product.stock < quantity:
                messages.error(request, "موجودی محصول کافی نیست.")
            else:
                cart.add(product=product, quantity=quantity)
                product.reduce_stock(quantity)
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

        if str(product.id) not in cart.cart:
            messages.error(request, f"محصول {product.name} در سبد خرید شما وجود ندارد.")
        else:
            cart.remove(product)
            messages.success(request, f"محصول {product.name} از سبد خرید حذف شد.")

        next_url = request.GET.get("next") or reverse("orders:cart")
        return redirect(next_url)


class OrderDetailView(LoginRequiredMixin, View):
    """
    نمایش جزئیات سفارش فقط برای کاربر لاگین شده
    """

    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(
            request,
            "orders/order.html",
            {"order": order, "form_class": self.form_class},
        )


class OrderCreateView(LoginRequiredMixin, View):
    """
    ایجاد سفارش جدید و انتقال داده‌های سبد خرید به سفارش
    """

    @staticmethod
    def get(request):
        cart = Cart(request=request)

        if len(cart) == 0:
            messages.error(request, "سبد خرید شما خالی است.")
            return redirect("orders:cart")

        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                price=item["price"],
                quantity=item["quantity"],
            )
        cart.clear()
        messages.success(request, "سفارش شما با موفقیت ثبت شد.")
        return redirect("orders:order_detail", order_id=order.id)


class OrderPayView(LoginRequiredMixin, View):
    """
    پرداخت سفارش
    """

    @staticmethod
    def get(request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            request.session["order_pay"] = {"order_id": order_id}
        except Order.DoesNotExist:
            return HttpResponse("Order not found", status=404)

        req_data = {
            "merchant_id": "XXXXXXXX",
            "amount": order.get_total_price(),
            "callback_url": request.build_absolute_uri(reverse("orders:pay_callback")),
            "description": f"پرداخت سفارش شماره {order.id}",
            "metadata": {
                "order_id": order.id,
                "mobile": request.user.phone_number,
                "email": request.user.email,
            },
        }

        req_headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                "https://api.zarinpal.com/pg/v4/payment/request",
                json=req_data,
                headers=req_headers,
            )
            response.raise_for_status()

            authority = response.json().get("data", {}).get("authority")

            if not authority:
                return HttpResponse("Authorization failed", status=400)

        except requests.RequestException as e:
            return HttpResponse(
                f"Error while processing payment request: {str(e)}", status=500
            )

        return render(
            request, "orders/pay.html", {"order": order, "req_data": req_data}
        )


# TODO: code hanoz tamoom nashode part two ham dareh
class OrderVerifyView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        order_id = request.session.get("order_pay", {}).get("order_id")
        if not order_id:
            return HttpResponse("Order ID not found", status=400)
        try:
            order = Order.objects.get(id=int(order_id))
        except Order.DoesNotExist:
            return HttpResponse("Order not found", status=404)
        t_status = request.GET.get("Status")
        t_authority = request.GET.get("Authority")
        if t_status == "OK":
            req_data = {
                "merchant_id": "XXXXXXXX",
                "order_id": order_id,
                "status": t_status,
                "authority": t_authority,
            }
            order.payment_status = "Verified"
            order.save()
            return HttpResponse("Payment successful", status=200)
        else:
            return HttpResponse("Payment failed", status=400)


class OrderApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            try:
                copun = Coupon.objects.get(
                    code__exact=code,
                    valid_from__lte=now,
                    valid_to__gte=now,
                    active=True,
                )
            except Coupon.DoesNotExist:
                messages.error(request, "this coupon does not exist", "danger")
                return redirect("orders:order_detail", order_id)
            order = Order.objects.get(id=order_id)
            order.discount = copun.discount
            order.save()
        return redirect("orders:order_detail", order_id)
