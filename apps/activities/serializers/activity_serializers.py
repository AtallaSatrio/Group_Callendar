from datetime import timezone
from rest_framework import serializers
from apps.activities.models import Activity


class ActivitySerializers(serializers.ModelSerializer):
    asign = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False
    )

    class Meta:
        model = Activity
        fields = [
            "id",
            "tanggal",
            "judul",
            "deskripsi",
            "prioritas",
            "label",
            "asign",
        ]

    def create(self, validated_data):
        asign = validated_data.pop("asign", [])
        obj_activity = Activity.objects.create(**validated_data)
        obj_activity.asign = asign
        obj_activity.save()
        return obj_activity

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
