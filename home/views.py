from django.shortcuts import render, get_object_or_404
from django.views import View
from home.models import Product


class HomeView(View):
    @staticmethod
    def get(request):
        products = Product.objects.filter(available=True)
        return render(request, "home/home.html", {"products": products})


class ProductDetailView(View):
    @staticmethod
    def get(request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, "home/detail.html", {"product": product})

