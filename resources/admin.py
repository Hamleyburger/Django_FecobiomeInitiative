from django.contrib import admin
from .models import Data, Publication


class PublicationAdmin(admin.ModelAdmin):
    readonly_fields = ["title", "authors", "date", "link", "type"]


# Register your models here.
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Data)
