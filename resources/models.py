from django.db import models
from django.db.models.fields import CharField
from django.db.models.signals import pre_save
from django.contrib import messages

# For API calls
import urllib
from .API_helper import get_biorxiv_meta, get_pubmed_meta


class Publication(models.Model):

    doi = models.CharField(max_length=100, unique=True, blank=False)
    link = models.URLField(blank=True)
    title = models.CharField(max_length=200, blank=True)
    authors = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=20, blank=True)

    def __str__(self):
        author = self.authors.split(
            ";")[0] if self.authors else "unknown author"
        if len(author) > 1:
            author = author + " et al."
        year = self.date.year if self.date else "unknown year"
        title = self.title if self.title else "unknown title"

        selfstring = "{} ({}): {}".format(
            author, year, title)
        return selfstring

# Signal for populating fields in Publication - it is recommended to have these in their own file


def get_publication_meta(sender, instance, **kwargs):
    """ Gets and populates publication metadata.\n
    Checks NCBI first, then Bioarchives if publication does not exist in NCBI """
    doi = urllib.parse.quote(instance.doi)
    instance.link = "https://doi.org/" + doi
    try:
        get_pubmed_meta(instance, doi)

    except Exception:
        try:
            get_biorxiv_meta(instance, doi)
        except Exception as e:
            raise e

    print("Creating or updating publication with doi: {}".format(doi))


pre_save.connect(get_publication_meta, sender=Publication)


class Data(models.Model):

    run_accession = models.CharField(max_length=20, unique=True, blank=False)
    sample_type = models.CharField(max_length=50, blank=False)
    location = models.CharField(max_length=100, blank=True)
    farm_name = models.CharField(max_length=50, blank=True)
    farm_size = models.PositiveSmallIntegerField(null=True, blank=True)
    animal = models.CharField(max_length=100, blank=True)
    antibiotics = models.CharField(max_length=100, blank=True)
    host = models.CharField(max_length=20, blank=True)
    age = models.FloatField(null=True, blank=True)
    diet = models.CharField(max_length=100, blank=True)
    sample_date = models.DateField(null=True, blank=True)
    publication = models.ForeignKey(
        Publication, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Data sets"

    def __str__(self):
        farm_name = self.farm_name
        if not farm_name:
            farm_name = "unknown farm"
        selfstring = "<Data {}: {} from {}.>".format(
            self.id, self.sample_type, farm_name)
        return selfstring
