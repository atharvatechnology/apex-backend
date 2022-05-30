from django.contrib import admin

from courses.models import Course, CourseCategory


class CourseAdmin(admin.ModelAdmin):
    """Admin for Course model."""

    readonly_fields = ("id",)
    list_display = (
        "id",
        "name",
        "category",
        "description",
        "link",
        "password",
        "status",
        "price",
    )
    list_filter = ("status", "category")


class CourseCategoryAdmin(admin.ModelAdmin):
    """Admin for CourseCategory model."""

    readonly_fields = ("id",)
    list_display = (
        "id",
        "name",
        "description",
    )
    search_fields = ["name"]


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
