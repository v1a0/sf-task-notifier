from django.utils.timezone import now
from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from django.db import transaction
from django.db.models import Q

from addressee.models import Addressee

from messaging.models import MessagingEvent, ScheduledMessage


class SendToFieldSerializer(serializers.Serializer):
    tags = serializers.ListField(child=serializers.CharField(), required=True, allow_empty=True, help_text='User tags')
    codes = serializers.ListField(child=serializers.CharField(), required=True, allow_empty=True, help_text='Operator code')


class StatisticSerializer(serializers.Serializer):
    scheduled = serializers.IntegerField()
    done = serializers.IntegerField()
    processing = serializers.IntegerField()
    failed = serializers.IntegerField()
    unknown = serializers.IntegerField()


class MessagingEventSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, max_length=255, default=None)
    text = serializers.CharField(required=True)
    send_to = SendToFieldSerializer(required=True)
    start_at = serializers.DateTimeField(required=True)
    stop_at = serializers.DateTimeField(required=True)

    def validate(self, data):
        data = super().validate(data)

        for code in data['send_to']['codes']:
            code: str
            if not code.isdigit() or len(code) != 3:
                raise serializers.ValidationError(f"Invalid operator code '{code}'. Example: '090'")

        if data['start_at'] > data['stop_at']:
            raise serializers.ValidationError(f"Logic issue. Value of 'start_at' should not be greater than 'stop_at'")

        if data['start_at'] < now():
            raise serializers.ValidationError(f"Value of 'start_at' should be greater than present date/time")

        return data

    @staticmethod
    def schedule_messages_for_event(messaging_event, send_to_tags, send_to_codes):
        matched_addressees = Addressee.objects.filter(
            Q(tags__title__in=send_to_tags) | Q(operator_code__in=send_to_codes)
        )
        scheduled_messages = list()

        with transaction.atomic():
            messaging_event.save()

            if messaging_event.scheduled_messages:
                messaging_event.scheduled_messages.filter(status__lt=300).delete()

            for addressee in matched_addressees:
                scheduled_messages.append(
                    ScheduledMessage(
                        event=messaging_event,
                        addressee=addressee
                    )
                )

            ScheduledMessage.objects.bulk_create(scheduled_messages)

        return messaging_event

    def create(self, validated_data):
        messaging_event = MessagingEvent(
            title=validated_data['title'],
            start_at=validated_data['start_at'],
            stop_at=validated_data['stop_at'],
            text=validated_data['text'],
            settings=validated_data['send_to']
        )

        messaging_event = self.schedule_messages_for_event(
            messaging_event=messaging_event,
            send_to_tags=validated_data['send_to']['tags'],
            send_to_codes = [int(code) for code in validated_data['send_to']['codes']]
        )

        return messaging_event

    def update(self, instance, validated_data):
        messaging_event = instance
        messaging_event.title = validated_data['title']
        messaging_event.start_at = validated_data['start_at']
        messaging_event.stop_at = validated_data['stop_at']
        messaging_event.text = validated_data['text']
        messaging_event.settings = validated_data['send_to']

        messaging_event = self.schedule_messages_for_event(
            messaging_event=messaging_event,
            send_to_tags=validated_data['send_to']['tags'],
            send_to_codes=[int(code) for code in validated_data['send_to']['codes']]
        )

        return messaging_event


class MessagingEventRetrieveSerializer(serializers.ModelSerializer):
    statistic = serializers.SerializerMethodField()

    class Meta:
        model = MessagingEvent
        fields = [
            "id",
            "title",
            "start_at",
            "stop_at",
            "text",
            "settings",
            "statistic",
        ]
        depth = 1

    @swagger_serializer_method(serializer_or_field=StatisticSerializer(read_only=True))
    def get_statistic(self, obj):
        obj: MessagingEvent
        data = obj.get_statistic()
        serializer = StatisticSerializer(data)

        return serializer.instance
