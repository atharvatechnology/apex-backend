# Generated by Django 3.2.13 on 2022-11-24 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bannerad", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bannerad",
            name="description",
        ),
        migrations.RemoveField(
            model_name="bannerad",
            name="title",
        ),
        migrations.AddField(
            model_name="bannerad",
            name="img",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="img"
            ),
        ),
    ]
