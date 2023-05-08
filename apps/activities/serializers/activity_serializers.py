from datetime import timezone
from rest_framework import serializers
from apps.accounts.models import User
from apps.activities.models import Activity


class ActivitySerializers(serializers.ModelSerializer):
    # asignees = serializers.ListField(
    #     child=serializers.CharField(max_length=100), required=False
    # )
    asignees = serializers.ListField(child=serializers.UUIDField(), required=False)

    class Meta:
        model = Activity
        fields = [
            "id",
            "tanggal",
            "judul",
            "deskripsi",
            "prioritas",
            "label",
            # "creator",
            "asignees",
        ]

    def create(self, validated_data):
        user = self.context.get("user")
        print(user)
        validated_data["creator"] = user
        asignees = validated_data.pop("asignees", [])
        print(asignees)

        if asignees is not None:
            for asignee in asignees:
                obj_activity = Activity.objects.create(**validated_data)

                for user in asignees:
                    obj_activity.asignees.add(User.objects.get(id=user))

        activity_copy = Activity.objects.create(**validated_data)
        for user in asignees:
            activity_copy.asignees.add(User.objects.get(id=user))
        # KALAU MAU GET ACTIVITY BERDASARKAN ID BISA PAKE ACTIVITY.ASIGNEES.FILTER(USER)
        # obj_activity.asign = asign
        # obj_activity.save()
        return activity_copy

    def update(self, instance, validated_data):
        judul = validated_data.get("judul")
        deskripsi = validated_data.get("deskripsi")
        prioritas = validated_data.get("prioritas")

        activity_instance = Activity.objects.filter(id=instance.id).first()
        activity_instance.judul = judul
        activity_instance.deskripsi = deskripsi
        activity_instance.prioritas = prioritas
        activity_instance.save()

        return activity_instance

    def to_representation(self, instance):
        user_id = []
        for user in instance.asignees.all():
            user_id.append(user.username)
        return {
            "id": instance.id,
            "judul": instance.judul,
            "deskripsi": instance.deskripsi,
            "prioritas": instance.prioritas,
            "label": instance.label,
            "asignees": user_id,
        }


class ActivityListSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            "id",
            "judul",
            "deskripsi",
            "prioritas",
            "label",
            "asign",
            "created_at",
        ]

    def get_created_at(self, obj):
        date = timezone.localtime(obj.created_at)
        formatted_date = date.strftime("%d %B %Y %H:%M:%S")
        return formatted_date


# class TodoDestroySerializer(serializers.Serializer):
#     id_todos = serializers.ListField(child=serializers.CharField(max_length=100))

#     def destroy(self, validated_data):
#         get_id_todos = validated_data.get("id_todos")
#         Todo.objects.filter(id__in=get_id_todos).update(is_delete=True)
