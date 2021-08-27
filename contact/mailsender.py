from django.core.mail import EmailMessage
from user.models import User

def sendMail(sender_name, sender_email, recipients: list, subject, message):
    """ Sends anything to the given email addresses """

    try:
        bot_message = 'Sender:\t{}\nE-mail:\t<{}> \n\n{}'.format(sender_name, sender_email, message)
        

        print(bot_message)

        fi_email = EmailMessage(
            subject,
            bot_message,
            'fecobiomeinitiative@gmail.com',
            recipients,
            reply_to=[sender_email],
            headers={'From': '{} <{}>'.format('Fecobiome Initiative', 'fecobiomeinitiative@gmail.com')}
        )

        fi_email.send(fail_silently=False)

        status = "success"
        feedback = "Your message has been sent"
    except Exception as E:
        status = "error"
        feedback = "Message could not be sent"
        print(E)

    return {"status": status, "feedback": feedback}