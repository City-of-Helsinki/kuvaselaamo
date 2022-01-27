# Generated by Django 1.10.2 on 2017-12-13 10:07


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0031_no_shipment_fee_discount"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaigncode",
            name="use_type",
            field=models.CharField(
                choices=[
                    ("SINGLE_USE", "Kertakäyttöinen"),
                    ("MULTI_USE", "Monikäyttöinen"),
                ],
                db_index=True,
                default="SINGLE_USE",
                max_length=20,
                verbose_name="Käyttö",
            ),
        ),
    ]
