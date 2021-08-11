from django.shortcuts import render
from .models import Post


def home(request):

    context = {
        "posts": Post.objects.order_by('-created_date').all()
    }
    return render(request, "blog/news.html", context)
