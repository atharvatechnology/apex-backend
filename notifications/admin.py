from django.contrib import admin

from notifications.models import NotificationMessage


@admin.register(NotificationMessage)
class NotificationMessageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "body",
        "created_at",
    )
    date_hierarchy = "created_at"
