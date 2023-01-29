from rest_framework import generics
from addressee.serializers import AddresseeSerializer, AddresseeRetrieveSerializer
from rest_framework.response import Response
import rest_framework.status as drf_statuses
from drf_yasg.utils import swagger_auto_schema

from addressee.models import Addressee

from misc.views import DefaultGenericCreateView


class AddresseeCreateView(DefaultGenericCreateView):
    serializer_class = AddresseeSerializer
    response_serializer_class = AddresseeRetrieveSerializer

    @swagger_auto_schema(
        operation_description='Create user',
        responses={
            201: AddresseeRetrieveSerializer()
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AddresseesListView(generics.ListAPIView):
    queryset = Addressee.objects.all()
    serializer_class = AddresseeRetrieveSerializer
