from django.db import models
from django.core.validators import RegexValidator


class UserTag(models.Model):
    name = models.CharField(null=True, default=None, blank=False, max_length=128)
    title = models.CharField(null=False, blank=False, max_length=255)


class User(models.Model):

    first_name = models.CharField(null=True, max_length=255, default=None)
    last_name = models.CharField(null=True, max_length=255, default=None)
    middle_name = models.CharField(null=True, max_length=255, default=None)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Incorrect phone format. Example: '+999999999'")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    tags = models.ManyToManyField(UserTag, related_name='users')
