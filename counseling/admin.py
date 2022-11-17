from django.contrib import admin

from counseling.models import Counseling

# Register your models here.


@admin.register(Counseling)
class CounselingAdmin(admin.ModelAdmin):
    """Admin for Counseling Model."""

    list_display = (
        "id",
        "student_name",
        "counsellor",
        "note",
        "phone_number",
        "created_at",
    )
