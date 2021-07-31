from django.contrib import admin
from .models import Data, Publication
from django.urls import path
from django.shortcuts import render
from django import forms
from csv import DictReader, reader
from io import TextIOWrapper
from .CSV_helper import upload_publications


class CsvImportForm(forms.Form):
    fileinput = forms.FileField()

class PublicationAdmin(admin.ModelAdmin):
    readonly_fields = ["title", "authors", "date", "link", "type"]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('csv_upload/', self.csv_upload),
        ]
        return my_urls + urls

    def csv_upload(self, request):

        if request.method == "POST":
            upload_publications(request)


        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


# Register your models here.
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Data)
