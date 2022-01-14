# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-08 11:05


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0013_auto_20170208_1222"),
    ]

    operations = [
        migrations.AddField(
            model_name="productorder",
            name="fullimg_original_height",
            field=models.FloatField(
                blank=True, null=True, verbose_name="Full res original image height"
            ),
        ),
        migrations.AddField(
            model_name="productorder",
            name="fullimg_original_width",
            field=models.FloatField(
                blank=True, null=True, verbose_name="Full res original image width"
            ),
        ),
    ]
