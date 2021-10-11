# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-18 14:40


import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models

import hkm.models.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_public', models.BooleanField(default=False, verbose_name='Public')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('show_in_landing_page', models.BooleanField(default=False, verbose_name='Show in landing page')),
                ('collection_type', models.CharField(choices=[(b'normal', 'Normal'), (b'favorite', 'Favorite')], default=b'normal', max_length=255, verbose_name='Type')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('record_id', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Finna record ID')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('content', models.TextField(verbose_name='Content')),
                ('is_notification_sent', models.BooleanField(default=False, verbose_name='Notification sent')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrintProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('prize', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prize')),
                ('width', models.IntegerField(verbose_name='Width')),
                ('height', models.IntegerField(verbose_name='Height')),
                ('paper_quality', models.CharField(max_length=255, verbose_name='Paper quality')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('session', models.CharField(max_length=255, verbose_name='Session')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last name')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, verbose_name='Phone number')),
                ('street_address', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Street adress')),
                ('postal_code', models.IntegerField(blank=True, null=True, verbose_name='Postal code')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('record_finna_id', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Finna record ID')),
                ('crop_x', models.IntegerField(blank=True, null=True, verbose_name='Crop x')),
                ('crop_y', models.IntegerField(blank=True, null=True, verbose_name='Crop y')),
                ('crop_width', models.IntegerField(blank=True, null=True, verbose_name='Crop width')),
                ('crop_height', models.IntegerField(blank=True, null=True, verbose_name='Crop height')),
                ('crop_image_width', models.IntegerField(blank=True, null=True, verbose_name='Crop image width')),
                ('crop_image_height', models.IntegerField(blank=True, null=True, verbose_name='Crop image height')),
                ('image_url', models.CharField(blank=True, max_length=2048, null=True, verbose_name='Image URL')),
                ('amount', models.IntegerField(default=1, verbose_name='Amount')),
                ('unit_prize', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Unit prize')),
                ('total_prize', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total prize')),
                ('datetime_confirmed', models.DateTimeField(blank=True, null=True, verbose_name='Confirmed')),
                ('datetime_checkout_started', models.DateTimeField(blank=True, null=True, verbose_name='Checkout started')),
                ('datetime_checkout_ended', models.DateTimeField(blank=True, null=True, verbose_name='Checkout ended')),
                ('is_checkout_successful', models.NullBooleanField(verbose_name='Checkout succesful')),
                ('datetime_order_started', models.DateTimeField(blank=True, null=True, verbose_name='Order started')),
                ('datetime_order_ended', models.DateTimeField(blank=True, null=True, verbose_name='Order ended')),
                ('is_order_successful', models.NullBooleanField(verbose_name='Order succesful')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('record_id', models.CharField(max_length=1024, verbose_name='Finna record ID')),
                ('edited_full_res_image', models.ImageField(blank=True, null=True, upload_to=hkm.models.models.get_collection_upload_path, verbose_name='Edited full resolution image')),
                ('edited_preview_image', models.ImageField(blank=True, null=True, upload_to=hkm.models.models.get_collection_upload_path, verbose_name='Edited preview image')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='hkm.Collection', verbose_name='Collection')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TmpImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('record_id', models.CharField(max_length=1024, verbose_name='Finna record ID')),
                ('record_title', models.CharField(max_length=1024, verbose_name='Title')),
                ('edited_image', models.ImageField(upload_to=hkm.models.models.get_tmp_upload_path, verbose_name='Edited image')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is admin')),
                ('language', models.CharField(choices=[(b'fi', 'Finnish'), (b'en', 'English'), (b'sv', 'Swedish')], default=b'fi', max_length=4, verbose_name='Language')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='productorder',
            name='record',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hkm.Record', verbose_name='Record'),
        ),
        migrations.AddField(
            model_name='productorder',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
