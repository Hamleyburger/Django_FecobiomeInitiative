# Generated by Django 3.2.4 on 2021-10-11 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20211010_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_verified',
            field=models.BooleanField("User has completed email verification", default=False)
        ),
    ]
