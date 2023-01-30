from messaging.models import ActiveMessages, MessageStatus, ScheduledMessage, MessageText
from notifier.celery import app
from messaging.fbrq import FbRQ
from rest_framework.status import HTTP_200_OK
from django.conf import settings


@app.task(bind=True)
def messages_sending(self):
    task_id = self.request.id
    data = ActiveMessages.get_and_reserve(task_id=task_id)
    service = FbRQ(token=settings.FBRQ_TOKEN)
    sending_ok_msgs = {}
    sending_failed_msg_ids = []

    for instance in data:
        response = service.send_message(instance.message_id, instance.phone_number, instance.text_value)

        if response == HTTP_200_OK:
            sending_ok_msgs[(instance.event_id, instance.text_id)] = \
                sending_ok_msgs.get((instance.event_id, instance.text_id), list()) + [instance.message_id]
        else:
            sending_failed_msg_ids.append(instance.message_id)

    for (event_id, message_text_id), ok_messages_ids in sending_ok_msgs.items():
        ScheduledMessage.objects.filter(id__in=ok_messages_ids).update(
            status=MessageStatus.SUCCESS,
            sent_with_text=MessageText.objects.filter(id=message_text_id).first()
        )

    ScheduledMessage.objects.filter(id__in=sending_failed_msg_ids).update(
        status=MessageStatus.FAILED,
    )

    return {
        'success': str(sending_ok_msgs),
        'filed': str(sending_failed_msg_ids)
    }

