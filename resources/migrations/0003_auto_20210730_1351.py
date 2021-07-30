# Generated by Django 3.2.4 on 2021-07-30 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_publication_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='authors',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='link',
            field=models.URLField(blank=True),
        ),
    ]
