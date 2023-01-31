from rest_framework import generics
import rest_framework.status as drf_statuses
from drf_yasg.utils import swagger_auto_schema

from misc.views import DefaultGenericCreateView, DefaultRetrieveUpdateDestroyView
from messaging.models import MessagingEvent
from messaging.serializers import MessagingEventSerializer, MessagingEventRetrieveSerializer, \
    MessagingEventStatisticRetrieveSerializer


class MessagingEventCreateView(DefaultGenericCreateView):
    serializer_class = MessagingEventSerializer
    retrieve_serializer_class = MessagingEventRetrieveSerializer

    @swagger_auto_schema(
        operation_description='Create messaging event',
        responses={
            201: MessagingEventRetrieveSerializer()
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MessagingEventListView(generics.ListAPIView):
    queryset = MessagingEvent.objects.all()
    serializer_class = MessagingEventRetrieveSerializer

    @swagger_auto_schema(
        operation_description="Get all MessagingEvents",
        responses={
            drf_statuses.HTTP_200_OK: MessagingEventRetrieveSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MessagingEventRetrieveUpdateDestroyView(DefaultRetrieveUpdateDestroyView):
    queryset = MessagingEvent.objects.all()
    retrieve_serializer_class = MessagingEventRetrieveSerializer
    update_serializer_class = MessagingEventSerializer

    @swagger_auto_schema(
        operation_description="Get MessagingEvent",
        responses={
            drf_statuses.HTTP_200_OK: retrieve_serializer_class()
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update MessagingEvent",
        responses={
            drf_statuses.HTTP_200_OK: retrieve_serializer_class()
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="Delete MessagingEvent",
        responses={
            drf_statuses.HTTP_204_NO_CONTENT: 'Done'
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MessagingEventStatisticRetrieveView(DefaultRetrieveUpdateDestroyView):
    queryset = MessagingEvent.objects.all()
    retrieve_serializer_class = MessagingEventStatisticRetrieveSerializer

    @swagger_auto_schema(
        operation_description="Get MessagingEvent",
        responses={
            drf_statuses.HTTP_200_OK: retrieve_serializer_class()
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)