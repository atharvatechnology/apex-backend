# Generated by Django 4.0.4 on 2022-05-24 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="instructor_id",
        ),
        migrations.RemoveField(
            model_name="course",
            name="type_id",
        ),
    ]
