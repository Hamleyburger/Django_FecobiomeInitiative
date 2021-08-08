from django.shortcuts import render
from .models import Data, Publication


def home(request):

    context = {
        "title": "Resources"
    }

    if request.method == "POST":

        context.update(
            {
            "data": Data.objects.all(),
            "publication": Publication.objects.all()
            }
        )
        print(context)
    
    return render(request, "resources/search.html", context)


def data(request):

    context = {
        "title": "Data",
        "data": Data.objects.all()
    }
    return render(request, "resources/data_datatable.html", context)


def publications(request):

    context = {
        "title": "Publications",
        "publications": Publication.objects.all()
    }
    return render(request, "resources/publication_datatable.html", context)
