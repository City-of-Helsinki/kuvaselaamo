# Generated by Django 1.10.2 on 2017-02-28 10:57


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0016_auto_20170228_1226"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productorder",
            name="order_hash",
            field=models.CharField(
                blank=True,
                max_length=1024,
                null=True,
                unique=True,
                verbose_name="Randomized order identifier phrase",
            ),
        ),
    ]
