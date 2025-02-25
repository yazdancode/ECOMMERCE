import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.views import View

from accounts.forms import LoginForm, UserRegisterForm, VerifyCodeForm
from accounts.models import OtpCode, User
from accounts.utils.utils import send_top_code


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = "accounts/register.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = random.randint(1000, 9999)
            send_top_code(form.cleaned_data["phone_number"], code)
            OtpCode.objects.create(
                phone=form.cleaned_data["phone_number"],
                code=code,
            )
            request.session["user_registration_info"] = {
                "phone_number": form.cleaned_data["phone_number"],
                "email": form.cleaned_data["email"],
                "fullname": form.cleaned_data["fullname"],
                "password": form.cleaned_data["password"],
            }
            messages.success(request, "کد تایید به شماره تلفن همراه شما ارسال شد")
            return redirect("accounts:verify_code")
        return render(request, self.template_name, {"form": form})


class VerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = "accounts/verify.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        user_session = request.session.get("user_registration_info")
        if not user_session:
            messages.error(request, "اطلاعات ثبت‌نام یافت نشد")
            return redirect("register")

        try:
            code_instance = OtpCode.objects.get(phone=user_session["phone_number"])
        except OtpCode.DoesNotExist:
            messages.error(request, "کد وارد شده نامعتبر است")
            return redirect("verify_code")

        if now() > code_instance.created_at + timedelta(minutes=2):
            code_instance.delete()
            messages.error(request, "کد منقضی شده است، لطفاً دوباره درخواست ارسال کنید")
            return redirect("accounts:verify_code")

        form = self.form_class(request.POST)
        if form.is_valid():
            if form.cleaned_data["code"] == code_instance.code:
                User.objects.create_user(
                    phone_number=user_session["phone_number"],
                    email=user_session["email"],
                    fullname=user_session["fullname"],
                    password=user_session["password"],
                )
                OtpCode.objects.filter(phone=user_session["phone_number"]).delete()
                del request.session["user_registration_info"]
                messages.success(request, "ثبت نام با موفقیت انجام شد")
                return redirect("home")

            messages.error(request, "کد وارد شده نامعتبر است")
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            user = User.objects.get(phone_number=phone_number)
            login(request, user)
            messages.success(request, "ورود با موفقیت انجام شد", "info")
            return redirect("home:home")
        messages.error(request, "کاربری با این شماره تلفن یافت نشد", "warning")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect("home:home")

    @staticmethod
    def post(request):
        logout(request)
        messages.success(request, "شما با موفقیت خارج شدید")
        return redirect("home:home")
