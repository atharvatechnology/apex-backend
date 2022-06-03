# Generated by Django 3.2.13 on 2022-06-03 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enrollments", "0008_auto_20220603_0945"),
    ]

    operations = [
        migrations.AlterField(
            model_name="examthroughenrollment",
            name="status",
            field=models.CharField(
                choices=[
                    ("created", "created"),
                    ("attempted", "attempted"),
                    ("failed", "failed"),
                    ("passed", "passed"),
                    ("completed", "completed"),
                ],
                default="created",
                max_length=32,
                verbose_name="status",
            ),
        ),
    ]
