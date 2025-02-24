from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ("email", "phone_number", "fullname")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("رمز عبورها یکسان نیستند")
        return cd["password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='شما نمی توانید رمز عبور را با استفاده از آن تغییر دهید <a href="../password/">این فرم</a>'
    )

    class Meta:
        model = User
        fields = ("email", "phone_number", "fullname", "password", "last_login")

    def clean_password(self):
        return self.initial["password"]


class UserRegisterForm(forms.Form):
    email = forms.EmailField(label="ایمیل")
    fullname = forms.CharField(label="نام و نام خانوادگی")
    phone_number = forms.CharField(label="شماره تلفن همراه")
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput,
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلا ثبت شده است")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("این شماره تلفن همراه قبلا ثبت شده است")
        return phone_number


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(label="کد تایید")

    def clean_code(self):
        cd = self.cleaned_data
        code = str(cd["code"])
        if len(code) != 4:
            raise forms.ValidationError("کد تایید باید ۴ رقم باشد")
        return cd["code"]


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, label="شماره تلفن همراه")
    password = forms.CharField(
        max_length=8,
        label="رمز عبور",
        widget=forms.PasswordInput,
    )
