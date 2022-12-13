# Generated by Django 4.1.3 on 2022-12-13 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charity_finder", "0005_alter_project_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="funding",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=13, null=True
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="goal",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=13, null=True
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="goal_remaining",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=13, null=True
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="latitude",
            field=models.DecimalField(decimal_places=2, max_digits=13),
        ),
        migrations.AlterField(
            model_name="project",
            name="longitude",
            field=models.DecimalField(decimal_places=2, max_digits=13),
        ),
    ]