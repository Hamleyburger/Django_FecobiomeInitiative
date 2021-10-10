from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="contact-home"),
    path('submit-data/', views.submit_data, name="contact-submit-data"),
    path('fetch_resources_meta/', views.fetch_resources_meta,
         name='fetch_resources_meta'),
]
