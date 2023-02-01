import logging
from datetime import timedelta
from rest_framework.status import HTTP_200_OK

from django.conf import settings
from django.utils.timezone import now
from django.core.mail import send_mail
from django.template.loader import render_to_string

from notifier.celery import app
from messaging.fbrq import FbRQ
from messaging.models import ActiveMessages, MessageStatus, ScheduledMessage, MessageText, MessagingEvent
from messaging.serializers import MessagingEventRetrieveSerializer


logger = logging.getLogger(__name__)


@app.task(bind=True)
def messages_sending(self):
    task_id = self.request.id
    data = ActiveMessages.get_and_reserve(task_id=task_id, limit=settings.CRON['messages-sending']['limit'])
    service = FbRQ(token=settings.FBRQ_API_TOKEN)

    sending_ok_msgs = {}            # message sent well
    sending_failed_msgs_ids = []    # not ok response from FbRQ API
    sending_canceled_msgs_ids = []  # sending is outdated

    for instance in data:
        logger.warning(f"Processing messaging event: {instance.event_id=}")

        if now() < instance.stop_at:
            response = service.send_message(instance.message_id, instance.phone_number, instance.text_value)
        else:
            sending_canceled_msgs_ids.append(instance.message_id)
            logger.warning(
                f"Sending time for message is outdated: {instance.stop_at}, {instance.message_id=}, {instance.event_id=}"
            )
            continue

        if response == HTTP_200_OK:
            sending_ok_msgs[(instance.event_id, instance.text_id)] = \
                sending_ok_msgs.get((instance.event_id, instance.text_id), list()) + [instance.message_id]
            logger.info(f"Message sending success: {response=}, {instance.message_id=}, {instance.event_id=}")

        else:
            logger.warning(f"Message sending failed: {response=}, {instance.message_id=}, {instance.event_id=}")
            sending_failed_msgs_ids.append(instance.message_id)

    for (event_id, message_text_id), ok_messages_ids in sending_ok_msgs.items():
        ScheduledMessage.objects.filter(id__in=ok_messages_ids).update(
            status=MessageStatus.SUCCESS,
            sent_with_text=MessageText.objects.filter(id=message_text_id).first(),
            updated_at=now()
        )

    if sending_failed_msgs_ids:
        ScheduledMessage.objects.filter(id__in=sending_failed_msgs_ids).update(
            status=MessageStatus.FAILED,
            updated_at=now()
        )

    if sending_canceled_msgs_ids:
        ScheduledMessage.objects.filter(id__in=sending_canceled_msgs_ids).update(
            status=MessageStatus.SCHEDULED,
            updated_at=now()
        )

    return {
        'success': str(sending_ok_msgs),
        'filed': str(sending_failed_msgs_ids),
        'canceled': str(sending_canceled_msgs_ids)
    }


@app.task(bind=True)
def daily_statistic_emailing(self):
    email_from = settings.EMAIL_HOST_USER
    email_to = settings.EMAIL_TO

    today = now().date()
    day_ago = today - timedelta(days=1)
    two_days_ago = day_ago - timedelta(days=1)

    messages = ScheduledMessage.objects.filter(updated_at__gt=two_days_ago, updated_at__lt=today)
    events_list = messages.values('event_id').distinct()
    data = MessagingEventRetrieveSerializer(MessagingEvent.objects.filter(id__in=events_list), many=True).data

    subject = f'Ежедневный отчет | {day_ago.isoformat()}'
    message = render_to_string('email_template.html', {'events': data, 'now': day_ago.isoformat()})

    return send_mail(subject, message, email_from, email_to, html_message=message)
