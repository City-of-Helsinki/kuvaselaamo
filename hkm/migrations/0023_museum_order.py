# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-24 12:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hkm', '0022_museum_only_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOrderCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderer_name', models.CharField(max_length=255, verbose_name="Orderer's name")),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Total order price')),
                ('sent_to_print', models.BooleanField(default=False, verbose_name='Sent to printer')),
            ],
        ),
        migrations.AddField(
            model_name='productorder',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_orders', to='hkm.ProductOrderCollection'),
        ),
    ]
