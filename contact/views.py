from django.forms.fields import EmailField
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from user.models import User


def home(request):

    form = ContactForm()

    if request.method == 'POST':

        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.keys())
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            #recipient = User.objects.filter(id=int(form.cleaned_data["recipient"])).first().email
            recipient = User.objects.filter(id=2).first().email
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            bot_message = 'Sender:\t{}\nE-mail:\t<{}> \n\n{}'.format(name, email, message)
            

            print(bot_message)

            fi_email = EmailMessage(
                subject,
                bot_message,
                'fecobiomeinitiative@gmail.com',
                [recipient],
                reply_to=[email],
                headers={'From': '{} <{}>'.format('Your friendly neighbourhood Fecobiome bot', 'fecobiomeinitiative@gmail.com')}
            )

            fi_email.send(fail_silently=False)
            # send_mail(
            #     subject=subject,
            #     message=bot_message,
            #     from_email='fecobiomeinitiative@gmail.com',
            #     recipient_list=[recipient],
            #     fail_silently=False,
            #     headers=headers
            # )
            messages.success(request, "Your message has been sent")
        else:
            messages.error(request, "Could not submit form")

    context = {
        "form": form
    }
    
    return render(request, "contact/contact.html", context)


