import csv
import uuid
from user.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from contact.mailsender import send_approval_request_to_admin, admin_unsubscribe_notify
import uuid
from sentry_sdk import capture_exception


def cancel_membership(unsubscribe_key=""):
    """ deletes members providing an unsubscribe key/registration key """

    unsubscriber = None

    if unsubscribe_key:
        unsubscribers = Profile.objects.filter(
            registration_key=unsubscribe_key).all()

        for profile in unsubscribers:
            try:
                admin_unsubscribe_notify(profile)
                unsubscriber = profile.user
                unsubscriber.delete()
            except Exception as e:
                capture_exception(e)
                raise e
    

    if unsubscriber:
        unsubscriber = 1

    return unsubscriber


def get_subscribers_emails():
    """ Send newletter to approved, not banned members """
    emails = []

    subscribers = Profile.objects.filter(approved=True, banned=False).all().values('user__email')
    for subscriber in subscribers:
        emails.append(subscriber["user__email"])
    print(emails)

    if settings.DEBUG:
        # if debugging only send stuff to dev
        dev = User.objects.filter(username=settings.HAMLEY).first()
        return [dev.email]
    else:
        return emails


def submit_member_request(first_name, last_name, email, affiliation, display_member, recaptcha_score):
    clear_previous_unverified(email)

    user = User(
        username=uuid.uuid4(),
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
            if not profile.approved and not profile.user_verified: # Don't check for banned because unverified profiles can never be banned
                user = profile.user
                print(user)
                user.delete()

def verify_profile(request, profile):
    # Clear previous verified, unapproved profiles (approved profile rank highest in the hierarchy)
    old_profiles = Profile.objects.filter(user__email=profile.user.email, approved=False, user_verified=True).all()
    
    for old_profile in old_profiles:
        if old_profile.banned:
            return None
        else:
            # Profile's user is banned. Do not verify this one.
            user = old_profile.user
            user.delete()

    profile.user_verified = True
    profile.save()
    send_approval_request_to_admin(request, profile)

    return profile