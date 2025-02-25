from django.urls import path, include
from home import views

app_name = "home"

bucket_urls = [
    path("", views.BucketHomeView.as_view(), name="buckets"),
    path("delete/", views.DeleteBucketHomeView.as_view(), name="delete_buckets"),
    path("download/", views.DownloadBucketHomeView.as_view(), name="download_buckets"),
    path("upload/", views.UploadBucketHomeView.as_view(), name="upload_buckets"),
]

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("buckets/", include(bucket_urls)),  # مسیرهای مربوط به bucketها
    path("product/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),  # مسیر محصولات
]
