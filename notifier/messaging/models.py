from django.db import models
from django.contrib.postgres.indexes import GinIndex

from addressee.models import Addressee


# Event

class ScheduledEventType(models.IntegerChoices):
    REGULAR = (0, 'regular')
    ONCE = (1, 'once')


class ScheduledEvent(models.Model):
    title = models.CharField(null=False, blank=False, max_length=512)
    type = models.IntegerField(null=False, choices=ScheduledEventType.choices, default=ScheduledEventType.ONCE)
    date = models.DateField(null=True, blank=False)
    time = models.TimeField(null=False, blank=False)
    stop_at = models.DateTimeField(null=True, default=None)
    text = models.CharField(null=False, blank=False, max_length=512)
    is_active = models.BooleanField(null=False, default=True)

    class Meta:
        indexes = [GinIndex(fields=['date', 'time']), GinIndex(fields=['stop_at'])]


# Messaging

class MessagingStatus(models.IntegerChoices):
    UNKNOWN = (100, 'unknown')
    DONE = (200, 'done')
    RESERVED = (300, 'reserved')
    FAILED = (400, 'failed')


class ScheduledMessage(models.Model):
    event = models.ForeignKey(ScheduledEvent, on_delete=models.CASCADE, null=False)
    addressee = models.ForeignKey(Addressee, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(null=False, db_index=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, blank=False, auto_now=True)
