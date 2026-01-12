from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    """
    Modelo para representar una tarea
    """

    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("in_progress", "En progreso"),
        ("completed", "Completada"),
        ("cancelled", "Cancelada"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Baja"),
        ("medium", "Media"),
        ("high", "Alta"),
    ]

    title = models.CharField(max_length=200, verbose_name="Titulo")
    description = models.TextField(blank=True, verbose_name="Descripción")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Estado"
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
        verbose_name="Prioridad",
    )

    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha limite")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Ultima actualización"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", verbose_name="Usuario"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
