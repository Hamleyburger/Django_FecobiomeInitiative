# Generated by Django 3.2.4 on 2021-10-10 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_profile_unregister_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='display_member',
            field=models.BooleanField("Display member on site", default=True)
        ),
    ]
