# Generated by Django 3.2.13 on 2022-11-25 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("counseling", "0006_alter_counseling_note"),
    ]

    operations = [
        migrations.AlterField(
            model_name="counseling",
            name="note",
            field=models.TextField(default="This is note", verbose_name="note"),
            preserve_default=False,
        ),
    ]
