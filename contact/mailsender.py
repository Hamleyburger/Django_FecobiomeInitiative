from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from user.models import User
from django.core.mail import send_mail
import re
from django.utils.html import strip_tags

def send_mail_from_admin(sender_name, recipients: list, subject, html_message):
    """ Sends anything to the given email addresses """
    print("sending to ")
    print(recipients)
    try:
        plain_text_message = textify(html_message)

        mail_from_admin = EmailMultiAlternatives(
            subject,
            plain_text_message,
            sender_name, # technically from_email
            bcc = recipients,
        )

        mail_from_admin.attach_alternative(html_message, "text/html")
        mail_from_admin.send(fail_silently=True)


        status = "success"
        feedback = "Your message has been sent"

    except Exception as E:
        status = "error"
        feedback = "Message could not be sent"
        print(E)

    return {"status": status, "feedback": feedback}

def send_mail_to_admin(sender_name, sender_email, recipients: list, subject, message):
    """ Sends anything to the given email addresses """

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

    return {"status": status, "feedback": feedback}

def textify(html):
    # Remove html tags and continuous whitespaces 
    text_only = strip_tags(html)
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip()