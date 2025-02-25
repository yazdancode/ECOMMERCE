import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ecommerce.settings")

app = Celery("Ecommerce")

app.autodiscover_tasks()


app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = "rpc://"
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json", "pickle"]
app.conf.result_expires = timedelta(days=1)
app.conf.task_always_eager = False
app.conf.worker_prefetch_multiplier = 1
app.conf.timezone = "UTC"
app.conf.enable_utc = True
