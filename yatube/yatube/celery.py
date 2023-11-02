import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatube.settings')
app = Celery('yatube')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'send_new_posts': {
        'task': 'newsletter.tasks.send_new_posts',
        'schedule': crontab(minute='*/1')
    }
}
