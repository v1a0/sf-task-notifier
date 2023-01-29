from rest_framework import generics
from messaging.serializers import MessagingEventCreateSerializer, MessagingEventSerializer
from rest_framework.response import Response
import rest_framework.status as drf_statuses
from drf_yasg.utils import swagger_auto_schema

from addressee.models import Addressee

from misc.views import DefaultGenericCreateView


class MessagingEventCreateView(DefaultGenericCreateView):
    serializer_class = MessagingEventCreateSerializer
    response_serializer_class = MessagingEventSerializer

    @swagger_auto_schema(
        operation_description='Create messaging event',
        responses={
            201: MessagingEventSerializer()
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
