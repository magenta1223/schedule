# Generated by Django 4.1.3 on 2022-12-18 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0003_private_remove_baseevent_cls_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="private",
            name="content",
            field=models.TextField(default="", verbose_name="desc"),
        ),
    ]
