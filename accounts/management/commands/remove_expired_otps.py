from datetime import datetime, timedelta

import pytz
from django.core.management.base import BaseCommand

from accounts.models import OtpCode


class Command(BaseCommand):
    help = "کدهای OTP منقضی شده را حذف کنید"

    def handle(self, *args, **options):
        expired_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) - timedelta(
            minutes=2
        )
        OtpCode.objects.filter(created_at__lt=expired_time).delete()
        self.stdout.write(self.style.SUCCESS("کدهای OTP منقضی شده حذف شدند"))
