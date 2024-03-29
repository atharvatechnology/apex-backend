# Generated by Django 3.2.13 on 2022-06-07 09:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendance",
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
                ("date", models.DateTimeField(verbose_name="Attendance date")),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="creator_attendances",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="updater_attendances",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendances",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="StudentAttendance",
            fields=[
                (
                    "attendance_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="attendance.attendance",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("attendance.attendance",),
        ),
        migrations.CreateModel(
            name="TeacherAttendance",
            fields=[
                (
                    "attendance_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="attendance.attendance",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("attendance.attendance",),
        ),
        migrations.CreateModel(
            name="TeacherAttendanceDetail",
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
                    "number_of_peroid",
                    models.IntegerField(verbose_name="Number of peroid"),
                ),
                ("message", models.TextField(verbose_name="Message")),
                ("remarks", models.TextField(verbose_name="Remarks")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("request", "Request"),
                            ("approve", "Approve"),
                            ("reject", "Reject"),
                            ("clarification", "Clarification"),
                        ],
                        default="draft",
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="creator_teacherattendancedetails",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="updater_teacherattendancedetails",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "teacher_attendance",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="details",
                        to="attendance.teacherattendance",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
