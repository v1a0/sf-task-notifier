import logging.config

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from misc.messages import MSG
from misc.auto_log import log_save_update, log_delete


logger = logging.getLogger(__name__)


class AddresseeTag(models.Model):
    name = models.CharField(null=True, default=None, blank=False, max_length=128)
    title = models.CharField(null=False, blank=False, max_length=255)


class Addressee(models.Model):
    name = models.CharField(null=True, blank=False, max_length=255, default=None)
    phone_number = models.BigIntegerField(
        null=False, blank=False,
        validators=[MinValueValidator(70000000000), MaxValueValidator(79999999999)],
        error_messages=MSG.ERROR.PHONE,
        unique=True)
    operator_code = models.IntegerField(
        null=False, blank=False,
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    tags = models.ManyToManyField(AddresseeTag, related_name='addressee')

    def __str__(self):
        return f"<Addressee: " \
               f"{self.id=}, " \
               f"{self.name=}, " \
               f"{self.phone_number=}, " \
               f"{self.operator_code=}, " \
               f"{self.created_at=}, " \
               f"{self.updated_at=}" \
               f">"

    @log_save_update(logger.info)
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.operator_code = int(str(self.phone_number)[1:4])
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    @log_delete(logger.info)
    def delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)