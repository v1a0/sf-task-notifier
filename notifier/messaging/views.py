from rest_framework import generics
from messaging.serializers import UserCreateSerializer, UserRetrieveSerializer
from rest_framework.response import Response
import rest_framework.status as drf_statuses
from drf_yasg.utils import swagger_auto_schema

from addressee.models import Addressee


class MessagingEventCreateView(generics.CreateAPIView):
    # authentication_classes = [TokenAuthentication]

    serializer_class = UserCreateSerializer
    response_serializer_class = UserRetrieveSerializer

    @swagger_auto_schema(
        operation_description='Create messaging event',
        responses={
            201: UserRetrieveSerializer()
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer_response = self.response_serializer_class(serializer.instance)
        headers = self.get_success_headers(serializer_response.instance)

        return Response(
            serializer_response.data,
            status=drf_statuses.HTTP_201_CREATED,
            headers=headers
        )