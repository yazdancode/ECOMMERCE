from django.urls import path

from accounts import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("verify/", views.VerifyCodeView.as_view(), name="verify_code"),
]
