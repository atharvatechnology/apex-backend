# Generated by Django 3.2.13 on 2022-08-15 12:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enrollments", "0038_alter_coursethroughenrollment_enrollment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursethroughenrollment",
            name="enrollment",
            field=models.ForeignKey(
                default=23,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_enrolls",
                to="enrollments.enrollment",
            ),
            preserve_default=False,
        ),
    ]
