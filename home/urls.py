from django.urls import path
from home import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("buckets/", views.BucketHomeView.as_view(), name="buckets"),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]
