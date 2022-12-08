from django.contrib import admin

from attendance.models import (  # Attendance,
    StudentAttendance,
    TeacherAttendance,
    TeacherAttendanceDetail,
)
from common.admin import CreatorBaseModelAdmin


# @admin.register(Attendance)
class AttendanceAdmin(CreatorBaseModelAdmin):
    """Attendance Admin panel."""

    list_display = ("date", "user")


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(CreatorBaseModelAdmin):
    """Student Attendance Admin panel."""

    list_display = ("id", "date", "user", "created_at", "created_by")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    date_hierarchy = "date"


class TeacherAttendanceDetailInline(admin.TabularInline):
    """Teacher Attendance Detail Inline."""

    model = TeacherAttendanceDetail
    extra = 1
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]
    list_display = (
        "id",
        "number_of_period",
        "remarks",
        "status",
        "section",
        "subject",
        "start_time",
        "end_time",
    )


@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(CreatorBaseModelAdmin, admin.ModelAdmin):
    """Teacher Attendance Admin panel."""

    list_display = ("id", "date", "user")
    inlines = [TeacherAttendanceDetailInline]

    def save_formset(self, request, form, formset, change):
        """Formset save to update created_by and updated_by."""
        if formset.model == TeacherAttendanceDetail:
            for instance in formset.save(commit=False):
                if not change:
                    instance.created_by = request.user
                instance.updated_by = request.user
                instance.save()
