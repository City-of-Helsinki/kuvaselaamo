# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-12-12 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hkm', '0030_discount_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='free_shipping',
            field=models.BooleanField(default=False, verbose_name='Free shipping'),
        ),
    ]
