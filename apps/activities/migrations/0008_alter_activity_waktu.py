# Generated by Django 4.2 on 2023-05-05 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activities", "0007_alter_activity_waktu"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="waktu",
            field=models.TimeField(default="14:44:24", verbose_name="waktu"),
        ),
    ]
