# Generated by Django 4.1 on 2022-09-06 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0014_alter_genome_created_date_alter_genome_expired_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genome',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='genome',
            name='expired_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
