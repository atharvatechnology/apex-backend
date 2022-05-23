from django.contrib import admin

from .models import Content, Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ["name"]
