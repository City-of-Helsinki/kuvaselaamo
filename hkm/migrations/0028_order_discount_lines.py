# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-16 14:32


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hkm', '0027_discounts'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOrderDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_used', models.CharField(max_length=255, null=True, verbose_name='Used discount code')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hkm.Campaign')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hkm.ProductOrderCollection')),
            ],
        ),
    ]
