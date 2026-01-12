from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "priority", "user", "created_at"]
    list_filter = ["status", "priority", "created_at"]
    search_fields = ["title", "description"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
