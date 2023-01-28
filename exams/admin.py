import nested_admin
from django import forms
from django.contrib import admin
from django.utils.html import mark_safe

from common.admin import CreatorBaseModelAdmin
from exams.models import Exam, ExamImage, ExamTemplate, Option, Question, Section


class CustomStackedInline(nested_admin.NestedStackedInline):
    template = "inlines/stacked.html"


class CustomTabularInline(nested_admin.NestedTabularInline):
    template = "inlines/tabular.html"


class OptionsAdminForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = "__all__"


class OptionInline(nested_admin.NestedTabularInline):
    """Option Inline."""

    model = Option
    extra = 0
    max_num = 4


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        widgets = {
            "feedback": admin.widgets.AdminTextareaWidget(attrs={"rows": 3, "cols": 2}),
        }


class QuestionInline(nested_admin.NestedStackedInline):
    """Question Inline with nested stacked inline."""

    model = Question
    extra = 1
    inlines = [
        OptionInline,
    ]
    form = QuestionAdminForm


class SectionInline(nested_admin.NestedStackedInline):
    """Section Inline with nested stacked inline."""

    model = Section
    extra = 1


@admin.register(ExamTemplate)
class ExamTemplateAdmin(CreatorBaseModelAdmin, nested_admin.NestedModelAdmin):
    """Exam Template Admin panel with nested admin."""

    list_display = [
        "id",
        "name",
        "duration",
        "full_marks",
        "pass_percentage",
        "display_num_questions",
    ]
    inlines = [
        SectionInline,
    ]


@admin.register(Exam)
class ExamAdmin(CreatorBaseModelAdmin, nested_admin.NestedModelAdmin):
    """Exam Admin Panel with nested admin inlines."""

    def preview(self, obj):
        return mark_safe(f'<a href="/exam-preview/{obj.id}">Preview</a>')

    def question(self, obj):
        return obj.questions.all().count()

    list_display = ["id", "name", "price", "question", "template", "preview"]
    list_filter = ["template", "category"]
    inlines = [
        QuestionInline,
    ]
    readonly_fields = CreatorBaseModelAdmin.readonly_fields + ["id"]
    save_on_top = True
    # list_editable = ["status"]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """Section Admin Customization."""

    list_display = [
        "id",
        "name",
        "num_of_questions",
        "pos_marks",
        "neg_percentage",
        "template",
    ]
    list_filter = ["template"]
    readonly_fields = ["id"]


@admin.register(Question)
class QuestionAdmin(nested_admin.NestedModelAdmin):
    """Question Admin Customization."""

    list_display = ["id", "detail", "img", "exam"]
    list_filter = ["exam"]
    readonly_fields = ["id"]

    inlines = [
        OptionInline,
    ]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    """Option Admin Customization."""

    list_display = ["id", "detail", "img", "question"]
    list_filter = ["question__exam"]
    readonly_fields = ["id"]


@admin.register(ExamImage)
class ExamImageAdmin(admin.ModelAdmin):
    """ExamImage Admin."""

    list_display = ["id", "exam", "upload"]
    list_filter = ["exam"]
    readonly_fields = ["id"]
