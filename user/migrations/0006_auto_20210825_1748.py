# Generated by Django 3.2.4 on 2021-08-25 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_profile_contactable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='mailing_lists',
        ),
        migrations.AddField(
            model_name='profile',
            name='contactable',
            field=models.BooleanField(default=False, verbose_name='Can be contacted'),
        ),
        migrations.DeleteModel(
            name='MailingList',
        ),
    ]
