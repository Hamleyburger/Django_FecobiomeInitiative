from django.contrib import admin
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    # readonly_fields = ["link"]
    
    search_fields = ['title', 'body', 'author']
    list_display = ('title', 'html_stripped_body', 'author', 'created_date', 
    #'image_tag'
    )
    list_filter = ('author',)
    fields = ['title', 'body'
    #, 'image'
    ]
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(Post, PostAdmin)



