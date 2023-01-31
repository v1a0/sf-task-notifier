from rest_framework import generics
from rest_framework.response import Response
import rest_framework.status as drf_statuses
from drf_yasg.utils import swagger_auto_schema


class DefaultGenericCreateView(generics.CreateAPIView):
    serializer_class = None
    retrieve_serializer_class = None

    # http_method_names = ['options', 'post']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer_response = self.retrieve_serializer_class(serializer.instance)
        headers = self.get_success_headers(serializer_response.instance)

        return Response(
            serializer_response.data,
            status=drf_statuses.HTTP_201_CREATED,
            headers=headers
        )


class DefaultRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    retrieve_serializer_class = None
    update_serializer_class = None

    # http_method_names = ['get', 'options', 'put', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.retrieve_serializer_class
        elif self.request.method == 'PUT':
            return self.update_serializer_class
        else:
            return None

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(self.retrieve_serializer_class(serializer.instance).data)

    @swagger_auto_schema(
        operation_description="Удаление объекта",
        responses={drf_statuses.HTTP_204_NO_CONTENT: 'Done'}
    )
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return Response(
            'Done', status=drf_statuses.HTTP_204_NO_CONTENT
        )
