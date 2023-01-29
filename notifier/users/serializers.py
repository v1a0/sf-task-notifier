import copy

from django.db import transaction
import django.core.exceptions as django_exceptions
# from drf_yasg.utils import swagger_serializer_method

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from users.models import User, UserTag
import misc.regexes as reg


class UserCreateSerializer(serializers.Serializer):

    first_name = serializers.CharField(required=False, max_length=255, default=None)
    last_name = serializers.CharField(required=False, max_length=255, default=None)
    middle_name = serializers.CharField(required=False, max_length=255, default=None)
    phone_number = serializers.RegexField(
        required=True, regex=reg.PHONE_NUMBER,
        validators=[UniqueValidator(queryset=User.objects.all().values('phone_number'))]
    )

    tags = serializers.ListField(
        required=False,
        child=serializers.CharField(),
        allow_empty=True,
        default=list()
    )

    def create(self, validated_data):
        tags_names = validated_data.pop('tags')
        user = User(**validated_data)
        tags_to_create = list()

        for tag_title in tags_names:
            if not UserTag.objects.filter(title=tag_title).exists():
                tags_to_create.append(UserTag(name=None, title=tag_title))

        with transaction.atomic():
            user.save()

            if tags_to_create:
                UserTag.objects.bulk_create(tags_to_create)
            if tags_names:
                user.tags.add(*UserTag.objects.filter(title__in=tags_names).values_list('id', flat=True))
                user.save()

        return user

    def update(self, instance, validated_data):
        pass


class UserTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTag
        fields = [
            "id",
            "name",
            "title"
        ]
        depth = 1


class UserRetrieveSerializer(serializers.ModelSerializer):
    tags = UserTagSerializer

    class Meta:
        model = User
        fields = [
            "id",
            "first_name", "last_name", "middle_name",
            "phone_number",
            "created_at", "updated_at",
            "tags",
        ]
        depth = 1


