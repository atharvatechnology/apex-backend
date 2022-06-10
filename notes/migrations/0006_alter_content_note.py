# Generated by Django 3.2.13 on 2022-06-08 05:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0005_rename_course_id_note_course"),
    ]

    operations = [
        migrations.AlterField(
            model_name="content",
            name="note",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contents",
                to="notes.note",
            ),
        ),
    ]