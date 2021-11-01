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

    return profile


def clear_previous_unverified(email):
    """ Checks if there is already an unverified member request and delete it.\n """
    profiles = Profile.objects.filter(user__email=email).all()
    if profiles:
        for profile in profiles:
            if not profile.approved and not profile.user_verified:
                user = profile.user
                print(user)
                user.delete()

def verify_profile(profile):
    # Clear previous verified, unapproved profiles (approved profile rank highest in the hierarchy)
    old_profiles = Profile.objects.filter(user__email=profile.user.email, approved=False, user_verified=True).all()
    
    for old_profile in old_profiles:
        user = old_profile.user
        user.delete()

    profile.user_verified = True
    profile.save()

    return profile