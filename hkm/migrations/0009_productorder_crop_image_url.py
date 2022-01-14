# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-07 08:23


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0008_productorder_form_phase"),
    ]

    operations = [
        migrations.AddField(
            model_name="productorder",
            name="crop_image_url",
            field=models.CharField(
                blank=True, max_length=2048, null=True, verbose_name="Cropped Image URL"
            ),
        ),
    ]
