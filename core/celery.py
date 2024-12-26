import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.develop')
apps = Celery("core", broker=settings.CELERY_BROKER_URL)
apps.config_from_object("django.conf:settings", namespace="CELERY")

apps.autodiscover_tasks()


@apps.task
def add_number():
    return 0
