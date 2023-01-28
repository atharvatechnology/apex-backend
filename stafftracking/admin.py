from django.contrib import admin

from stafftracking.models import StaffTracking


@admin.register(StaffTracking)
class StaffTrackingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "latitude", "longitude", "created_at"]
    search_fields = ["user__username", "user__lastname", "user__firstname"]
    date_hierarchy = "created_at"
