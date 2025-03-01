from home.models import Product

CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = {}
            self.session[CART_SESSION_ID] = cart  # مقداردهی اولیه
        self.cart = cart

    def __iter__(self):
        """تبدیل کلیدهای سبد خرید به محصولات دیتابیس و محاسبه قیمت کل"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product  # محصول را اضافه می‌کنیم

        for item in cart.values():
            item["quantity"] = int(item["quantity"])  # تبدیل به عدد صحیح
            item["price"] = float(item["price"])  # تبدیل به عدد اعشاری
            item["total_price"] = item["price"] * item["quantity"]  # محاسبه قیمت کل
            yield item

    def add(self, product, quantity=1):
        """افزودن محصول به سبد خرید"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),  # تبدیل به `str` برای جلوگیری از JSON خطا
            }
        self.cart[product_id]["quantity"] += max(int(quantity), 1)
        self.save()

    def remove(self, product):
        """حذف محصول از سبد خرید"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """محاسبه مجموع قیمت کل محصولات در سبد خرید"""
        return sum(
            float(item["price"]) * int(item["quantity"]) for item in self.cart.values()
        )

    def clear(self):
        """حذف تمامی محصولات از سبد خرید"""
        self.session[CART_SESSION_ID] = {}
        self.save()

    def save(self):
        """ذخیره تغییرات در سبد خرید"""
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True  # ذخیره‌ی تغییرات در session
