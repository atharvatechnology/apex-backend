from django import forms
from django.contrib import admin
from django.db import models

from common.admin import CreatorBaseModelAdmin
from enrollments.models import (
    CourseThroughEnrollment,
    Enrollment,
    ExamSession,
    ExamThroughEnrollment,
    QuestionEnrollment,
    Session,
)


class ExamThroughEnrollmentInline(admin.TabularInline):
    """ExamThroughEnrollment inline."""

    model = ExamThroughEnrollment
    extra = 1
    readonly_fields = ["status"]


class CourseThroughEnrollmentInline(admin.TabularInline):
    """CourseThroughEnrollment inline."""

    model = CourseThroughEnrollment
    extra = 1
    readonly_fields = ["course_enroll_status"]


@admin.register(CourseThroughEnrollment)
class CourseThroughEnrollmentAdmin(admin.ModelAdmin):
    list_display = ["id", "enrollment"]


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
        CourseThroughEnrollmentInline,
    ]
    date_hierarchy = "created_at"

    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return super().get_readonly_fields(request, obj) + ["status"]


class CustomAdminSplitDateTime(admin.widgets.AdminSplitDateTime):
    def __init__(self, attrs=None):
        widgets = [
            admin.widgets.AdminDateWidget,
            admin.widgets.AdminTimeWidget(attrs=None, format="%H:%M"),
        ]
        forms.MultiWidget.__init__(self, widgets, attrs)


@admin.register(Session)
class SessionAdmin(CreatorBaseModelAdmin, admin.ModelAdmin):
    """Session admin."""

    list_display = ("status", "start_date", "end_date")
    # , "is_published")
    list_filter = ("status",)
    inlines = [ExamThroughEnrollmentInline]
    formfield_overrides = {
        models.DateTimeField: {
            "widget": CustomAdminSplitDateTime(),
            "help_text": "Seconds doesnot matters",
        },
    }
    date_hierarchy = "created_at"
    readonly_fields = CreatorBaseModelAdmin.readonly_fields + ["end_date"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return super().get_readonly_fields(request, obj) + [
            "status",
        ]


@admin.register(ExamSession)
class ExamSessionAdmin(CreatorBaseModelAdmin, admin.ModelAdmin):
    """Session admin."""

    list_display = ("status", "start_date", "end_date", "result_is_published")
    list_filter = ("status",)
    inlines = [ExamThroughEnrollmentInline]
    formfield_overrides = {
        models.DateTimeField: {
            "widget": CustomAdminSplitDateTime(),
            "help_text": "Seconds doesnot matters",
        },
    }
    date_hierarchy = "created_at"
    readonly_fields = CreatorBaseModelAdmin.readonly_fields + ["end_date"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return super().get_readonly_fields(request, obj) + [
            "status",
        ]


@admin.register(ExamThroughEnrollment)
class ExamThroughEnrollmentAdmin(admin.ModelAdmin):
    """Exam through enrollment admin."""

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("enrollment", "exam")
            .prefetch_related("question_states")
        )

    def question(self, obj):
        return obj.question_states.all().count()

    list_display = ("id", "enrollment", "exam", "question", "score", "status")
    list_filter = ("status", "exam", "selected_session")
    inlines = [
        QuestionEnrollmentInline,
    ]
    readonly_fields = []
    date_hierarchy = "enrollment__created_at"

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return super().get_readonly_fields(request, obj) + ["status"]


@admin.register(QuestionEnrollment)
class QuestionEnrollmentAdmin(admin.ModelAdmin):
    """Question enrollment admin."""

    list_display = ("exam_stat", "question", "selected_option", "updated_at")
    list_filter = ("question__exam",)
    search_fields = (
        "exam_stat__enrollment__student__first_name",
        "exam_stat__enrollment__student__last_name",
    )
