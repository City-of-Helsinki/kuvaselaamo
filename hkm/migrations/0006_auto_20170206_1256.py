# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-06 10:56


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hkm', '0005_productorder_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='product_type',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='hkm.PrintProduct', verbose_name='Product type'),
        ),
    ]
