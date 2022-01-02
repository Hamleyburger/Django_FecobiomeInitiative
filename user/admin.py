from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'user_email', 'recaptcha_score', 'submission_time')

    @admin.display(description='User email')
    def user_email(self, obj):
        return ("%s - \n(Email can only be edited from the 'User' page.)" % (obj.user.email))
    
    fields = ('user', 'display_name', 'affiliation', 'user_email', 'profile_picture', 'display_member', 'approved', 'user_verified', 'banned', 'recaptcha_score', 'submission_time')



# Re-register UserAdmin
admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

