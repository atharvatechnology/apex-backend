from django.contrib import admin

from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "meeting_id",
        "host_id",
        "host_email",
        "variant",
        "start_time",
        "course",
        "created_at",
        "topic",
        "duration",
    ]
    readonly_fields = ["id"]
