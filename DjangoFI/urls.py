"""DjangoFI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .admin_views import NewsletterView, MemberView, approve_members
from .views import UnsubscribeFormView, ValidateFormView

urlpatterns = [
    path('admin/write-newsletter/', NewsletterView.as_view(), name="admin-write-newsletter"),
    path('admin/approve-members/', approve_members, name="admin-approve-members"),
    path('admin/', admin.site.urls),
    path('', include("pages.urls")),
    path('news/', include("blog.urls")),
    path('resources/', include("resources.urls")),
    path('contact/', include("contact.urls")),
    path('cancel-membership/<uuid:unsubscribe_key>/', UnsubscribeFormView.as_view(),  name="unsubscribe"),
    path('cancel-membership/', UnsubscribeFormView.as_view(), name="unsubscribe"),
    path('validate/<uuid:registration_key>/', ValidateFormView.as_view(),  name="validate")

]
# add static url with media and root options?
# From this SO post: https://stackoverflow.com/questions/36280056/page-not-found-404-django-media-files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Fecobiome Initiative Admin"
admin.site.site_title = "FI Admin"
