from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from user.models import NewsletterSubscriber
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import Settings, settings


def send_newsletter(request, sender_name, recipients: list, subject, html_message):
    """ Sends anything to the given email addresses """

    sender_email = request.user.email
    sender_name_and_email = "{} <{}>".format(sender_name, sender_email)

    try:
        for recipient in recipients:

            uid = get_unsubscribe_key(recipient)
            unsibscribe_link = "{}://{}{}".format(request.scheme, request.get_host(), reverse("unsubscribe", kwargs={"unsubscribe_key": uid}))
            plain_text_message = textify(html_message) + "\n\nUnsubscribe with this link: {}".format(unsibscribe_link)
            individual_html_message = html_message + '<p></p><p><a href="{}">Unsubscribe</a></p>'.format(unsibscribe_link)

            mail_from_admin = EmailMultiAlternatives(
                subject,
                plain_text_message,
                sender_name, # technically from_email
                bcc = [recipient],
                headers = {'Reply-To': sender_name_and_email}
            )

            mail_from_admin.attach_alternative(individual_html_message, "text/html")
            mail_from_admin.send(fail_silently=True)


    except Exception as E:
        print(E)



def send_mail_to_admin(sender_name, sender_email, recipients: list, subject, message):
    """ Sends anything to the given email addresses """
    sender_email = sender_email.lower()

    try:
        
        fi_email = EmailMessage(
            subject,
            message,
            sender_email,
            recipients,
            reply_to=[sender_email],
            headers={'From': 'FI user: {} <{}>'.format(sender_name, sender_email)},
        )

        fi_email.send(fail_silently=False)

        status = "success"
        feedback = "Your message has been sent"
    except Exception as E:
        status = "error"
        feedback = "Message could not be sent"
        print(E)
    
    # If contacter happens to be a newsletter subscriber, give them a name. Purely for admin friendliness.
    subscriber = NewsletterSubscriber.objects.filter(email=sender_email).first()
    if subscriber:
        if not subscriber.name:
            subscriber.name = sender_name
            subscriber.save()

    return {"status": status, "feedback": feedback}


def submit_data_to_admin(sender_name, email, affiliation, recipients: list, message, file, data_type):
    """ Sends an email with attached file to the given email addresses """

    sender_email = email.lower()
    bot_message = "Name: {}\nAffiliation: {}\nEmail: {}\n\n{}".format(sender_name, affiliation, email, message)

    try:
        
        submission_email = EmailMessage(
            "{} submission request".format(data_type),
            bot_message,
            sender_email,
            recipients,
            reply_to=[sender_email],
            headers={'From': '{} from {} <{}>'.format(sender_name, affiliation, sender_email)},
        )

        submission_email.attach(file.name, file.read())
        submission_email.send(fail_silently=False)

        status = "success"
        feedback = "Your submission has been sent"
    except Exception as E:
        status = "error"
        feedback = "Submission failed"
        print(E)
    
    # If contacter happens to be a newsletter subscriber, give them a name. Purely for admin friendliness.
    subscriber = NewsletterSubscriber.objects.filter(email=sender_email).first()
    if subscriber:
        if not subscriber.name:
            subscriber.name = sender_name
            subscriber.save()

    return {"status": status, "feedback": feedback}

def send_verification_mail(request, profile):
    """ Sends anything to the given email addresses """

    print("preparing to send")
    recipient = profile.user.email
    sender_name_and_email = "{} <{}>".format("Fecobiome Initiative", "noreply")

    uid = profile.registration_key
    verification_link = "{}://{}{}".format(request.scheme, request.get_host(), reverse("validate", kwargs={"registration_key": uid}))
        
    if profile.display_member:
        display = "Let my profile (not including email) be visible in the members' section."
    else:
        display = "Please hide my profile from the members' section."

    if profile.profile_picture:
        has_pic = "Yes"
    else:
        has_pic = "No"

    html_message = "<p>A membership for the Fecobiome Initiative has been requested with the following details using this email.</p>Name: {} {}<br>Affiliation: {}<br>Visibility: {}<br>Profile picture: {}<br><p>To verify that this was you please click the link below.</p>".format(profile.user.first_name, profile.user.last_name, profile.affiliation, display, has_pic)
    plain_text_message = textify(html_message) + "\nConfirmation link: {}".format(verification_link)
    individual_html_message = html_message + '<p></p><p><a href="{}">Confirm that this is your e-mail</a></p>'.format(verification_link)



    try:
        verification_email = EmailMultiAlternatives(
            "Email confirmation",
            plain_text_message,
            sender_name_and_email, # technically from_email
            to = [recipient],
            headers = {'Reply-To': "noreply"}
        )

        verification_email.attach_alternative(individual_html_message, "text/html")
        verification_email.send(fail_silently=False)

    except Exception as E:
        print(E)
    print("sent mail to user, {}".format(profile.user.email))


def get_unsubscribe_key(email):
    subscriber = NewsletterSubscriber.objects.filter(email=email).first()
    key = subscriber.unsubscribe_key
    return key


def textify(html):
    # Remove html tags and continuous whitespaces 
    text_only = strip_tags(html)
    text_only = text_only.replace('&nbsp;', '')
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip()
