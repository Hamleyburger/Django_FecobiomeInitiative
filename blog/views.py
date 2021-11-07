from django.shortcuts import render
from .models import Post
from django.views.generic.list import ListView



class PostListView(ListView):

    model = Post
    context_object_name = "posts"
    ordering = '-created_date'
    paginate_by = 5
    paginate_orphans = 2
    template_name = "blog/news.html"
