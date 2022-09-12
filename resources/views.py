from django.shortcuts import render, redirect
from .models import Data, Genome_version, Publication, Genome
from .search_helper import search_data, search_publications, search_genomes
from django.urls import reverse


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
        genome_hits = len(search_genomes(query))


        context.update(
            {
            "query": query, # will be passed on in a link to the sub resource page
            "data_hits": data_hits,
            "publication_hits": publication_hits,
            "genome_hits": genome_hits
            }
        )
    
    return render(request, "resources/search.html", context)


def data(request, query=None):

    if request.method == "POST":
        query = request.POST.get("searchbar") if request.POST.get("searchbar") else None
        clear = request.POST.get("clear-btn")
        if not clear:
            return redirect('resources-data', query=query)
        else:
            return redirect('resources-data')

    if query:
        results = search_data(query)
    else:
        results = Data.objects.all()

    context = {
        "title": "Sequencing data",
        "data": results,
        "query": query
    }

    return render(request, "resources/data_datatable.html", context)


def publications(request, query=None):

    if request.method == "POST":

        query = request.POST.get("searchbar") if request.POST.get("searchbar") else None
        clear = request.POST.get("clear-btn")
        if not clear:
            return redirect('resources-publications', query=query)
        else:
            return redirect('resources-publications')

    if query:
        results = search_publications(query)
    else:
        results = Publication.objects.all()

    context = {
        "title": "Publications",
        "publications": results,
        "query": query
    }
    return render(request, "resources/publication_datatable.html", context)


def genomes(request, query=None):

    if request.method == "POST":
        query = request.POST.get("searchbar") if request.POST.get("searchbar") else None
        clear = request.POST.get("clear-btn")
        if not clear:
            return redirect('resources-genomes', query=query)
        else:
            return redirect('resources-genomes')


    if query:
        results = search_genomes(query)
    else:
        results = Genome.objects.all()

    context = {
        "title": "Reference genomes",
        "genomes": results, # replace data with genomes
        "query": query,
        "versions": Genome_version.objects.all().order_by('-date')
    }

    return render(request, "resources/genome_datatable.html", context)
