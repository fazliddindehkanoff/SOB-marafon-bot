# Generated by Django 5.2.2 on 2025-06-19 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0008_telegramuser_chosen_tarif"),
    ]

    operations = [
        migrations.AddField(
            model_name="marathontarif",
            name="private_group_link",
            field=models.CharField(default="", max_length=150),
        ),
    ]
