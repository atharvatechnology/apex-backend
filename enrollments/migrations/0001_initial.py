# Generated by Django 4.0.4 on 2022-05-25 12:29

from decimal import Decimal

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("exams", "0005_question_section"),
    ]

    operations = [
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "active"),
                            ("inactive", "inactive"),
                            ("pending", "pending"),
                            ("cancelled", "cancelled"),
                        ],
                        default="pending",
                        max_length=32,
                        verbose_name="status",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="creator_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Enrollment",
                "verbose_name_plural": "Enrollments",
            },
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("start_date", models.DateTimeField(verbose_name="start_date")),
                ("end_date", models.DateTimeField(verbose_name="end_date")),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "active"), ("inactive", "inactive")],
                        default="active",
                        max_length=32,
                        verbose_name="status",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="creator_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="updater_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Session",
                "verbose_name_plural": "Sessions",
            },
        ),
        migrations.CreateModel(
            name="ExamThroughEnrollment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "score",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.0"),
                        max_digits=5,
                        verbose_name="score",
                    ),
                ),
                (
                    "status",
                    models.CharField(
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
                (
                    "enrollment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exam_enrolls",
                        to="enrollments.enrollment",
                        verbose_name="enrollment",
                    ),
                ),
                (
                    "exam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exam_enrolls",
                        to="exams.exam",
                        verbose_name="exam",
                    ),
                ),
                (
                    "selected_session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="session_enrolls",
                        to="enrollments.session",
                        verbose_name="exam_session",
                    ),
                ),
            ],
            options={
                "verbose_name": "ExamThroughEnrollment",
                "verbose_name_plural": "ExamThroughEnrollments",
            },
        ),
        migrations.AddField(
            model_name="enrollment",
            name="exams",
            field=models.ManyToManyField(
                blank=True,
                related_name="enrolls",
                through="enrollments.ExamThroughEnrollment",
                to="exams.exam",
                verbose_name="exams",
            ),
        ),
        migrations.AddField(
            model_name="enrollment",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="enrollments",
                to=settings.AUTH_USER_MODEL,
                verbose_name="student",
            ),
        ),
        migrations.AddField(
            model_name="enrollment",
            name="updated_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="updater_%(class)ss",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
