from django.contrib import admin

from .models import Content, Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
