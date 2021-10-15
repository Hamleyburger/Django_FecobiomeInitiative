import csv
import uuid
from user.models import NewsletterSubscriber, Profile
from django.contrib.auth.models import User



def subscribe(email):
    """ adds any string to mailing list so make sure to validate first?\n
    Also adds an unsubscribe key that can be used in an unsubscribe link """
    email = email.lower()

    if not NewsletterSubscriber.objects.filter(email=email).first():
        print("Subscriber is new")
        subscriber = NewsletterSubscriber(email=email)
        subscriber.save()
    else:
        print("subscirber exists")


def unsubscribe(unsubscribe_key="", unsubscribe_email=""):
    """ for removing subscriber with an unsubscribe link providing an unsubscribe key """
    print("Unsubscribe called")

    unsubscriber = None

    if unsubscribe_key:
        unsubscriber = NewsletterSubscriber.objects.filter(
            unsubscribe_key=unsubscribe_key)

    if unsubscribe_email:
        unsubscriber = NewsletterSubscriber.objects.filter(
            email=unsubscribe_email.lower())

    if unsubscriber:
        unsubscriber.delete()
        unsubscriber = 1

    return unsubscriber


def get_subscribers_emails():
    emails = []
    subscribers = NewsletterSubscriber.objects.all().values('email')
    for subscriber in subscribers:
        emails.append(subscriber["email"])
    print(emails)
    return emails


def get_unsubscribe_key(email):
    subscriber = NewsletterSubscriber.objects.filter(email=email).first()
    key = subscriber.unsubscribe_key
    return key


def submit_member_request(first_name, last_name, email, affiliation, display_member, profile_picture):
    can_submit(email)
    # create user and profile object
    # if there is no approved, make new pending, else:
    #   if thre is a validated unapproved:
    #
    #   check if there is a pending
    #   if there is not a pending, make a pending
    #   if there is a pending, give feedback to first verify the pending "you already have a pending verification" and do nothing
    #   if there
    # save
    # save image and link to profile
    pass


def can_submit(email):
    """ Checks if user with is email is allowed to submit an unverified member request """
    profiles = Profile.objects.filter(user__email=email).all()
    if profiles:
        for profile in profiles:
            print("exists: {}".format(profile))
            print("submission time: {}".format(profile.submission_time))
    else:
        print("no profile with this email: {}".format(email))
