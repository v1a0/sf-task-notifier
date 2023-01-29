from rest_framework import generics
from addressee.serializers import AddresseeSerializer, AddresseeRetrieveSerializer
from rest_framework.response import Response
import rest_framework.status as drf_statuses
from drf_yasg.utils import swagger_auto_schema

from addressee.models import Addressee

from misc.views import DefaultGenericCreateView, DefaultRetrieveUpdateDestroyView


class AddresseeCreateView(DefaultGenericCreateView):
    serializer_class = AddresseeSerializer
    retrieve_serializer_class = AddresseeRetrieveSerializer

    @swagger_auto_schema(
        operation_description='Create user Addressee',
        responses={
            drf_statuses.HTTP_201_CREATED: AddresseeRetrieveSerializer()
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AddresseesListView(generics.ListAPIView):
    queryset = Addressee.objects.all()
    serializer_class = AddresseeRetrieveSerializer

    @swagger_auto_schema(
        operation_description="Get all Addressee",
        responses={
            drf_statuses.HTTP_200_OK: AddresseeRetrieveSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AddresseeRetrieveUpdateDestroyView(DefaultRetrieveUpdateDestroyView):
    queryset = Addressee.objects.all()
    retrieve_serializer_class = AddresseeRetrieveSerializer
    update_serializer_class = AddresseeSerializer

    @swagger_auto_schema(
        operation_description="Update Addressee",
        responses={
            drf_statuses.HTTP_200_OK: retrieve_serializer_class()
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)\
    

    @swagger_auto_schema(
        operation_description="Delete Addressee",
        responses={
            drf_statuses.HTTP_204_NO_CONTENT: 'Done'
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
