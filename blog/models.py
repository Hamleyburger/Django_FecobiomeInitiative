from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.html import format_html
from datetime import datetime
from django.utils.html import mark_safe
from django.db.models.signals import pre_save

# Create your models here.


class Post(models.Model):

    title = models.CharField(max_length=70, blank=False,
                             help_text="Title or one-liner news")
    body = RichTextField(
        blank=True, null=True, help_text="In case you want to elaborate")
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/",
                              help_text=mark_safe("Make sure the image is cropped to be square. You can use <a href='https://croppola.com/' target='_blank'>this external cropping tool</a>"))
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    @property
    def html_stripped_body(self):
        return format_html(self.body)
    html_stripped_body.fget.short_description = "body"

    @property
    def image_tag(self):
        return mark_safe('<img src="/media/{}" style="max-width: 100%; max-height: 120px;" />'.format(self.image))
    image_tag.fget.short_description = 'image'

    def __str__(self):
        date = datetime.strftime(self.created_date, "%-d/%-m-%y")
        abbreviated_string = self.title[0:20]
        string = "{}: {}".format(date, abbreviated_string)
        return string


def clear_body(sender, instance, **kwargs):
    """ Empties empty body so it returns None/"" """

    # doi needs to be cleaned before input and before any given check
    if instance.body == " ":
        instance.body == None

pre_save.connect(clear_body, sender=Post)
