from django.contrib import admin

from stafftracking.models import StaffConnectionStatus, StaffTracking


@admin.register(StaffTracking)
class StaffTrackingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "latitude", "longitude", "created_at"]
    search_fields = ["user__username", "user__lastname", "user__firstname"]
    date_hierarchy = "created_at"


@admin.register(StaffConnectionStatus)
class StaffConnectionStatusAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "is_connected", "is_enabled"]
    search_fields = ["user__username", "user__lastname", "user__firstname"]
