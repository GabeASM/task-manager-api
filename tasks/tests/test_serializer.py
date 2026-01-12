from datetime import timedelta

import pytest
from django.utils import timezone

from tasks.models import Task
from tasks.serializers import TaskListSerializer, TaskSerializer


@pytest.mark.django_db
class TestTaskSerializer:
    """Tests para TaskSerializer."""

    def test_serialize_task(self, task):
        """Test serializar una tarea."""
        serializer = TaskSerializer(task)
        data = serializer.data

        assert data["id"] == task.id
        assert data["title"] == task.title
        assert data["description"] == task.description
        assert data["status"] == task.status
        assert data["priority"] == task.priority
        assert "user" in data
        assert data["user"]["username"] == task.user.username

    def test_deserialize_valid_data(self, user, task_data):
        """Test deserializar datos válidos."""
        serializer = TaskSerializer(data=task_data)

        assert serializer.is_valid(), serializer.errors

        task = serializer.save(user=user)

        assert task.title == task_data["title"]
        assert task.user == user

    def test_validate_due_date_future(self, task_data):
        """Test que due_date en el futuro es válido."""
        future_date = timezone.now() + timedelta(days=7)
        task_data["due_date"] = future_date

        serializer = TaskSerializer(data=task_data)

        assert serializer.is_valid(), serializer.errors

    def test_validate_due_date_past_invalid(self, task_data):
        """Test que due_date en el pasado es inválido."""
        past_date = timezone.now() - timedelta(days=7)
        task_data["due_date"] = past_date

        serializer = TaskSerializer(data=task_data)

        # Necesitas llamar a is_valid() con raise_exception=False
        is_valid = serializer.is_valid(raise_exception=False)

        assert not is_valid, f"Expected invalid but got: {serializer.validated_data}"
        assert (
            "due_date" in serializer.errors
        ), f"Expected due_date error but got: {serializer.errors}"

    def test_required_fields(self):
        """Test que title es requerido."""
        serializer = TaskSerializer(data={})

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_read_only_fields(self, task_data):
        """Test que campos read_only no se pueden modificar."""
        task_data["id"] = 999
        task_data["created_at"] = timezone.now()

        serializer = TaskSerializer(data=task_data)

        assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
class TestTaskListSerializer:
    """Tests para TaskListSerializer."""

    def test_list_serializer_fields(self, task):
        """Test que el serializer de lista tiene los campos correctos."""
        serializer = TaskListSerializer(task)
        data = serializer.data

        assert "id" in data
        assert "title" in data
        assert "status" in data
        assert "status_display" in data
        assert "priority" in data
        assert "priority_display" in data
        assert "user_username" in data
        assert data["user_username"] == task.user.username

    def test_status_display(self, task):
        """Test que status_display muestra el valor legible."""
        task.status = "completed"
        task.save()

        serializer = TaskListSerializer(task)

        assert serializer.data["status_display"] == "Completada"
