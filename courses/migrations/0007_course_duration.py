# Generated by Django 3.2.13 on 2022-08-16 09:59

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0006_auto_20220816_1542"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="duration",
            field=models.DurationField(
                default=datetime.timedelta, verbose_name="Duration"
            ),
            preserve_default=False,
        ),
    ]
