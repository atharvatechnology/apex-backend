# Generated by Django 3.2.13 on 2022-11-28 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bannerad", "0003_alter_bannerad_img"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bannerad",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "BannerAd",
                "verbose_name_plural": "BannerAds",
            },
        ),
    ]
