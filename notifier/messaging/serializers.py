from django.db import transaction
from django.db.models import Q

from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from addressee.models import Addressee, AddresseeTag

from messaging.models import MessagingEvent, ScheduledMessage, MessageStatus


class SendToFieldSerializer(serializers.Serializer):
    tags = serializers.ListField(child=serializers.CharField(), required=True, allow_empty=True)
    codes = serializers.ListField(child=serializers.CharField(), required=True, allow_empty=True)


class StatisticSerializer(serializers.Serializer):
    scheduled = serializers.IntegerField()
    done = serializers.IntegerField()
    processing = serializers.IntegerField()
    failed = serializers.IntegerField()
    unknown = serializers.IntegerField()


class MessagingEventCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, max_length=255, default=None)
    text = serializers.CharField(required=True)
    send_to = SendToFieldSerializer(required=True)
    start_at = serializers.DateTimeField(required=True)
    stop_at = serializers.DateTimeField(required=True)

    def validate(self, data):
        data = super().validate(data)

        for code in data['send_to']['codes']:
            code: str
            if not code.isdigit():
                raise serializers.ValidationError(f"Invalid operator code '{code}' ")

        return data

    def create(self, validated_data):

        messaging_event = MessagingEvent(
            title=validated_data['title'],
            start_at=validated_data['start_at'],
            stop_at=validated_data['stop_at'],
            text=validated_data['text']
        )

        send_to_tags = validated_data['send_to']['tags']
        send_to_codes = [int(code) for code in validated_data['send_to']['codes']]

        matched_addressees = Addressee.objects.filter(
            Q(tags__title__in=send_to_tags) | Q(operator_code__in=send_to_codes)
        )
        scheduled_messages = list()

        with transaction.atomic():
            messaging_event.save()

            for addressee in matched_addressees:
                scheduled_messages.append(
                    ScheduledMessage(
                        event=messaging_event,
                        addressee=addressee,
                        is_active=True,
                    )
                )

            ScheduledMessage.objects.bulk_create(scheduled_messages)

        return messaging_event


class MessagingEventSerializer(serializers.ModelSerializer):
    statistic = serializers.SerializerMethodField()

    class Meta:
        model = MessagingEvent
        fields = [
            "id",
            "title",
            "type",
            "start_at",
            "stop_at",
            "text",
            "is_active",
            "statistic",
        ]
        depth = 1

    @swagger_serializer_method(serializer_or_field=StatisticSerializer(read_only=True))
    def get_statistic(self, obj):
        obj: MessagingEvent
        data = obj.get_statistic()
        serializer = StatisticSerializer(data)

        return serializer.instance
