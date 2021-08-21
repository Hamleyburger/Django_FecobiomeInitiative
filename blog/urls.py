from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name="blog-home"),
    path('', views.PostListView.as_view(), name="blog-home"),
]
