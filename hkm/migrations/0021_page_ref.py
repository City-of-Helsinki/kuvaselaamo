# Generated by Django 1.10.2 on 2017-07-14 09:11


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0020_translatable_page_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="sent_from",
            field=models.CharField(
                blank=True, max_length=500, null=True, verbose_name="Sent from"
            ),
        ),
    ]
