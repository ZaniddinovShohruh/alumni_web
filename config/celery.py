import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-students-info': {
        'task': 'alumni.tasks.check_and_notify_debt_students',
        'schedule': crontab(minute='*/1'),  # Har oyning har kuni
    },
}
