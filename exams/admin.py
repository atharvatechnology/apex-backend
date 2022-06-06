import nested_admin
from django import forms
from django.contrib import admin

from common.admin import CreatorBaseModelAdmin
from exams.models import Exam, ExamTemplate, Option, Question, Section


class CustomStackedInline(nested_admin.NestedStackedInline):
    template = "inlines/stacked.html"


class CustomTabularInline(nested_admin.NestedTabularInline):
    template = "inlines/tabular.html"


class OptionsAdminForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = "__all__"


class OptionInline(nested_admin.NestedTabularInline):
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
    model = Question
    extra = 1
    inlines = [
        OptionInline,
    ]
    form = QuestionAdminForm


class SectionInline(nested_admin.NestedStackedInline):
    model = Section
    extra = 1


@admin.register(ExamTemplate)
class ExamTemplateAdmin(CreatorBaseModelAdmin, nested_admin.NestedModelAdmin):
    list_display = [
        "id",
        "name",
        "duration",
        "full_marks",
        "pass_marks",
        "display_num_questions",
    ]
    inlines = [
        SectionInline,
    ]


@admin.register(Exam)
class ExamAdmin(CreatorBaseModelAdmin, nested_admin.NestedModelAdmin):
    list_display = ["id", "name", "status", "price", "template"]
    list_filter = ["status", "template"]
    inlines = [
        QuestionInline,
    ]
    readonly_fields = ["id"]
    save_on_top = True


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "num_of_questions",
        "pos_marks",
        "neg_marks",
        "template",
    ]
    list_filter = ["template"]
    readonly_fields = ["id"]


@admin.register(Question)
class QuestionAdmin(nested_admin.NestedModelAdmin):
    list_display = ["id", "detail", "exam"]
    list_filter = ["exam"]
    readonly_fields = ["id"]

    inlines = [
        OptionInline,
    ]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ["id", "detail", "question"]
    list_filter = ["question"]
    readonly_fields = ["id"]
