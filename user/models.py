from django.db import models
from django.contrib.auth.models import User
import uuid



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    contactable = models.BooleanField("Can be contacted", default=False)

    def __str__(self):
        return "{} - Profile".format(self.user.username)

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, blank=False)
    unsubscribe_key = models.UUIDField(blank=False, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200, blank=True, help_text="This field is not required", verbose_name="Name (if given)")
    class Meta:
         verbose_name = "Newsletter Subscribers"

    def __str__(self):
        return "Subscriber: {}".format(self.email)