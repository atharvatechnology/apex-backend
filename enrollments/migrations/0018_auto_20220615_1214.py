# Generated by Django 3.2.13 on 2022-06-15 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enrollments", "0017_auto_20220615_1106"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="coursethroughenrollment",
            name="joining_date",
        ),
        migrations.AlterField(
            model_name="coursethroughenrollment",
            name="course_status",
            field=models.CharField(
                choices=[
                    ("new", "new"),
                    ("initiated", "initiated"),
                    ("on-hold", "on-hold"),
                    ("progress", "progress"),
                    ("declined", "declined"),
                    ("final phase", "final phase"),
                    ("completed", "completed"),
                ],
                default="new",
                max_length=50,
            ),
        ),
    ]
