import nested_admin
from django import forms
from django.contrib import admin

from exams.models import Exam, ExamTemplate, Option, Question, Section


class CustomStackedInline(nested_admin.NestedStackedInline):
    template = "inlines/stacked.html"


class CustomTabularInline(nested_admin.NestedTabularInline):
    template = "inlines/tabular.html"


class OptionsAdminForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = "__all__"
        widgets = {
            "detail": admin.widgets.AdminTextareaWidget(
                attrs={"rows": 2, "cols": 1, "class": "vTextField"}
            ),
        }


class OptionInline(CustomTabularInline):
    model = Option
    extra = 4
    max_num = 6
    form = OptionsAdminForm


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        widgets = {
            "detail": admin.widgets.AdminTextareaWidget(attrs={"rows": 3, "cols": 2}),
            "feedback": admin.widgets.AdminTextareaWidget(attrs={"rows": 3, "cols": 2}),
        }


class QuestionInline(CustomStackedInline):
    model = Question
    extra = 1
    inlines = [
        OptionInline,
    ]
    form = QuestionAdminForm


class SectionInline(CustomStackedInline):
    model = Section
    extra = 1


@admin.register(ExamTemplate)
class ExamTemplateAdmin(nested_admin.NestedModelAdmin):
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
    readonly_fields = ["id"]


@admin.register(Exam)
class ExamAdmin(nested_admin.NestedModelAdmin):
    list_display = ["id", "name", "status", "price", "template"]
    list_filter = ["status", "template"]
    inlines = [
        QuestionInline,
    ]
    readonly_fields = ["id"]


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
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "detail", "exam"]
    list_filter = ["exam"]
    readonly_fields = ["id"]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ["id", "detail", "question"]
    list_filter = ["question"]
    readonly_fields = ["id"]
