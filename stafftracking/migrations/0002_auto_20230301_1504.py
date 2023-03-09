# Generated by Django 3.2.13 on 2023-03-01 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stafftracking", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stafftracking",
            name="latitude",
            field=models.DecimalField(decimal_places=13, max_digits=15),
        ),
        migrations.AlterField(
            model_name="stafftracking",
            name="longitude",
            field=models.DecimalField(decimal_places=13, max_digits=15),
        ),
    ]
