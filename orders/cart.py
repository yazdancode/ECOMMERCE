from decimal import Decimal

from home.models import Product

CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        """مقداردهی اولیه سبد خرید"""
        self.session = request.session
        cart = self.session.get(
            CART_SESSION_ID, {}
        ).copy()  # کپی برای جلوگیری از تغییر در session
        self.cart = cart

    def __iter__(self):
        """تولید مقادیر سبد خرید شامل محصولات از دیتابیس و قیمت کل"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_copy = self.cart.copy()  # ایجاد یک کپی برای جلوگیری از تغییرات ناخواسته

        for product in products:
            cart_copy[str(product.id)]["product"] = product

        for item in cart_copy.values():
            item["quantity"] = int(item["quantity"])
            item["price"] = Decimal(
                item["price"]
            )  # تبدیل مقدار به Decimal برای دقت بیشتر
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """تعداد کل آیتم‌های درون سبد خرید"""
        return sum(int(item["quantity"]) for item in self.cart.values())

    def add(self, product, quantity=1):
        """افزودن محصول به سبد خرید"""
        quantity = max(int(quantity), 1)  # اطمینان از معتبر بودن مقدار quantity
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(
                    product.price
                ),  # ذخیره قیمت به صورت string برای جلوگیری از مشکلات JSON
            }
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product):
        """حذف یک محصول از سبد خرید"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """محاسبه مجموع قیمت کل محصولات در سبد خرید"""
        return sum(
            Decimal(item["price"]) * int(item["quantity"])
            for item in self.cart.values()
        )

    def clear(self):
        """حذف تمامی محصولات از سبد خرید"""
        self.session[CART_SESSION_ID] = {}
        self.session.modified = True

    def save(self):
        """ذخیره تغییرات در سبد خرید"""
        cart_copy = {
            product_id: {
                "quantity": item["quantity"],
                "price": str(
                    item["price"]
                ),  # تبدیل Decimal به str برای جلوگیری از خطای JSON
            }
            for product_id, item in self.cart.items()
        }

        self.session[CART_SESSION_ID] = cart_copy
        self.session.modified = True
