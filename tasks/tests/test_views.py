import pytest
from django.urls import reverse
from rest_framework import status

from tasks.models import Task


@pytest.mark.django_db
class TestTaskViewSet:
    """Tests para TaskViewSet."""

    def test_list_tasks_unauthenticated(self, api_client):
        """Test que usuarios no autenticados no pueden listar tareas."""
        url = reverse("task-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_tasks_authenticated(self, authenticated_client, task):
        """Test listar tareas del usuario autenticado."""
        url = reverse("task-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == task.title

    def test_list_tasks_only_own_tasks(self, authenticated_client, user, other_user):
        """Test que cada usuario solo ve sus propias tareas."""
        Task.objects.create(title="Mi tarea", user=user)
        Task.objects.create(title="Tarea del otro", user=other_user)

        url = reverse("task-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == "Mi tarea"

    def test_create_task(self, authenticated_client, task_data):
        """Test crear una tarea."""
        url = reverse("task-list")
        response = authenticated_client.post(url, task_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == task_data["title"]
        assert response.data["status"] == task_data["status"]
        assert Task.objects.filter(title=task_data["title"]).exists()

    def test_create_task_auto_assign_user(self, authenticated_client, task_data, user):
        """Test que el usuario se asigna automáticamente."""
        url = reverse("task-list")
        response = authenticated_client.post(url, task_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED

        task = Task.objects.get(id=response.data["id"])
        assert task.user == user

    def test_retrieve_task(self, authenticated_client, task):
        """Test obtener detalle de una tarea."""
        url = reverse("task-detail", kwargs={"pk": task.pk})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == task.id
        assert response.data["title"] == task.title

    def test_retrieve_other_user_task_forbidden(self, authenticated_client, other_user):
        """Test que no se puede ver tarea de otro usuario."""
        other_task = Task.objects.create(title="Otra tarea", user=other_user)

        url = reverse("task-detail", kwargs={"pk": other_task.pk})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_task(self, authenticated_client, task):
        """Test actualizar una tarea."""
        url = reverse("task-detail", kwargs={"pk": task.pk})
        update_data = {
            "title": "Título Actualizado",
            "status": "completed",
            "priority": "high",
        }
        response = authenticated_client.patch(url, update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Título Actualizado"
        assert response.data["status"] == "completed"

        task.refresh_from_db()
        assert task.title == "Título Actualizado"
        assert task.status == "completed"

    def test_delete_task(self, authenticated_client, task):
        """Test eliminar una tarea."""
        url = reverse("task-detail", kwargs={"pk": task.pk})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(id=task.id).exists()

    def test_filter_by_status(self, authenticated_client, user):
        """Test filtrar tareas por status."""
        Task.objects.create(title="Pendiente", status="pending", user=user)
        Task.objects.create(title="Completada", status="completed", user=user)

        url = reverse("task-list")
        response = authenticated_client.get(url, {"status": "pending"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["status"] == "pending"

    def test_filter_by_priority(self, authenticated_client, user):
        """Test filtrar tareas por priority."""
        Task.objects.create(title="Alta", priority="high", user=user)
        Task.objects.create(title="Baja", priority="low", user=user)

        url = reverse("task-list")
        response = authenticated_client.get(url, {"priority": "high"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["priority"] == "high"

    def test_search_tasks(self, authenticated_client, user):
        """Test buscar tareas por título o descripción."""
        Task.objects.create(
            title="Comprar pan", description="En la panadería", user=user
        )
        Task.objects.create(title="Llamar doctor", description="Urgente", user=user)

        url = reverse("task-list")
        response = authenticated_client.get(url, {"search": "pan"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert "pan" in response.data["results"][0]["title"].lower()


@pytest.mark.django_db
class TestTaskCustomActions:
    """Tests para actions personalizados."""

    def test_pending_tasks(self, authenticated_client, user):
        """Test endpoint /api/tasks/pending/"""
        Task.objects.create(title="Pendiente 1", status="pending", user=user)
        Task.objects.create(title="Pendiente 2", status="pending", user=user)
        Task.objects.create(title="Completada", status="completed", user=user)

        url = "/api/tasks/pending/"
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_completed_tasks(self, authenticated_client, user):
        """Test endpoint /api/tasks/completed/"""
        Task.objects.create(title="Pendiente", status="pending", user=user)
        Task.objects.create(title="Completada 1", status="completed", user=user)
        Task.objects.create(title="Completada 2", status="completed", user=user)

        url = "/api/tasks/completed/"
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_complete_task_action(self, authenticated_client, task):
        """Test endpoint /api/tasks/{id}/complete/"""
        url = f"/api/tasks/{task.pk}/complete/"
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK

        task.refresh_from_db()
        assert task.status == "completed"

    def test_stats_endpoint(self, authenticated_client, user):
        """Test endpoint /api/tasks/stats/"""
        Task.objects.create(title="T1", status="pending", priority="high", user=user)
        Task.objects.create(
            title="T2", status="completed", priority="medium", user=user
        )
        Task.objects.create(title="T3", status="in_progress", priority="low", user=user)

        url = "/api/tasks/stats/"
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["total"] == 3
        assert response.data["pending"] == 1
        assert response.data["completed"] == 1
        assert response.data["in_progress"] == 1
        assert response.data["high_priority"] == 1
