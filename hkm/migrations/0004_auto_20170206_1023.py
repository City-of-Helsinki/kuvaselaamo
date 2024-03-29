# Generated by Django 1.10.2 on 2017-02-06 08:23


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0003_productorder_product_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productorder",
            name="crop_image_height",
        ),
        migrations.RemoveField(
            model_name="productorder",
            name="crop_image_width",
        ),
        migrations.AddField(
            model_name="productorder",
            name="original_height",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Original image height"
            ),
        ),
        migrations.AddField(
            model_name="productorder",
            name="original_width",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Original image width"
            ),
        ),
        migrations.AlterField(
            model_name="productorder",
            name="crop_x",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Crop x coordinate from left"
            ),
        ),
        migrations.AlterField(
            model_name="productorder",
            name="crop_y",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Crop y coordinate from top"
            ),
        ),
    ]
