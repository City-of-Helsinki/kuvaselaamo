# Generated by Django 1.11.29 on 2022-01-25 23:04

from django.db import migrations
import django.db.models.deletion
import parler.fields


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0044_userprofile_albums_null_is_redundant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaigntranslation",
            name="master",
            field=parler.fields.TranslationsForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="translations",
                to="hkm.Campaign",
            ),
        ),
        migrations.AlterField(
            model_name="pagecontenttranslation",
            name="master",
            field=parler.fields.TranslationsForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="translations",
                to="hkm.PageContent",
            ),
        ),
    ]
