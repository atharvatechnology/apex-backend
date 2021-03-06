# Generated by Django 3.2.13 on 2022-06-16 04:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_user_otp_user_otp_generate_time"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                    "college_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "image",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=accounts.models.Profile.profile_image_upload,
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("faculty", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["user"],
            },
        ),
    ]
