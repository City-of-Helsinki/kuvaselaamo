# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-07 11:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import hkm.models.campaigns
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('hkm', '0026_hkm_museum_printer_credentials'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(blank=True, db_index=True, max_length=64, null=True)),
                ('status', models.CharField(choices=[(b'DISABLED', 'Ei k\xe4yt\xf6ss\xe4'), (b'ENABLED', 'Aktiivinen')], db_index=True, default=b'ENABLED', max_length=20, verbose_name='Tila')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now_add=True)),
                ('usable_from', models.DateField(blank=True, null=True, verbose_name='Alkup\xe4iv\xe4m\xe4\xe4r\xe4')),
                ('usable_to', models.DateField(blank=True, null=True, verbose_name='Loppup\xe4iv\xe4m\xe4\xe4r\xe4')),
                ('usage_type', models.CharField(choices=[(b'SINGLE_USE', 'Kertak\xe4ytt\xf6inen'), (b'CODELESS', 'Kooditon')], default=b'SINGLE_USE', max_length=20, verbose_name='Tyyppi')),
                ('module', models.CharField(blank=True, max_length=128, verbose_name='Kampanjamoduuli')),
                ('mutex_group', models.CharField(blank=True, help_text='Mik\xe4li asetettu, useampaa saman ryhm\xe4n kampanjaa ei voi k\xe4ytt\xe4\xe4 yhdess\xe4 tilauksessa', max_length=32, verbose_name='Yhteisk\xe4ytt\xf6estoryhm\xe4')),
                ('percentage_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Prosentuaalinen alennus')),
                ('fixed_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Absoluuttinen alennus (veroton)')),
            ],
            options={
                'verbose_name': 'kampanja',
                'verbose_name_plural': 'kampanjat',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model, hkm.models.campaigns._UsageMixin),
        ),
        migrations.CreateModel(
            name='CampaignCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=40)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[(b'DISABLED', 'Ei k\xe4yt\xf6ss\xe4'), (b'ENABLED', 'Aktiivinen')], db_index=True, default=b'ENABLED', max_length=20, verbose_name='Tila')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaign_codes', to='hkm.Campaign', verbose_name='Kampanja')),
            ],
            options={
                'verbose_name': 'kampanjakoodi',
                'verbose_name_plural': 'kampanjakoodit',
            },
            bases=(models.Model, hkm.models.campaigns._UsageMixin),
        ),
        migrations.CreateModel(
            name='CampaignTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(blank=True, max_length=256, verbose_name='Nimi')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='hkm.Campaign')),
            ],
            options={
                'managed': True,
                'db_table': 'hkm_campaign_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'kampanja Translation',
            },
        ),
        migrations.AlterUniqueTogether(
            name='campaigntranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]