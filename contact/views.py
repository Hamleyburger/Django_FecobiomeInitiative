from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import ContactForm, SubmitDataForm
from user.models import User
from resources.models import resources_meta
from .mailsender import send_mail_to_admin, submit_data_to_admin
from django import http
from django.http import Http404, JsonResponse
from django.conf import settings


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

            if settings.DEBUG:
                recipient = User.objects.filter(
                username=settings.HAMLEY).first().email  # Dev mail
            else:
                recipient = User.objects.filter(
                username=settings.PANOS).first().email  # Admin mail
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
                username=settings.PANOS).first().email  # Panos
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

@require_http_methods(["POST"])
def fetch_resources_meta(request):
    # Makes the downloadable excel and txt example files be the correct
    # resource format (data/publication) in the submit-data page.
    meta_key = request.POST.get('key')
    requested_dict = resources_meta.get(meta_key)
    txt_path = requested_dict.get("example_file_txt")
    xlsx_path = requested_dict.get("example_file_xlsx")

    data = {
        'txt_path': txt_path,
        'xlsx_path':  xlsx_path
    }
    return JsonResponse(data)

