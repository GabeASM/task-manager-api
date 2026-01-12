import pytest
from django.utils import timezone

from tasks.models import Task


@pytest.mark.django_db
class TestTaskModel:
    """Tests para el modelo Task."""

    def test_create_task(self, user):
        """Test crear una tarea."""
        task = Task.objects.create(
            title="Mi Tarea",
            description="Descripción",
            status="pending",
            priority="high",
            user=user,
        )

        assert task.id is not None
        assert task.title == "Mi Tarea"
        assert task.status == "pending"
        assert task.user == user
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_str_representation(self, task):
        """Test el método __str__ del modelo."""
        expected = f"{task.title} - Pendiente"
        assert str(task) == expected

    def test_task_default_values(self, user):
        """Test valores por defecto."""
        task = Task.objects.create(title="Tarea Mínima", user=user)

        assert task.status == "pending"
        assert task.priority == "medium"
        assert task.description == ""
        assert task.due_date is None

    def test_task_choices_display(self, task):
        """Test get_status_display y get_priority_display."""
        task.status = "completed"
        task.priority = "high"
        task.save()

        assert task.get_status_display() == "Completada"
        assert task.get_priority_display() == "Alta"

    def test_task_ordering(self, user):
        """Test que las tareas se ordenan por created_at descendente."""
        task1 = Task.objects.create(title="Tarea 1", user=user)
        task2 = Task.objects.create(title="Tarea 2", user=user)
        task3 = Task.objects.create(title="Tarea 3", user=user)

        tasks = Task.objects.all()

        assert tasks[0] == task3  # Más reciente primero
        assert tasks[1] == task2
        assert tasks[2] == task1

    def test_user_relationship(self, user):
        """Test relación con User."""
        task1 = Task.objects.create(title="Tarea 1", user=user)
        task2 = Task.objects.create(title="Tarea 2", user=user)

        # Acceso reverso
        user_tasks = user.tasks.all()

        assert user_tasks.count() == 2
        assert task1 in user_tasks
        assert task2 in user_tasks

    def test_task_cascade_delete(self, user, task):
        """Test que al borrar usuario se borran sus tareas."""
        task_id = task.id
        user.delete()

        assert not Task.objects.filter(id=task_id).exists()
