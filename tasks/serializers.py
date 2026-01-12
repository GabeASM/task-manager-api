from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from .models import Task


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar información básica del usuario.
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id"]


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Task.
    """

    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "created_at",
            "updated_at",
            "user",
            "user_id",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user"]

    def create(self, validated_data):
        """
        Asigna automáticamente el usuario autenticado al crear una tarea.
        """
        validated_data.pop("user_id", None)

        if "user" not in validated_data:
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                validated_data["user"] = request.user

        return super().create(validated_data)

    def validate_due_date(self, value):
        """
        Valida que la fecha límite no sea en el pasado.
        """
        if value and value < timezone.now():
            raise serializers.ValidationError(
                "La fecha límite no puede ser en el pasado."
            )
        return value


class TaskListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tareas (sin detalles completos).
    """

    user_username = serializers.CharField(source="user.username", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    priority_display = serializers.CharField(
        source="get_priority_display", read_only=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "status",
            "status_display",
            "priority",
            "priority_display",
            "due_date",
            "created_at",
            "user_username",
        ]
