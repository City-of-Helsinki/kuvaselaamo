# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-02 09:40


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0024_hkm_museum_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="printer_presets",
            field=models.TextField(
                default=b'{"api-poster-gloss-40x30": 0, "api-poster-gloss-A4-horizontal": 0, "api-poster-50x70": 0, "api-poster-gloss-A4": 0, "api-poster-70x50": 0, "api-poster-gloss-30x40": 0}',
                verbose_name="Tulostimen presetit",
            ),
        ),
    ]
