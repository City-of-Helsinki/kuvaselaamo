# Generated by Django 1.10.8 on 2020-07-21 04:22


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0037_change_deprecated_field_type_for_printer_ip"),
    ]

    operations = [
        migrations.CreateModel(
            name="Showcase",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="Modified"),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Showcase title"),
                ),
                (
                    "show_on_home_page",
                    models.BooleanField(default=True, verbose_name="Show on Home page"),
                ),
                (
                    "albums",
                    models.ManyToManyField(
                        to="hkm.Collection", verbose_name="Selected albums"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
