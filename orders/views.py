from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from home.models import Product
from orders.cart import Cart
from orders.forms import CartAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order, OrderItem


class CartView(View):
    """
    نمایش سبد خرید برای کاربر
    """
    def get(self, request):
        cart = Cart(request)
        return render(request, "orders/cart.html", {"cart": cart})


class CartAddView(View):
    """افزودن محصول به سبد خرید"""
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            quantity = int(cd["quantity"])  # اطمینان از تبدیل به عدد صحیح
            
            if quantity < 1:
                messages.error(request, "تعداد محصول باید حداقل ۱ باشد.")
            elif product.stock < quantity:  # فرض بر این که محصول فیلد `stock` دارد
                messages.error(request, "موجودی محصول کافی نیست.")
            else:
                cart.add(product=product, quantity=quantity)
                messages.success(request, f"محصول {product.name} به سبد خرید اضافه شد.")

        next_url = request.GET.get("next") or reverse("orders:cart")
        return redirect(next_url)


class CartRemoveView(View):
    """
    حذف محصول از سبد خرید
    """
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        if str(product.id) not in cart.cart:  # بررسی موجودیت در سبد خرید
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
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(request, 'orders/order.html', {'order': order})
        


class OrderCreateView(LoginRequiredMixin, View):
    """
    ایجاد سفارش جدید و انتقال داده‌های سبد خرید به سفارش
    """
    def get(self, request):
        cart = Cart(request=request)

        if len(cart) == 0:
            messages.error(request, "سبد خرید شما خالی است.")
            return redirect("orders:cart")

        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order, 
                product=item['product'], 
                price=item['price'], 
                quantity=item['quantity']
            )
        cart.clear()
        messages.success(request, "سفارش شما با موفقیت ثبت شد.")
        return redirect('orders:order_detail', order_id=order.id)
