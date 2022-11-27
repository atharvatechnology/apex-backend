from django.contrib import admin

from common.admin import CreatorBaseModelAdmin

from .models import CourseInfo, CourseInfoCategory, WebResouce


@admin.register(CourseInfo)
class CourseInfoAdmin(admin.ModelAdmin):
    """CourseInfo admin."""

    list_display = ["id", "title", "category"]


@admin.register(CourseInfoCategory)
class CourseInfoCategoryAdmin(admin.ModelAdmin):
    """CourseInfoCategory admin."""

    list_display = ["id", "name"]


@admin.register(WebResouce)
class WebResouceAdmin(CreatorBaseModelAdmin):
    """WebResouce admin."""

    list_display = ["id", "title", "created_at", "created_by"]
