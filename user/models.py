from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import uuid
from django.dispatch import receiver
import os



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    display_name = models.CharField(max_length=100)
    contactable = models.BooleanField("Can be contacted", default=False)
    profile_picture = models.ImageField("Profile picture", null=True, blank=True, upload_to="user_profile_pics")
    affiliation = models.CharField(max_length=150, null=True, blank=True)
    approved = models.BooleanField("Approved member", default=False)
    registration_key = models.UUIDField(blank=False, default=uuid.uuid4, unique=True, editable=False)
    display_member = models.BooleanField("Show my profile on the site", default=True)
    user_verified = models.BooleanField("User has completed email verification", default=False)
    submission_time = models.DateTimeField("Time of submission", default=timezone.now)
    recaptcha_score = models.FloatField(default=0.0)


    class Meta:
         verbose_name = "Member profile"

    def __str__(self):
        info = ""
        if self.user.username == "Sapuizait":
            info = "Overlord"
        elif self.user.is_staff:
            info = "Staff"
        elif self.approved:
            info = "Member"
        elif self.user_verified:
            info = "*** PENDING ***"
        else:
            info = "Unverified"
    
        return "{} - {}".format(self.user.username, info)


@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)
        


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, blank=False)
    unsubscribe_key = models.UUIDField(blank=False, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200, blank=True, help_text="This field is not required", verbose_name="Name (if given)")
    class Meta:
         verbose_name = "Newsletter Subscriber"

    def __str__(self):
        return "Subscriber: {}".format(self.email)


