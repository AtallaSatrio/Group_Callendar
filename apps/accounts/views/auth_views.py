from django.contrib.auth.models import update_last_login
from rest_framework import generics, status
from rest_framework.response import Response
from apps.accounts.models import User
from apps.accounts.serializers.auth_serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserRefreshTokenSerializer,
    UserGetSerializer,
)
from rest_framework.permissions import IsAuthenticated


class UserGetAPIView(generics.ListAPIView):
    serializer_class = UserGetSerializer
    queryset = User.objects.all()


class UserRegistrationAPIView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serialzers = self.get_serializer(data=request.data)
        serialzers.is_valid(raise_exception=True)
        serialzers.save()
        return Response(data=serialzers.data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        update_last_login(None, serializers.user)
        response = Response(serializers.data, status=status.HTTP_200_OK)
        response.set_cookie("refresh", str(serializers.data["token"]["refresh"]))
        return response
