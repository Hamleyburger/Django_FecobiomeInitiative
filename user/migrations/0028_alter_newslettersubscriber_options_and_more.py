# Generated by Django 4.0 on 2021-12-26 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_auto_20211105_1257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newslettersubscriber',
            options={'verbose_name': 'Newsletter Subscriber (not in use)'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='banned',
            field=models.BooleanField(default=False, verbose_name='Ban user'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='recaptcha_score',
            field=models.FloatField(default=0.0),
        ),
    ]
