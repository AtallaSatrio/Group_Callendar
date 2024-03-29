import jwt
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from apps.accounts.models import User


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pkid", "id", "email", "username")


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    default_error_messages = {
        "email_taken": _("This email is already in use"),
    }

    class Meta:
        model = User
        fields = ("email", "username", "password", "confirm_password")

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Password does not match")
        return data

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError("Email already used")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        "inactive_account": _("Employee account is disabled"),
        "invalid_credentials": _("Unable to login with provided credentials"),
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(
            email=attrs.get("email"), password=attrs.get("password")
        )

        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(
                    self.error_messages["inactive_account"]
                )
            return attrs
        else:
            raise serializers.ValidationError(
                self.error_messages["invalid_credentials"]
            )

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(self.user)
        life_time = int(refresh.access_token.lifetime.total_seconds())
        response = {
            "id": self.user.id,
            "email": self.user.email,
            "token": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "life_time": life_time,
            },
        }
        return response


class UserRefreshTokenSerializer(TokenRefreshSerializer):
    def __init__(self, *args, **kwargs):
        super(UserRefreshTokenSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        data = super().validate(attrs)
        data["refresh"] = attrs.get("refresh")
        return data

    def get_new_token(self, validated_data):
        access_token = validated_data.get("access")
        refresh_token = validated_data.get("refresh")
        refresh = RefreshToken(refresh_token)
        life_time = int(refresh.access_token.lifetime.total_seconds())
        jwt_decode = jwt.decode(
            access_token,
            settings.SIMPLE_JWT["SIGNING_KEY"],
            algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
        )

        self.user = User.objects.get(id=jwt_decode["user_id"])
        response_formated = {
            "user": self.user.id,
            "token": {
                "access": access_token,
                "life_time": life_time,
            },
        }
        return response_formated
