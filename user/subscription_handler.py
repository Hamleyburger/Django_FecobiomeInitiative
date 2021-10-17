import csv
import uuid
from user.models import NewsletterSubscriber, Profile
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import uuid


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


def submit_member_request(first_name, last_name, email, affiliation, display_member, recaptcha_score):
    clear_previous_unverified(email)

    user = User(
        username="{} {}".format(first_name, last_name),
        first_name=first_name,
        last_name=last_name,
        email=email,
        )
    user.save()
    profile = Profile(
        display_name="{} {}".format(user.first_name, user.last_name),
        affiliation=affiliation,
        display_member=display_member,
        recaptcha_score=recaptcha_score,
    )

    profile.user = user
    profile.save()
    message = "Dear {}. This is an email".format(user.first_name)
    #user.email_user("Test mail", message, from_email="alma9000@gmail.com")
    return profile
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



def clear_previous_unverified(email):
    """ Checks if there is already an unverified member request and delete it.\n """
    profiles = Profile.objects.filter(user__email=email).all()
    if profiles:
        for profile in profiles:
            if not profile.approved and not profile.user_verified:
                user = profile.user
                print(user)
                user.delete()
    #             now = datetime.now().replace(tzinfo=None) 
    #             difference = now - profile.submission_time.replace(tzinfo=None)
    #             difference_in_minutes = int(difference.total_seconds()) / 60
    #             if not difference_in_minutes > 30:
    #                 return False
    # return True
