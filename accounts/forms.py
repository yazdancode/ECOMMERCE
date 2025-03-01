import re

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator

from accounts.models import OtpCode, User


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
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "example@email.com"}
        ),
    )

    fullname = forms.CharField(
        label="نام و نام خانوادگی",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "مثال: علی رضایی"}
        ),
        validators=[
            RegexValidator(
                regex=r"^[\u0600-\u06FF\s]+$",
                message="نام و نام خانوادگی باید فقط شامل حروف فارسی باشد.",
            )
        ],
    )

    phone_number = forms.CharField(
        label="شماره تلفن همراه",
        max_length=11,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "مثال: 09*********"}
        ),
        validators=[
            RegexValidator(
                regex=r"^09\d{9}$",
                message="شماره تلفن همراه معتبر نیست (باید با 09 شروع شده و ۱۱ رقم باشد).",
            )
        ],
    )

    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "******"}
        ),
        validators=[
            RegexValidator(
                regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,12}$",
                message="رمز عبور باید بین ۶ تا ۱۲ کاراکتر و شامل حداقل یک حرف و یک عدد باشد.",
            )
        ],
    )

    password_confirmation = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "******"}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("این شماره تلفن همراه قبلاً ثبت شده است.")
        OtpCode.objects.filter(phone=phone_number).delete()
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("رمز عبور و تکرار آن یکسان نیستند.")

        return cleaned_data


class VerifyCodeForm(forms.Form):
    code = forms.CharField(
        label="کد تأیید",
        max_length=4,
        min_length=4,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "مثال: 1234"}
        ),
        validators=[
            RegexValidator(
                regex=r"^\d{4}$", message="کد تأیید باید دقیقاً ۴ رقم عددی باشد."
            )
        ],
    )

    def clean_code(self):
        code = self.cleaned_data["code"]
        if not code.isdigit():
            raise forms.ValidationError("کد تأیید باید فقط شامل اعداد باشد.")
        return code


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        label="شماره تلفن همراه",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "مثال: 09*********"}
        ),
        help_text="شماره تلفن باید ۱۱ رقمی و با 09 شروع شود.",
    )

    password = forms.CharField(
        max_length=8,
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "******"}
        ),
        validators=[
            RegexValidator(
                regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,8}$",
                message="رمز عبور باید بین ۶ تا ۸ کاراکتر و شامل حداقل یک حرف و یک عدد باشد.",
            )
        ],
        help_text="رمز عبور باید بین ۶ تا ۸ کاراکتر و شامل حداقل یک حرف و یک عدد باشد.",
    )

    password_confirmation = forms.CharField(
        max_length=8,
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "******"}
        ),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        phone_number = phone_number.replace(" ", "").replace(
            "-", ""
        )  # حذف فاصله و خط تیره

        if not re.fullmatch(r"09\d{9}", phone_number):
            raise forms.ValidationError("شماره تلفن همراه معتبر نیست.")

        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("رمز عبور و تکرار آن یکسان نیستند.")

        return cleaned_data
