from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm
from user.models import User
from .mailsender import sendMail

def home(request):

    form = ContactForm()

    if request.method == 'POST':

        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            #recipient = User.objects.filter(id=int(form.cleaned_data["recipient"])).first().email
            recipient = User.objects.filter(username='Sapuizait').first().email # Panos
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            feedback = sendMail(name, email, [recipient], subject, message)
            
            if feedback["status"] == "success":
                messages.success(request, feedback["feedback"])
            else:
                messages.error(request, feedback["feedback"])
        else:
            messages.error(request, "Could not submit form - invalid")

    context = {
        "form": form
    }
    
    return render(request, "contact/contact.html", context)


