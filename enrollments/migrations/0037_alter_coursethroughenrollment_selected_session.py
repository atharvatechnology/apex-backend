# Generated by Django 3.2.13 on 2022-08-04 05:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enrollments", "0036_alter_examthroughenrollment_selected_session"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursethroughenrollment",
            name="selected_session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_enrolls",
                to="enrollments.coursesession",
            ),
        ),
    ]
