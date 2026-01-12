import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tasks.models import Task


@pytest.fixture
def api_client():
    """Cliente API de DRF para hacer peticiones."""
    return APIClient()


@pytest.fixture
def user(db):
    """Usuario de prueba."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def other_user(db):
    """Otro usuario de prueba."""
    return User.objects.create_user(
        username="otheruser",
        email="other@example.com",
        password="otherpass123",
        first_name="Other",
        last_name="User",
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Cliente autenticado con JWT."""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def task(user):
    """Tarea de prueba."""
    return Task.objects.create(
        title="Test Task",
        description="Test Description",
        status="pending",
        priority="medium",
        user=user,
    )


@pytest.fixture
def task_data():
    """Datos válidos para crear una tarea."""
    return {
        "title": "Nueva Tarea",
        "description": "Descripción de la tarea",
        "status": "pending",
        "priority": "high",
    }
