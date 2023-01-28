from django.contrib import admin

from common.admin import CreatorBaseModelAdmin

from .models import CourseInfo, CourseInfoCategory, WebResource


@admin.register(CourseInfo)
class CourseInfoAdmin(admin.ModelAdmin):
    """CourseInfo admin."""

    list_display = ["id", "title", "category"]


@admin.register(CourseInfoCategory)
class CourseInfoCategoryAdmin(admin.ModelAdmin):
    """CourseInfoCategory admin."""

    list_display = ["id", "name"]


@admin.register(WebResource)
class WebResourceAdmin(CreatorBaseModelAdmin):
    """WebResource admin."""

    list_display = ["id", "title", "created_at", "created_by"]
