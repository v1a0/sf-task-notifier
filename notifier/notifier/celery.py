# DON'T MOVE THIS CODE BLOCK (TOP)
if __name__ == '__main__':
    from gevent import monkey as curious_george
    curious_george.patch_all(thread=False, select=False)
# DON'T MOVE THIS CODE BLOCK (BOTTOM)

import os
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

from django.conf import settings


# Getting django env settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifier.settings')

app = Celery('notifier', task_always_eager=True)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'messages-sending': {
        'task': 'messaging.tasks.messages_sending',
        'schedule': timedelta(seconds=settings.CRON['messages-sending']['delay']),
    },
    'daily-statistic-emailing': {
        'task': 'messaging.tasks.daily_statistic_emailing',
        'schedule': crontab(
            hour=settings.CRON['daily-statistic-emailing']['hour'],
            minute=settings.CRON['daily-statistic-emailing']['minute'],
        ),
    },
}
app.conf.timezone = settings.TIME_ZONE
