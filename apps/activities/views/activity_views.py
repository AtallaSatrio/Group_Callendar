from rest_framework import generics, status

# from rest_framework.permissions import IsAuthenticated
from apps.activities.serializers.activity_serializers import (
    ActivitySerializers,
    ActivityListSerializer,
)
from apps.activities.models import Activity
from rest_framework.response import Response
from rest_framework.decorators import api_view


# class TodoDestroyAPIView(generics.DestroyAPIView):
#     serializer_class = TodoDestroySerializer

#     def destroy(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.destroy(serializer.validated_data)
#         return Response(
#             "todo has deleted",
#             status=status.HTTP_200_OK,
#         )


class ActivityListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializers

    def create(self, request):
        # user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        data = self.get_queryset()

        serialzer = ActivitySerializers(data, many=True)

        return Response(serialzer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        queryset = Activity.objects.filter(is_delete=False).order_by("-created_at")

        return queryset


class ActivityRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ActivitySerializers
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializers = self.get_serializer(instance)

        return Response(serializers.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializers = self.get_serializer(instance, request.data)
        serializers.is_valid(raise_exception=True)
        self.perform_update(serializers)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        queryset = Activity.objects.filter(is_delete=False)
        return queryset


# class TodoDestroyAPIView(generics.DestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     # serializer_class = TodoDestroySerializer

#     # def destroy(self, request, *args, **kwargs):
#     #     # serializer = self.get_serializer(data=request.data)
#     #     # serializer.is_valid(raise_exception=True)
#     #     # serializer.destroy(serializer.validated_data)

#     #     return Response(
#     #         "Todo is deleted",
#     #         status=status.HTTP_200_OK,
#     #     )
