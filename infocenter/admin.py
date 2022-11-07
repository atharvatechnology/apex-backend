from django.contrib import admin

from .models import CourseInfo, CourseInfoCategory


@admin.register(CourseInfo)
class CourseInfoAdmin(admin.ModelAdmin):
    """CourseInfo admin."""

    list_display = ["id", "title", "category"]


@admin.register(CourseInfoCategory)
class CourseInfoCategoryAdmin(admin.ModelAdmin):
    """CourseInfoCategory admin."""

    list_display = ["id", "name"]
