from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, NewsletterSubscriber

# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

class NewsletterSubscriberAdmin(admin.ModelAdmin):
    # readonly_fields = ["link"]
    list_display = ('email', 'name')



# Re-register UserAdmin
admin.site.register(Profile)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
