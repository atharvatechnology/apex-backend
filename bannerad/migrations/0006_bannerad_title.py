# Generated by Django 3.2.13 on 2023-01-10 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bannerad", "0005_bannerad_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="bannerad",
            name="title",
            field=models.CharField(default="Test", max_length=200),
            preserve_default=False,
        ),
    ]
