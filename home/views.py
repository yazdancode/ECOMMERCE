from django.shortcuts import render
from django.views import View
from home.models import Product


class HomeView(View):
    @staticmethod
    def get(request):
        products = Product.objects.filter(available=True)
        return render(request, "home/home.html", {'products': products})
    



