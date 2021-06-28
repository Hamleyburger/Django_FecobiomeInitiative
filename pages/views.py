from django.shortcuts import render

from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Home page</h1>")


def wikiCow(request):
    return HttpResponse("<h1>WikiCow about cows</h1>")
