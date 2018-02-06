# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-01-19 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hkm', '0032_multiusage_codes'),
    ]

    operations = [
        migrations.AddField(
            model_name='productordercollection',
            name='order_hash',
            field=models.CharField(blank=True, max_length=1024, null=True, unique=True, verbose_name='Randomized order collection identifier phrase'),
        ),
    ]