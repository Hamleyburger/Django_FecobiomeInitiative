# Generated by Django 3.2.4 on 2021-10-10 18:14

from django.db import migrations, models
from user.models import Profile




class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_profile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(verbose_name="Profile picture", null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='approved',
            field=models.BooleanField("Approved member", default=False),
        ),
    ]











