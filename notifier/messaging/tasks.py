from rest_framework.status import HTTP_200_OK

from django.conf import settings
from django.utils.timezone import now

from notifier.celery import app
from messaging.fbrq import FbRQ
from messaging.models import ActiveMessages, MessageStatus, ScheduledMessage, MessageText


@app.task(bind=True)
def messages_sending(self):
    task_id = self.request.id
    data = ActiveMessages.get_and_reserve(task_id=task_id)
    service = FbRQ(token=settings.FBRQ_API_TOKEN)

    sending_ok_msgs = {}            # message sent well
    sending_failed_msgs_ids = []    # not ok response from FbRQ API
    sending_canceled_msgs_ids = []  # sending is outdated

    log = []

    for instance in data:
        if now() < instance.stop_at:
            response = service.send_message(instance.message_id, instance.phone_number, instance.text_value)
        else:
            sending_canceled_msgs_ids.append(instance.message_id)
            log.append([instance.message_id, 'outdated', instance.stop_at])
            continue

        if response == HTTP_200_OK:
            sending_ok_msgs[(instance.event_id, instance.text_id)] = \
                sending_ok_msgs.get((instance.event_id, instance.text_id), list()) + [instance.message_id]
        else:
            log.append([instance.message_id, 'api response', response])
            sending_failed_msgs_ids.append(instance.message_id)

    for (event_id, message_text_id), ok_messages_ids in sending_ok_msgs.items():
        ScheduledMessage.objects.filter(id__in=ok_messages_ids).update(
            status=MessageStatus.SUCCESS,
            sent_with_text=MessageText.objects.filter(id=message_text_id).first()
        )

    if sending_failed_msgs_ids:
        ScheduledMessage.objects.filter(id__in=sending_failed_msgs_ids).update(
            status=MessageStatus.FAILED,
        )

    if sending_canceled_msgs_ids:
        ScheduledMessage.objects.filter(id__in=sending_canceled_msgs_ids).update(
            status=MessageStatus.SCHEDULED,
        )

    return {
        'success': str(sending_ok_msgs),
        'filed': str(sending_failed_msgs_ids),
        'canceled': str(sending_canceled_msgs_ids),
        'log': str(log)
    }


@app.task(bind=True)
def messages_sending(self):
    from django.core.mail import send_mail

    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['54@mailforspam.com'],
        fail_silently=False,
    )
