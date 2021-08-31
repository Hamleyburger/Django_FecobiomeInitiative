import csv
import uuid
from user.models import NewsletterSubscriber



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
