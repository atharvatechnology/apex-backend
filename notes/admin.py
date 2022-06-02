from django.contrib import admin

from common.admin import CreatorBaseModelAdmin

from .models import Content, Note


class ContentTabularInline(admin.TabularInline):
    model = Content
    extra = 1
    readonly_fields = ["created_by", "updated_by"]


@admin.register(Content)
class ContentAdmin(CreatorBaseModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Note)
class NoteAdmin(CreatorBaseModelAdmin, admin.ModelAdmin):
    list_display = ["id", "title"]
    inlines = [ContentTabularInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if not hasattr(instance, "created_by"):
                instance.created_by = request.user
            instance.updated_by = request.user
            instance.save()
        formset.save_m2m()
