# Generated by Django 1.10.8 on 2020-11-23 12:11


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0039_collection_is_showcaseable"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="record",
            name="edited_full_res_image",
        ),
        migrations.RemoveField(
            model_name="record",
            name="edited_preview_image",
        ),
    ]
