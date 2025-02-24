from django.shortcuts import get_object_or_404, render
from django.views import View

from home.models import Product
from home.utils.tasks import all_bucket_objects_task


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


class BucketHomeView(View):
    template_name = "home/buckets.html"

    def get(self, request):
        objects = all_bucket_objects_task()
        return render(request, self.template_name, {"objects": objects})
