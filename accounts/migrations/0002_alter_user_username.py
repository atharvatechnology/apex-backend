# Generated by Django 4.0.4 on 2022-05-22 05:41

from django.db import migrations, models

import accounts.validators


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[accounts.validators.PhoneNumberValidator()],
                verbose_name="username",
            ),
        ),
    ]
