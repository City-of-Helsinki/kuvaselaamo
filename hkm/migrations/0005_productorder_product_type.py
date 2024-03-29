# Generated by Django 1.10.2 on 2017-02-06 10:51


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0004_auto_20170206_1023"),
    ]

    operations = [
        migrations.AddField(
            model_name="productorder",
            name="product_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="hkm.PrintProduct",
                verbose_name="Product type",
            ),
        ),
    ]
