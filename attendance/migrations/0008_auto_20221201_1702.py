# Generated by Django 3.2.13 on 2022-12-01 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0007_auto_20221130_1144"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="teacherattendancedetail",
            name="message",
        ),
        migrations.RemoveField(
            model_name="teacherattendancedetail",
            name="remarks",
        ),
        migrations.AddField(
            model_name="teacherattendancedetail",
            name="class_note",
            field=models.TextField(default="dummy", verbose_name="class_note"),
            preserve_default=False,
        ),
    ]
