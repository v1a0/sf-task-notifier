from django.db import models

from users.models import User


# Event

class ScheduledEventType(models.IntegerChoices):
    REGULAR = (0, 'regular')
    ONCE = (1, 'once')


class ScheduledEvent(models.Model):
    title = models.CharField(null=False, blank=False, max_length=512)
    type = models.IntegerField(null=False, choices=ScheduledEventType.choices, default=ScheduledEventType.ONCE)
    date = models.DateField(null=True, blank=False)
    time = models.TimeField(null=False, blank=False)
    is_active = models.BooleanField(null=False, default=True)


# Messaging

class MessagingStatus(models.IntegerChoices):
    UNKNOWN = (100, 'unknown')
    DONE = (200, 'done')
    RESERVED = (300, 'reserved')
    FAILED = (400, 'failed')


class MessagingSchedule(models.Model):
    event = models.ForeignKey(ScheduledEvent, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(null=False, db_index=True)


class MessagingScheduleLog(models.Model):
    schedule = models.ForeignKey(MessagingSchedule, on_delete=models.CASCADE, db_index=True)
    status = models.IntegerField(null=False, choices=MessagingStatus.choices, default=MessagingStatus.UNKNOWN)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, blank=False, auto_now=True)
