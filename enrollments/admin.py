from django.contrib import admin

from common.admin import CreatorBaseModelAdmin
from enrollments.models import (
    Enrollment,
    ExamThroughEnrollment,
    QuestionEnrollment,
    Session,
)


class ExamThroughEnrollmentInline(admin.TabularInline):
    """ExamThroughEnrollment inline."""

    model = ExamThroughEnrollment
    extra = 1
    readonly_fields = ["status"]


class QuestionEnrollmentInline(admin.TabularInline):
    """QuestionEnrollment Inline."""

    model = QuestionEnrollment
    extra = 1


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Enrollment admin."""

    list_display = ("student", "status", "created_at")
    list_filter = ("status", "exams")
    search_fields = ("student__username",)
    inlines = [
        ExamThroughEnrollmentInline,
    ]

    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return super().get_readonly_fields(request, obj) + ["status"]


@admin.register(Session)
class SessionAdmin(CreatorBaseModelAdmin, admin.ModelAdmin):
    """Session admin."""

    list_display = ("exam", "status", "start_date", "end_date")
    list_filter = ("status", "exam")
    inlines = [ExamThroughEnrollmentInline]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return super().get_readonly_fields(request, obj) + ["status"]


@admin.register(ExamThroughEnrollment)
class ExamThroughEnrollmentAdmin(admin.ModelAdmin):
    """Exam through enrollment admin."""

    list_display = ("id", "enrollment", "exam", "selected_session", "score", "status")
    list_filter = ("status", "enrollment", "exam", "selected_session")
    inlines = [
        QuestionEnrollmentInline,
    ]
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return super().get_readonly_fields(request, obj) + ["status"]


@admin.register(QuestionEnrollment)
class QuestionEnrollmentAdmin(admin.ModelAdmin):
    """Question enrollment admin."""

    list_display = ("exam_stat", "question", "selected_option", "updated_at")
    list_filter = ("exam_stat", "question")
