from django.shortcuts import render
from .models import Data, Publication

# Dummy data
resources = [{
    "type": "good data",
    "cows": "brown cows",
    "age": "old",
    "country": "France",
    "farm": "Maggie's Farm",
    "year": "2010"
},
    {
        "type": "different",
        "cows": "red cows",
        "age": "middle aged",
        "country": "Djabouti",
        "farm": "Xadji's Farm",
        "year": "1998"
},
    {
        "type": "happy data",
        "cows": "white cows",
        "age": "young",
        "country": "Canada",
        "farm": "Shithole Farm",
        "year": "2011"
},
    {
        "type": "scribbles",
        "cows": "Herford",
        "age": "Teenagers",
        "country": "France",
        "farm": "Hay Day",
        "year": "2018"
},
    {
        "type": "good data",
        "cows": "brown cows",
        "age": "young",
        "country": "France",
        "farm": "Hay Day",
        "year": "2019"
}
]


def home(request):

    context = {}

    if request.method == "POST":
        context = {
            "data": Data.objects.all(),
            "publication": Publication.objects.all()
        }
    
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
