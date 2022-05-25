# Generated by Django 4.0.4 on 2022-05-25 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exams", "0004_remove_examtemplate_max_score_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="section",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sections",
                to="exams.section",
                verbose_name="section",
            ),
            preserve_default=False,
        ),
    ]