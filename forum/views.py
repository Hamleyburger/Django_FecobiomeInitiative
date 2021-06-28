from django.shortcuts import render

from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>You're home in the forum</h1>")
