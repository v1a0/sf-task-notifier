if __name__ == '__main__':
    from gevent import monkey as curious_george
    curious_george.patch_all(thread=False, select=False)

import os
from celery import Celery
from celery.schedules import crontab

# import bugfix
from django.conf import settings


# Getting django env settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifier.settings')

app = Celery('notifier')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'ac-data-scrapping': {
#         'task': 'activecollab.tasks.scrap_ac_data_upw',
#         'schedule': crontab(
#             day_of_week=settings.SCHEDULER_TRIGGER_TIME['ac_data_scrapping']['day_of_week'],
#             hour=settings.SCHEDULER_TRIGGER_TIME['ac_data_scrapping']['hour'],
#             minute=settings.SCHEDULER_TRIGGER_TIME['ac_data_scrapping']['minute'],
#         ),
#     },
#     'telegram-bot-daily-notification-1': {
#         'task': 'telegram_bot.tasks.send_daily_notifications_1',
#         'schedule': crontab(
#             day_of_week=settings.SCHEDULER_TRIGGER_TIME['telegram-bot-daily-notification-1']['day_of_week'],
#             hour=settings.SCHEDULER_TRIGGER_TIME['telegram-bot-daily-notification-1']['hour'],
#             minute=settings.SCHEDULER_TRIGGER_TIME['telegram-bot-daily-notification-1']['minute'],
#         ),
#     },
#     'telegram-bot-daily-notification-2': {
#         'task': 'telegram_bot.tasks.send_daily_notifications_2',
#         'schedule': crontab(
#             day_of_week=settings.SCHEDULER_TRIGGER_TIME['telegram-bot-daily-notification-2']['day_of_week'],
#             hour=settings.SCHEDULER_TRIGGER_TIME['telegram-bot-daily-notification-2']['hour'],
#             minute=settings.SCHEDULER_TRIGGER_TIME['telegram-bot-daily-notification-2']['minute'],
#         ),
#         # 'schedule': timedelta(seconds=5),   # sun every 5 sec //requirement: from datetime import timedelta
#     },
#     'estimates-garbage-files-collector': {
#         'task': 'estimates.tasks.garbage_files_collector',
#         'schedule': crontab(
#             day_of_week=settings.SCHEDULER_TRIGGER_TIME['estimates-garbage-files-collector']['day_of_week'],
#             hour=settings.SCHEDULER_TRIGGER_TIME['estimates-garbage-files-collector']['hour'],
#             minute=settings.SCHEDULER_TRIGGER_TIME['estimates-garbage-files-collector']['minute'],
#         ),
#         # 'schedule': timedelta(seconds=5),   # sun every 5 sec //requirement: from datetime import timedelta
#     },
# }
app.conf.timezone = settings.TIME_ZONE
