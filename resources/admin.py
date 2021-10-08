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
    fileinput = forms.FileField(widget=forms.FileInput(attrs={'accept':'.txt'}))

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
    list_display = ('authors', "year", "title", 'modified_date')
    form = PublicationForm

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add_from_file/', self.add_from_file, name="publication-add-from-file"),
        ]
        return my_urls + urls

    def add_from_file(self, request):

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
        return render(request, "admin/resources/publication/add_from_file.html", data)




class DataAdmin(admin.ModelAdmin):
    # readonly_fields = ["link"]
    search_fields = ['run_accession', 'bioproject', 'sample_type', 'data_type', 'location',
                     'farm_name', 'animal', 'diet', 'host', 'antibiotics']
    list_display = ('run_accession', 'bioproject', 'sample_type', 'data_type', 'location',
                    'farm_name', 'animal', 'diet', 'FBP_detected', 'host', 'antibiotics', 'farm_size', 'age',
                    'sample_date', 'publication', 'modified_date')
    empty_value_display = 'NA'
    list_filter = ('publication',)


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add_from_file/', self.add_from_file),
        ]
        return my_urls + urls

    def add_from_file(self, request):

        feedback = {}
        if request.method == "POST":
            try:
                feedback = upload_dataset_from_file(request)
                if not feedback.get("field_problems") and not feedback.get("invalid_rows") and not feedback.get("missing_headers") and feedback.get("success"):
                    messages.success(request, "New data sets were succesfully uploaded/updated :-)")
                elif (feedback.get("field_problems") or feedback.get("invalid_rows") or feedback.get("missing_headers")) and feedback.get("success"):
                    messages.warning(request, "Some rows were added/updated, but check feedback to see potential problems")
                elif feedback.get("field_problems") or feedback.get("invalid_rows") or feedback.get("missing_headers") and not feedback.get("success"):
                    messages.error(request, "No rows were added. What went wrong?")
                else:
                    messages.info(request, "...Nothing happened...")
            except Exception as e:
                messages.error(request, "Error: File could not be uploaded")
                raise e("Uploading data set from file caused an error")

        form = CsvImportForm()
        data = {
            "form": form,
            "feedback": feedback
        }
        return render(request, "admin/resources/data/add_from_file.html", data)




# Register your models here.
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Data, DataAdmin)
