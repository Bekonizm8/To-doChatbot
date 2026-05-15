from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user_name",
        "title",
        "completed",
        "created_at"
    )

    search_fields = (
        "user_name",
        "title"
    )

    list_filter = (
        "completed",
        'created_at'
    )

    ordering = (
        "id",
    )