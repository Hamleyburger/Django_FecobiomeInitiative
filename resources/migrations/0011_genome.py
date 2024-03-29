# Generated by Django 4.1 on 2022-09-04 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0010_alter_publication_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=100, unique=True)),
                ('closest_rel_alt_name', models.CharField(max_length=100, unique=True)),
                ('phyl_class', models.CharField(max_length=100)),
                ('original_sample', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('publication', models.CharField(max_length=100)),
                ('dRep_secondary_cluster', models.CharField(max_length=100)),
                ('checkm_completeness', models.DecimalField(decimal_places=2, max_digits=5)),
                ('checkm_contamination', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mean_contig_read_coverage', models.DecimalField(decimal_places=2, max_digits=6)),
                ('dRep_set_of_MAGs', models.BooleanField()),
                ('source', models.CharField(max_length=100)),
                ('latest_doi', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('expired_date', models.DateTimeField(blank=True)),
            ],
        ),
    ]
