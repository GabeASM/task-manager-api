from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskListSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de tareas.

    Endpoints:
    - GET /api/tasks/ - Listar tareas del usuario
    - POST /api/tasks/ - crear nueva tarea
    - GET /api/tasks/{id} - ver detalle de tarea
    - PUT /api/tasks/{id} - Actualizar tarea completa
    - PATCH /api/tasks/{id} - Actualizar tarea parcial
    - DELETE /api/tasks/{id} - Eliminar tarea
    """

    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "priority"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at", "due_date", "priority"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """
        Retonar solo las tareas del usuario autenticado
        """
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        Usa diferentes serializaers para list y retrieve
        """
        if self.action == "list":
            return TaskListSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        """
        Asigna automaticamente el usuario al crear una tarea.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def pending(self, request):
        """
        Endpoint personalizado: GET /api/tasks/pending
        Retorna solo las tareas pendientes.
        """
        tasks = self.get_queryset().filter(status="pending")
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def completed(self, request):
        """
        Endpoint personalizado: GET /api/tasks/completed/
        Retorna solo las tareas completadas.
        """
        tasks = self.get_queryset().filter(status="completed")
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """
        Endpoint personalizado: POST /api/tasks/{id}/complete/
        Marca una tarea como completada.
        """
        task = self.get_object()
        task.status = "completed"
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        Endpoint personalizado: GET /api/tasks/stats/
        Retorna estadisticas de las tareas de usuario.
        """
        queryset = self.get_queryset()

        stats = {
            "total": queryset.count(),
            "pending": queryset.filter(status="pending").count(),
            "in_progress": queryset.filter(status="in_progress").count(),
            "completed": queryset.filter(status="completed").count(),
            "cancelled": queryset.filter(status="cancelled").count(),
            "high_priority": queryset.filter(priority="high").count(),
            "medium_priority": queryset.filter(priority="medium").count(),
            "low_priority": queryset.filter(priority="low").count(),
        }
        return Response(stats)
