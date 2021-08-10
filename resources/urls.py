from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="resources-home"),
    path('data/', views.data, name="resources-data"),
    path('data/<str:query>/', views.data, name="resources-data"),
    path('publications/', views.publications, name="resources-publications"),
    path('publications/<str:query>/', views.publications, name="resources-publications"),
]
