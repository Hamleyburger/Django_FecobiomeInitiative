from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.urls import reverse
from user.mailing_lists import get_unsubscribe_key


def send_newsletter(request, sender_name, recipients: list, subject, html_message):
    """ Sends anything to the given email addresses """

    try:
        for recipient in recipients:

            uid = get_unsubscribe_key(recipient)
            unsibscribe_link = "{}://{}{}".format(request.scheme, request.get_host(), reverse("unsubscribe", kwargs={"unsubscribe_key": uid}))
            plain_text_message = textify(html_message) + "\n\nUnsubscribe with this link: {}".format(unsibscribe_link)
            html_message = html_message + '<p></p><p><a href="{}">Unsubscribe</a></p>'.format(unsibscribe_link)

            mail_from_admin = EmailMultiAlternatives(
                subject,
                plain_text_message,
                sender_name, # technically from_email
                bcc = [recipient],
            )

            mail_from_admin.attach_alternative(html_message, "text/html")
            mail_from_admin.send(fail_silently=True)


    except Exception as E:
        print(E)



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
    text_only = text_only.replace('&nbsp;', '')
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip()
