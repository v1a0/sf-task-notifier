from rest_framework import generics
from rest_framework.response import Response
import rest_framework.status as drf_statuses


class DefaultGenericCreateView(generics.CreateAPIView):
    serializer_class = None
    response_serializer_class = None

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
