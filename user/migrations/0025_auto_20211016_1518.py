# Generated by Django 3.2.8 on 2021-10-16 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_auto_20211015_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='recaptcha_score',
            field=models.FloatField("Possibility that user is human", default=0.0)
        ),
    ]