from datetime import timedelta

import pytz
from celery import shared_task
from django.utils import timezone

from accounts.models import OtpCode


@shared_task
def remove_expired_otp_codes():
    tehran_tz = pytz.timezone("Asia/Tehran")
    expired_time = timezone.now().astimezone(tehran_tz) - timedelta(minutes=2)
    OtpCode.objects.filter(created_at__lt=expired_time).delete()
