# Generated by Django 3.2.13 on 2022-06-08 07:57
# Custom migration for calculating pass percentage against pass marks and full marks.

from django.db import migrations


def update_passpercentage_against_passmarks(apps, schema_editor):
    """Pass percentage are calculated against pass marks and full marks."""
    ExamTemplate = apps.get_model("exams", "ExamTemplate")

    for exam_template in ExamTemplate.objects.all():
        exam_template.pass_percentage = (
            exam_template.pass_marks / exam_template.full_marks
        )
        exam_template.save()


def reverse_update_passpercentage_against_passmarks(apps, schema_editor):
    """Pass marks are calculated against pass percentage and full marks."""
    ExamTemplate = apps.get_model("exams", "ExamTemplate")

    for exam_template in ExamTemplate.objects.all():
        exam_template.pass_marks = (
            exam_template.full_marks * exam_template.pass_percentage
        )
        exam_template.save()


class Migration(migrations.Migration):

    dependencies = [
        ("exams", "0010_examtemplate_pass_percentage"),
    ]

    operations = [
        migrations.RunPython(
            update_passpercentage_against_passmarks,
            reverse_code=reverse_update_passpercentage_against_passmarks,
        ),
    ]
