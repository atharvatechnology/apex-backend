# Generated by Django 3.2.13 on 2022-10-12 11:10

from django.db import migrations, models

import courses.models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0009_auto_20221012_1417"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="feature_detail",
            field=models.TextField(
                blank=True, null=True, verbose_name="feature_detail"
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="overview_detail",
            field=models.TextField(
                blank=True, null=True, verbose_name="overview_detail"
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=courses.models.Course.course_image_path,
                verbose_name="image",
            ),
        ),
    ]
