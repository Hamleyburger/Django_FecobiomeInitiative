from django.db import models
from django.db.models.fields import CharField
from django.db.models.signals import pre_save
from django.utils.html import mark_safe

# For API calls
import urllib
import requests
from .API_helpers.publications import get_biorxiv_meta, get_pubmed_meta, clean_doi


class Publication(models.Model):

    doi = models.CharField(max_length=100, unique=True, blank=False)
    link = models.URLField(
        blank=True, help_text="Links are generated automatically from doi if one exists")
    title = models.CharField(max_length=200, blank=True)
    authors = models.TextField(
        blank=True, help_text="First author must be first and names must be separated with semicolon ';'. <br>Example: <br>'Sapountzis, P.; Segura, A.; Desvaux, M.; Forano, E.'")
    date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=20, blank=True, choices=[(
        "peer-reviewed", "peer-reviewed"), ("preprint", "preprint")])
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def author_et_al(self):
        author = self.authors.split(
            ";")[0] if self.authors else "unknown author"
        if len(author) > 1:
            author = author + " et al."
        return author


    def year(self):
        year = self.date.year if self.date else "unknown year"
        return year

    def __str__(self):
        author = self.author_et_al()
        year = self.year()
        title = "\n{}...".format(self.title[0:20]) if self.title else "\nunknown title"

        selfstring = "{} ({}): {}".format(
            author, year, title)
        return selfstring

# Signal for populating fields in Publication - it is recommended to have these in their own file


def get_publication_meta(sender, instance, **kwargs):
    """ Gets and populates publication metadata.\n
    Checks NCBI first, then Bioarchives if publication does not exist in NCBI """

    # doi needs to be cleaned before input and before any given check
    doi = clean_doi(instance.doi)
    instance.doi = doi
    url_encoded_doi = urllib.parse.quote(doi)
    link = "https://doi.org/" + url_encoded_doi
    if requests.get(link).status_code == 200:
        instance.link = link

    if not instance.title:
        print("save seems to be called by uploading file")

        # Try getting metadata from various APIs

        try:
            get_pubmed_meta(instance, url_encoded_doi)

        except Exception:
            try:
                get_biorxiv_meta(instance, url_encoded_doi)
            except Exception as e:
                raise e

    print("Creating or updating publication with doi: {} ".format(instance.doi))


pre_save.connect(get_publication_meta, sender=Publication)


class Data(models.Model):

    run_accession = models.CharField(max_length=20, unique=True, blank=False)
    sample_type = models.CharField(max_length=50, blank=False)
    data_type = models.CharField(max_length=20, blank=False)
    location = models.CharField(max_length=100, blank=True)
    farm_name = models.CharField(max_length=50, blank=True)
    farm_size = models.PositiveSmallIntegerField(null=True, blank=True)
    animal = models.CharField(max_length=100, blank=True)
    antibiotics = models.CharField(max_length=100, blank=True)
    host = models.CharField(max_length=20, blank=True)
    age = models.FloatField(null=True, blank=True)
    diet = models.CharField(max_length=100, blank=True)
    target_region_16s = models.CharField(max_length=100, blank=True)
    no_of_samples = models.PositiveSmallIntegerField(null=True, blank=True)
    no_of_animals = models.PositiveSmallIntegerField(null=True, blank=True)
    sample_date = models.DateField(null=True, blank=True)
    publication = models.ForeignKey(
        Publication, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Data sets"

    def __str__(self):
        farm_name = self.farm_name
        location = self.location
        place = "unknown location"
        if farm_name and location:
            place = farm_name + ", " + location
        elif farm_name and not location:
            place = farm_name + ", unknown location"
        elif location:
            place = location
        selfstring = "run_acc: '{}', type '{}\' from {}.".format(
            self.run_accession, self.sample_type, place)
        return selfstring


