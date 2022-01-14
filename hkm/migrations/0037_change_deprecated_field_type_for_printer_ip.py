# Generated by Django 1.10.8 on 2020-06-01 12:47


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0036_campaign_user_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="printer_ip",
            field=models.GenericIPAddressField(
                blank=True, null=True, verbose_name="Museum printer IP"
            ),
        ),
    ]
