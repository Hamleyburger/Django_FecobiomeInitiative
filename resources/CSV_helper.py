from io import TextIOWrapper
from csv import DictReader

from django.contrib import messages
from .models import Data, Publication


def upload_publications(request):

    fieldnames = []
    for field in Publication._meta.fields:
        fieldnames.append(field.name)
    file = request.FILES["fileinput"]
    file_data = TextIOWrapper(file, encoding='utf-8', newline='')
    csv_reader = DictReader(file_data, delimiter="\t")

    for row in csv_reader:
        for key, item in row.items():
            if key == "doi" and item != "":
                try:
                    Publication.objects.update_or_create(doi=item)

                except Exception as e:
                    print("**** Problem with {}".format(item))
                    messages.error(request, e)
                    raise e
