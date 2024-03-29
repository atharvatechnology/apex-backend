# Generated by Django 3.2.13 on 2022-08-04 02:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enrollments", "0035_coursesession"),
    ]

    operations = [
        migrations.AlterField(
            model_name="examthroughenrollment",
            name="selected_session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="session_enrolls",
                to="enrollments.examsession",
                verbose_name="exam_session",
            ),
        ),
    ]
