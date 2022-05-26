from django.contrib import admin

from .models import Content, Note


class ContentTabularInline(admin.TabularInline):
    model = Content
    extra = 1
    readonly_fields = ["created_by", "updated_by"]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not hasattr(instance, "created_by"):
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    inlines = [ContentTabularInline]
    readonly_fields = ["created_by", "updated_by"]

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not hasattr(instance, "created_by"):
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

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
