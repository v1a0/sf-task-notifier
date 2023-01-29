if __name__ == '__main__':
    from gevent import monkey as curious_george
    curious_george.patch_all(thread=False, select=False)

import os
from celery import Celery
from datetime import timedelta

# import bugfix
from django.conf import settings


# Getting django env settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifier.settings')

app = Celery('notifier')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'messages-sending': {
        'task': 'messaging.tasks.messages_sending',
        'schedule': timedelta(seconds=settings.MESSAGING_SENDING_CRON_DELAY),
    },
}
app.conf.timezone = settings.TIME_ZONE
