from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from home.models import Product
from home.tasks.tasks import (all_bucket_objects_task,
                              delete_bucket_objects_task,
                              download_objects_task, upload_objects_task)
from home.utils.utils import IsAdminUserMixin


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


class BucketHomeView(IsAdminUserMixin, View):
    template_name = "home/bucket.html"

    def get(self, request):
        objects = all_bucket_objects_task()
        return render(request, self.template_name, {"objects": objects})


class DeleteBucketHomeView(IsAdminUserMixin, View):
    @staticmethod
    def get(request):
        keys = request.GET.get("keys")
        if keys:
            delete_bucket_objects_task.delay(keys)
            messages.success(request, "شیء شما به زودی حذف می‌شود.", "info")
        return redirect("buckets")


class DownloadBucketHomeView(IsAdminUserMixin, View):
    @staticmethod
    def get(request):
        keys = request.GET.get("keys")
        if keys:
            download_objects_task.delay(keys)
            messages.success(request, "بارگیری شما به زودی شروع می شود.", "info")
        return redirect("buckets")


class UploadBucketHomeView(IsAdminUserMixin, View):
    @staticmethod
    def get(request):
        key = request.GET.get("key")
        file_path = request.GET.get("file_path")
        if key and file_path:
            upload_objects_task.delay(file_path, key)
            messages.success(request, "بارگذاری شما به زودی آغاز می شود.", "info")
        return redirect("buckets")
