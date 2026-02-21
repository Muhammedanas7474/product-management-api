import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("product_management")

# Load settings from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed apps
app.autodiscover_tasks()
