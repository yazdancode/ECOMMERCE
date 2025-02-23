from datetime import timedelta

import django_jalali.db.models as jmodels
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.timezone import now

from accounts.managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name="آدرس ایمیل")
    phone_number = models.CharField(
        max_length=11, unique=True, verbose_name="شماره تلفن"
    )
    fullname = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_admin = models.BooleanField(default=False, verbose_name="مدیر")
    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "fullname"]

    def __str__(self):
        return self.phone_number

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


def default_expire_time():
    return now() + timedelta(minutes=5)


class OtpCode(models.Model):
    phone = models.CharField(max_length=11, verbose_name="شماره تلفن", unique=True)
    code = models.PositiveIntegerField(verbose_name="کد اعتبار سنجی")
    created_at = jmodels.jDateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد (شمسی)"
    )
    expire_at = models.DateTimeField(
        verbose_name="تاریخ انقضا", default=default_expire_time
    )
    is_used = models.BooleanField(default=False, verbose_name="استفاده شده؟")
    attempts = models.PositiveSmallIntegerField(default=0, verbose_name="تعداد تلاش‌ها")
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, verbose_name="آدرس IP کاربر"
    )
    device_info = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="مشخصات دستگاه"
    )

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = "کد اعتبار سنجی"
        verbose_name_plural = "کدهای اعتبار سنجی"
