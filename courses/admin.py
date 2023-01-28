import nested_admin
from django import forms
from django.contrib import admin

from notes.models import Content, Note

from .models import Course, CourseCategory


class CustomStackedInline(nested_admin.NestedStackedInline):
    template = "inlines/stacked.html"


class CustomTabularInline(nested_admin.NestedTabularInline):
    template = "inlines/tabular.html"


class ContentAdminForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = "__all__"


class ContentInline(CustomTabularInline):
    model = Content
    form = ContentAdminForm
    extra = 1


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    """Admin for CourseCategory model."""

    readonly_fields = ("id",)
    list_display = (
        "id",
        "name",
        "description",
    )
    search_fields = ["name"]


class NoteAdminForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = "__all__"


class NoteInline(CustomStackedInline):
    model = Note
    extra = 1
    inlines = [ContentInline]
    form = NoteAdminForm


@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    list_display = ["id", "name", "category"]
    # list
    inlines = [NoteInline]
    list_filter = ("status", "category")
