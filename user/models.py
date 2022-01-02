from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import uuid
from django.dispatch import receiver
import os
from django.conf import settings



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    display_name = models.CharField(max_length=100)
    contactable = models.BooleanField("Can be contacted", default=False)
    profile_picture = models.ImageField("Profile picture", null=True, blank=True, upload_to="user_profile_pics")
    affiliation = models.CharField(max_length=150, null=True, blank=True)
    registration_key = models.UUIDField(blank=False, default=uuid.uuid4, unique=True, editable=False)
    display_member = models.BooleanField("Show my profile on the site", default=True)
    submission_time = models.DateTimeField("Time of submission", default=timezone.now)
    recaptcha_score = models.FloatField(default=0.0)
    approved = models.BooleanField("Approved member", default=False)
    user_verified = models.BooleanField("User has completed email verification", default=False)
    banned = models.BooleanField("Ban user", default=False)


    class Meta:
         verbose_name = "Member profile"

    def __str__(self):
        info = ""
        if self.user.username == settings.PANOS:
            info = "Overlord"
        elif self.banned:
            info = "! BANNED !"
        elif self.user.is_staff:
            info = "Staff"
        elif self.approved:
            info = "Member"
        elif self.user_verified:
            info = "*** PENDING ***"
        else:
            info = "Unverified"
    
        return "{} - {}".format(self.display_name, info)


@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)
        


