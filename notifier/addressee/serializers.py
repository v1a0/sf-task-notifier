from django.db import transaction
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from addressee.models import Addressee, AddresseeTag
import misc.regexes as reg
from misc.messages import MSG


class AddresseeSerializer(serializers.Serializer):

    name = serializers.CharField(required=False, max_length=255, default=None)
    phone_number = serializers.RegexField(
        required=True,
        regex=reg.PHONE_NUMBER,
        error_messages=MSG.ERROR.PHONE,
        validators=[
            UniqueValidator(
                queryset=Addressee.objects.all().values('phone_number'),
                message='This number already registered'
            )],

    )

    tags = serializers.ListField(
        required=False,
        child=serializers.CharField(),
        allow_empty=True,
        default=list()
    )

    def create(self, validated_data):
        tags_names = validated_data.pop('tags')
        user = Addressee(**validated_data)
        tags_to_create = list()

        for tag_title in tags_names:
            if not AddresseeTag.objects.filter(title=tag_title).exists():
                tags_to_create.append(AddresseeTag(name=None, title=tag_title))

        with transaction.atomic():
            user.save()

            if tags_to_create:
                AddresseeTag.objects.bulk_create(tags_to_create)
            if tags_names:
                user.tags.add(*AddresseeTag.objects.filter(title__in=tags_names).values_list('id', flat=True))
                user.save()

        return user

    def update(self, instance, validated_data):
        pass


class AddresseeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddresseeTag
        fields = [
            "id",
            "name",
            "title"
        ]
        depth = 1


class AddresseeRetrieveSerializer(serializers.ModelSerializer):
    tags = AddresseeTagSerializer
    operator_code = serializers.SerializerMethodField()

    class Meta:
        model = Addressee
        fields = [
            "id",
            "name",
            "phone_number",
            "operator_code",
            "tags",
            "created_at", "updated_at",
        ]
        depth = 1

    @staticmethod
    def get_operator_code(obj):
        return f'{str(obj.operator_code):0>3}'  # appending zeros at left side up to len == 3

