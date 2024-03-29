# Generated by Django 1.10.2 on 2017-02-28 10:26


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0015_auto_20170223_1101"),
    ]

    operations = [
        migrations.AlterField(
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
