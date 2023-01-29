from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from misc.messages import MSG


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

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.operator_code = int(str(self.phone_number)[1:4])
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
