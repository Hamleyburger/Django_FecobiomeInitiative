from django.shortcuts import render
from .models import Data, Publication
from .search_helper import search_data, search_publications


def home(request):

    context = {
        "title": "Resources",
        "query": None,
        "data_hits": ""
    }

    if request.method == "POST":


        query = request.POST.get("searchbar") if request.POST.get("searchbar") else None

        data_hits = len(search_data(query))
        publication_hits = len(search_publications(query))


        context.update(
            {
            "data": Data.objects.all(),
            "publication": Publication.objects.all(),
            "query": query,
            "data_hits": data_hits,
            "publication_hits": publication_hits,
            }
        )
    
    return render(request, "resources/search.html", context)


def data(request, query=None):

    if query:
        results = search_data(query)
    else:
        results = Data.objects.all()

    context = {
        "title": "Data",
        "data": results
    }


    return render(request, "resources/data_datatable.html", context)


def publications(request, query=None):

    if query:
        results = search_publications(query)
    else:
        results = Data.objects.all()

    context = {
        "title": "Publications",
        "publications": results
    }
    return render(request, "resources/publication_datatable.html", context)
