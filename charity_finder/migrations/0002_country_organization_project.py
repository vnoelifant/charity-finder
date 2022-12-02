# Generated by Django 4.1.3 on 2022-12-02 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("charity_finder", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("country_code", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=200, null=True)),
                ("org_id", models.IntegerField(blank=True, default=0, null=True)),
                ("mission", models.TextField(blank=True, default="", null=True)),
                (
                    "active_projects",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                (
                    "total_projects",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                ("ein", models.CharField(blank=True, max_length=200, null=True)),
                ("logo_url", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "address_line1",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "address_line2",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=200, null=True)),
                ("state", models.CharField(blank=True, max_length=200, null=True)),
                ("postal", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "country_home",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("url", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "countries",
                    models.ManyToManyField(
                        related_name="countries", to="charity_finder.country"
                    ),
                ),
                (
                    "themes",
                    models.ManyToManyField(
                        related_name="themes", to="charity_finder.theme"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "org",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="charity_finder.organization",
                    ),
                ),
            ],
        ),
    ]