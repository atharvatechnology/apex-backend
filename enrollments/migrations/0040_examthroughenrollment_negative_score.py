# Generated by Django 3.2.13 on 2022-08-22 08:58

from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enrollments", "0039_alter_coursethroughenrollment_enrollment"),
    ]

    operations = [
        migrations.AddField(
            model_name="examthroughenrollment",
            name="negative_score",
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal("0.0"),
                max_digits=5,
                verbose_name="Negative Score",
            ),
        ),
    ]
