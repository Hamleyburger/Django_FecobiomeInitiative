from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="pages-home"),
    path('wiki-cow/', views.wikiCow, name="pages-wikicow"),
    path('subscribe-to-newsletter/', views.subscribe_newsletter, name="subscribe-to-newsletter"),
    path('request-membership/', views.request_membership, name="request-membership"),
]
