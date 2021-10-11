# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-09-02 08:12


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hkm', '0038_showcase'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='is_showcaseable',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Use in Showcases'),
        ),
    ]
