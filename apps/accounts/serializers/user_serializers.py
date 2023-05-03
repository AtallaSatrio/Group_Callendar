from apps.accounts.models import User
from rest_framework import serializers
from django.utils import timezone


class UserRetrieveSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()

    def get_date_joined(self, obj):
        date = timezone.localtime(obj.date_joined)
        formatted_date = date.strftime("%d %B %Y %H:%M:%S")
        return formatted_date

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "is_superuser",
            "is_staff",
            "is_team_lead",
            "is_active",
            "date_joined",
        ]
