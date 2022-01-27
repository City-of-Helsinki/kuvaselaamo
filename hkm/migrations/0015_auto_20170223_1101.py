# Generated by Django 1.10.2 on 2017-02-23 09:01


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0014_auto_20170208_1305"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productorder",
            name="product_type",
            field=models.ForeignKey(
                blank=True,
                default=6,
                on_delete=django.db.models.deletion.CASCADE,
                to="hkm.PrintProduct",
                verbose_name="Product type",
            ),
        ),
    ]
