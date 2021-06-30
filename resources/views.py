from django.shortcuts import render

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

    context = {
        "resources": resources
    }
    return render(request, "resources/resources.html", context)
