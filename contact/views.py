from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm, SubmitDataForm
from user.models import User
from resources.models import resources_meta
from .mailsender import send_mail_to_admin, submit_data_to_admin
from django import http
from django.http import JsonResponse


def home(request):

    form = ContactForm()
    context = {
        "form": form
    }

    if request.method == 'POST':

        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            #recipient = User.objects.filter(id=int(form.cleaned_data["recipient"])).first().email
            recipient = User.objects.filter(
                username='Sapuizait').first().email  # Panos
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            feedback = send_mail_to_admin(
                name, email, [recipient], subject, message)

            if feedback["status"] == "success":
                messages.success(request, feedback["feedback"])
                return http.HttpResponseRedirect(request.path)
            else:
                messages.error(request, feedback["feedback"])
        else:
            messages.error(request, "Could not submit form - invalid")

    return render(request, "contact/contact.html", context)


def submit_data(request):

    form = SubmitDataForm()
    context = {
        "form": form
    }

    if request.method == 'POST':

        form = SubmitDataForm(request.POST, request.FILES)

        if form.is_valid():

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            #recipient = User.objects.filter(id=int(form.cleaned_data["recipient"])).first().email
            recipient = User.objects.filter(
                username='Sapuizait').first().email  # Panos
            affiliation = form.cleaned_data["affiliation"]
            message = form.cleaned_data["message"]
            file = form.cleaned_data["file"]
            data_type = resources_meta.get(form.cleaned_data["database"])["name"]

            feedback = submit_data_to_admin(name, email, affiliation, [recipient], message, file, data_type)

            if feedback["status"] == "success":
                messages.success(request, feedback["feedback"])
                return http.HttpResponseRedirect(request.path)
            else:
                messages.error(request, feedback["feedback"])
        else:
            print(form.errors)
            messages.error(request, form.errors)

    return render(request, "contact/submit_data.html", context)


def fetch_resources_meta(request):
    meta_key = request.POST.get('key')
    requested_dict = resources_meta.get(meta_key)
    txt_path = requested_dict.get("example_file_txt")
    xlsx_path = requested_dict.get("example_file_xlsx")
    print(requested_dict)
    data = {
        'txt_path': txt_path,
        'xlsx_path':  xlsx_path
    }
    return JsonResponse(data)
