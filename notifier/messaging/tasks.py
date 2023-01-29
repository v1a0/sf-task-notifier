from celery import shared_task
from django.core.cache import cache
from messaging.models import ActiveMessages, MessageStatus, ScheduledMessage
from notifier.celery import app
from messaging.fbrq import FbRQ
from rest_framework.status import HTTP_200_OK
from django.conf import settings


@app.task(bind=True)
def do_job(self):
    task_id = self.request.id
    data = ActiveMessages.get_and_reserve(2, task_id)
    service = FbRQ(token=settings.FBRQ_TOKEN)
    sending_ok_msg_ids = []
    sending_failed_msg_ids = []

    for instance in data:
        result = service.send_message(instance.message_id, instance.phone_number, instance.text)

        if result is HTTP_200_OK:
            sending_ok_msg_ids.append(instance.message_id)
        else:
            sending_failed_msg_ids.append(instance.message_id)

    ScheduledMessage.objects.filter(id__in=sending_ok_msg_ids).update(status=MessageStatus.SUCCESS)
    ScheduledMessage.objects.filter(id__in=sending_failed_msg_ids).update(status=MessageStatus.FAILED)

    return 0

