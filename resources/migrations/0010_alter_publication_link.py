# Generated by Django 4.0 on 2021-12-26 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0009_auto_20211008_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='link',
            field=models.URLField(blank=True, help_text="Links are generated by attaching doi to 'doi.org/' who may choose to redirect"),
        ),
    ]
