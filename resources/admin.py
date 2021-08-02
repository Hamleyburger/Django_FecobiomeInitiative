from django.contrib import admin, messages
from .models import Data, Publication
from django.urls import path
from django.shortcuts import render
from django import forms
from csv import DictReader
from io import TextIOWrapper
from .upload_helper import upload_publications_from_file, upload_dataset_from_file


# This form is for bulk importing publications
class CsvImportForm(forms.Form):
    fileinput = forms.FileField()

# This form makes all publication fields required
class PublicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['authors'].required = True
        self.fields['date'].required = True
        self.fields['type'].required = True

    class Meta:
        model = Publication
        fields = '__all__'

class PublicationAdmin(admin.ModelAdmin):
    readonly_fields = ["link"]

    form = PublicationForm

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('csv_upload/', self.csv_upload),
        ]
        return my_urls + urls

    def csv_upload(self, request):

        failed_uploads = []
        if request.method == "POST":
            failed_uploads = upload_publications_from_file(request)
            if not failed_uploads:
                messages.success(request, "All publications were succesfully uploaded/updated :-)")


        form = CsvImportForm()
        data = {
            "form": form,
            "failed_uploads": failed_uploads
        }
        return render(request, "admin/resources/publication/csv_upload.html", data)




class DataAdmin(admin.ModelAdmin):
    # readonly_fields = ["link"]
    search_fields = ['run_accession', 'sample_type', 'location', 'farm_name']

    #form = PublicationForm

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('csv_upload/', self.csv_upload),
        ]
        return my_urls + urls

    def csv_upload(self, request):

        feedback = []
        if request.method == "POST":
            feedback = upload_dataset_from_file(request)
            if not feedback.get("field_problems") and not feedback.get("invalid_rows") and not feedback.get("missing_headers") and feedback.get("success"):
                messages.success(request, "New data sets were succesfully uploaded/updated :-)")
            elif feedback.get("field_problems") or feedback.get("invalid_rows") or feedback.get("missing_headers") and feedback.get("success"):
                messages.warning(request, "Some rows were added, but check feedback to see any problems that occurred")
            elif feedback.get("field_problems") or feedback.get("invalid_rows") or feedback.get("missing_headers") and not feedback.get("success"):
                messages.error(request, "No rows were added. What went wrong?")
            else:
                messages.info(request, "All rows seem to already exist with these run_accessions")


        form = CsvImportForm()
        data = {
            "form": form,
            "feedback": feedback
        }
        return render(request, "admin/resources/data/csv_upload.html", data)




# Register your models here.
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Data, DataAdmin)
