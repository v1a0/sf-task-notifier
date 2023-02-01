import logging.config

from django.utils.timezone import now
from django.db import models, transaction
from django.utils.crypto import get_random_string
from django.db.models import Count

from addressee.models import Addressee


logger = logging.getLogger(__name__)


# Event

class MessageText(models.Model):
    text = models.CharField(null=False, blank=False, max_length=512)

    def delete(self, using=None, keep_parents=False):
        pass

    def __str__(self):
        return self.text


class MessagingEvent(models.Model):
    title = models.CharField(null=False, blank=False, max_length=512)
    start_at = models.DateTimeField(null=True, blank=False)
    stop_at = models.DateTimeField(null=True, default=None)
    text_col = models.ForeignKey(MessageText, null=True, on_delete=models.SET_NULL, db_column="text_id")
    settings = models.JSONField(null=False, default=dict)

    # relations
    scheduled_messages: None    # ScheduledMessage

    default_title = "Рассылка"

    class Meta:
        indexes = [models.Index(fields=['start_at', 'stop_at'])]

    def __str__(self):
        return f"<MessagingEvent: " \
               f"{self.id=}, " \
               f"{self.title=}, " \
               f"{self.start_at=}, " \
               f"{self.stop_at=}, " \
               f"{self.text_col=}, " \
               f"{self.settings=}" \
               f">"

    @property
    def is_active(self):
        if not self.stop_at:
            return False
        return now() > self.stop_at

    @property
    def text(self) -> str:
        return str(self.text_col)

    @text.setter
    def text(self, value):
        msg_txt = MessageText.objects.filter(text=value)

        if not msg_txt.exists():
            msg_txt = MessageText(text=value)
            msg_txt.save()
        else:
            msg_txt = msg_txt.first()

        self.text_col = msg_txt

    def count_scheduled_messages(self):
        return self.scheduled_messages.all().count()

    def get_statistic(self):
        code_and_total = self.scheduled_messages.all().values('status').annotate(total=Count('status')).order_by('status').values_list('status', 'total')

        stat = {
            code: total
            for code, total in code_and_total
        }

        return {
            status_label: stat.get(status_value, 0)
            for status_value, status_label in MessageStatus.choices
        }

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.title:
            self.title = f"{self.default_title}_{get_random_string(16)}"
        self.created_at = now()

        logger.info(
            f"MessagingEvent updated: {self}"
            if self.id else
            f"MessagingEvent created: {self}"
        )

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def delete(self, using=None, keep_parents=False):
        logger.info(f"MessagingEvent deleted: {self}")
        return super().delete(using=using, keep_parents=keep_parents)


# Messaging

class MessageStatus(models.IntegerChoices):
    SCHEDULED = (100, 'scheduled')
    FAILED = (200, 'failed')
    PROCESSING = (300, 'processing')
    SUCCESS = (400, 'success')
    BLOCKED = (500, 'blocked')


class ScheduledMessage(models.Model):
    event = models.ForeignKey(MessagingEvent, on_delete=models.CASCADE, null=False, related_name='scheduled_messages')
    addressee = models.ForeignKey(Addressee, on_delete=models.CASCADE, null=False, related_name='scheduled_messages')
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    status = models.IntegerField(null=False, choices=MessageStatus.choices, default=MessageStatus.SCHEDULED)
    updated_by_task = models.UUIDField(null=True, blank=False, default=None)
    sent_with_text = models.ForeignKey(MessageText, null=True, default=None, on_delete=models.SET_NULL)


# # TODO: have no idea why this mixin doesn't work well
#
# class MessagesViewMixin(models.Model):
#     event = models.ForeignKey(MessagingEvent, on_delete=models.DO_NOTHING)
#     message = models.ForeignKey(ScheduledMessage, on_delete=models.DO_NOTHING)
#     addressee = models.ForeignKey(Addressee, on_delete=models.DO_NOTHING)
#
#     event_title = models.CharField(max_length=512)
#     stop_at = models.DateTimeField(null=True, default=None)
#     text = models.CharField(max_length=512)
#     status = models.IntegerField(null=False, choices=MessageStatus.choices, default=MessageStatus.SCHEDULED)
#     phone_number = models.BigIntegerField()
#
#     updated_by_task = models.UUIDField(null=True, default=None)
#
#     class Meta:
#         abstract = True


class ProcessingMessages(models.Model):
    event = models.ForeignKey(MessagingEvent, on_delete=models.DO_NOTHING, related_name='processing_messages')
    message = models.ForeignKey(ScheduledMessage, on_delete=models.DO_NOTHING, related_name='processing_messages')
    addressee = models.ForeignKey(Addressee, on_delete=models.DO_NOTHING, related_name='processing_messages')
    text = models.ForeignKey(MessageText, on_delete=models.DO_NOTHING)

    event_title = models.CharField(max_length=512)
    stop_at = models.DateTimeField(null=True, default=None)
    text_value = models.CharField(max_length=512)
    status = models.IntegerField(null=False, choices=MessageStatus.choices, default=MessageStatus.SCHEDULED)
    phone_number = models.BigIntegerField()

    updated_by_task = models.UUIDField(null=True, default=None)

    class Meta:
        abstract = False
        managed = False
        db_table = 'processing_messages'


class ActiveMessages(models.Model):
    event = models.ForeignKey(MessagingEvent, on_delete=models.DO_NOTHING, related_name='active_messages')
    message = models.ForeignKey(ScheduledMessage, on_delete=models.DO_NOTHING, related_name='active_messages')
    addressee = models.ForeignKey(Addressee, on_delete=models.DO_NOTHING, related_name='active_messages')
    text = models.ForeignKey(MessageText, on_delete=models.DO_NOTHING)

    event_title = models.CharField(max_length=512)
    stop_at = models.DateTimeField(null=True, default=None)
    text_value = models.CharField(max_length=512)
    status = models.IntegerField(null=False, choices=MessageStatus.choices, default=MessageStatus.SCHEDULED)
    phone_number = models.BigIntegerField()

    updated_by_task = models.UUIDField(null=True, default=None)

    class Meta:
        abstract = False
        managed = False
        db_table = 'active_messages'

    @classmethod
    def get_and_reserve(cls, task_id: str, limit: int = None):
        if limit is None:
            limit = -1

        with transaction.atomic():
            ScheduledMessage.objects.filter(
                id__in=cls.objects.all()[:limit].values('message_id')
            ).update(
                status=MessageStatus.PROCESSING,
                updated_by_task=task_id,
                updated_at=now()
            )

            return ProcessingMessages.objects.filter(
                status=MessageStatus.PROCESSING,
                updated_by_task=task_id,
            )

