from django.db import transaction
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from addressee.models import Addressee, AddresseeTag
from misc.messages import MSG


class AddresseeSerializer(serializers.Serializer):

    name = serializers.CharField(required=False, max_length=255, default=None)
    phone_number = serializers.IntegerField(
        required=True,
        error_messages=MSG.ERROR.PHONE,
        max_value=79999999999,
        min_value=70000000000,
        validators=[
            UniqueValidator(
                queryset=Addressee.objects.all().values('phone_number'),
                message='This phone number already registered'
            )],

    )

    tags = serializers.ListField(
        required=False,
        child=serializers.CharField(),
        allow_empty=True,
        default=list()
    )

    @staticmethod
    def filter_tags_to_create(items) -> list:
        tags_to_create = list()

        for tag_title in items:
            if not AddresseeTag.objects.filter(title=tag_title).exists():
                tags_to_create.append(AddresseeTag(name=None, title=tag_title))

        return tags_to_create

    def add_tags_to_addressee(self, addressee: Addressee, tags_names: list[str]):
        tags_to_create = self.filter_tags_to_create(tags_names)

        with transaction.atomic():
            addressee.save()

            if addressee.tags:
                addressee.tags.clear()
            if tags_to_create:
                AddresseeTag.objects.bulk_create(tags_to_create)
            if tags_names:
                addressee.tags.add(*AddresseeTag.objects.filter(title__in=tags_names).values_list('id', flat=True))

        return addressee

    def create(self, validated_data):
        tags_names = validated_data.pop('tags')
        addressee = Addressee(**validated_data)

        self.add_tags_to_addressee(
            addressee=addressee,
            tags_names=tags_names
        )
        addressee.save()

        return addressee

    def update(self, instance: Addressee, validated_data):
        tags_names = validated_data.pop('tags')
        addressee = instance
        addressee.name = validated_data.get('name')
        addressee.phone_number = validated_data.get('phone_number')

        self.add_tags_to_addressee(
            addressee=addressee,
            tags_names=tags_names
        )
        addressee.save()

        return instance


class AddresseeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddresseeTag
        fields = [
            "id",
            "title"
        ]
        depth = 1


class AddresseeRetrieveSerializer(serializers.ModelSerializer):
    tags = AddresseeTagSerializer(many=True)
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

    @swagger_serializer_method(serializer_or_field=serializers.CharField(read_only=True))
    def get_operator_code(self, obj):
        return f'{str(obj.operator_code):0>3}'  # appending zeros at left side up to len == 3
