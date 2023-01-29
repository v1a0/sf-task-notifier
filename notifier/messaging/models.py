from django.db import models
from django.utils.crypto import get_random_string
from django.db.models import Count

from addressee.models import Addressee


# Event

class MessagingEventType(models.IntegerChoices):
    REGULAR = (0, 'regular')
    ONCE = (1, 'once')


class MessagingEvent(models.Model):
    title = models.CharField(null=False, blank=False, max_length=512)
    type = models.IntegerField(null=False, choices=MessagingEventType.choices, default=MessagingEventType.ONCE)
    start_at = models.DateTimeField(null=True, blank=False)
    stop_at = models.DateTimeField(null=True, default=None)
    text = models.CharField(null=False, blank=False, max_length=512)
    is_active = models.BooleanField(null=False, default=True)

    default_title = "Рассылка"

    class Meta:
        indexes = [models.Index(fields=['start_at', 'stop_at'])]

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

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


# Messaging

class MessageStatus(models.IntegerChoices):
    SCHEDULED = (100, 'scheduled')
    DONE = (200, 'done')
    RESERVED = (300, 'processing')
    FAILED = (400, 'failed')
    UNKNOWN = (500, 'unknown')


class ScheduledMessage(models.Model):
    event = models.ForeignKey(MessagingEvent, on_delete=models.CASCADE, null=False, related_name='scheduled_messages')
    addressee = models.ForeignKey(Addressee, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(null=False, db_index=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    status = models.IntegerField(null=False, choices=MessageStatus.choices, default=MessageStatus.SCHEDULED)
