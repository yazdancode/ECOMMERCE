from django.urls import path

from accounts import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("verify/", views.VerifyCodeView.as_view(), name="verify_code"),
]
