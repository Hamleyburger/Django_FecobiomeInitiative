from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import Http404
from django.core.validators import validate_email
from user.subscription_handler import subscribe
from user.file_helpers import get_mimetype
from .forms import ProfileForm, UserForm
from django.utils.safestring import mark_safe

def home(request):
    return render(request, "pages/index.html")


def wikiCow(request):
    return render(request, "pages/wikicow.html")

def subscribe_newsletter(request):
    if request.method == 'POST':

        email = request.POST.get('input_email')
        response_data = {}

        try:
            validate_email(email)
            subscribe(email)
            response_data['success'] = 'Subscription successful!'
        except:
            response_data['error'] = 'Invalid email'


        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        raise Http404("Use the newsletter subscription form to subscribe to our newsletter")


def request_membership(request):
    print("request membership accessed")
    if request.method == 'POST':
        # profile_form = ProfileForm(request.POST, request.FILES)

        profile_form = ProfileForm(request.POST, request.FILES)
        user_form = UserForm(request.POST)
        response = {}

        if request.is_ajax():

            if user_form.is_valid() and profile_form.is_valid():
                print("forms are is valid");

                file = request.FILES.get("profile_picture")
                if file:
                    mimetype = get_mimetype(file)
                    if mimetype != "image/png" and mimetype != "image/jpeg":
                        return HttpResponse(
                            json.dumps({ "error": "Profile picture must be .jpeg or .png" }),
                            content_type="application/json"
                        )

                #If file was invalid, function has already been returned.
                # Save file somewhere when we have a user id

                user_form = user_form.clean()
                profile_form = profile_form.clean()



                """
                # UpdatecreateUser
                Check if user with email exists:
                    CreateUser: Lav en ny (midlertidig) user med id. Hvis anden user med email eksisterer, så skrot den gamle plus billede hvis denne verificeres.
                    # Gør noget med billede
                    Resize billede og crop ligesom i minimalepar.
                    Gem billede i media med brugerens id som filnavn.
                        Tjek om der er nogen brugere, der ikke er verificeret, hvor forskellen på nu og submission time er mere end (1 time?)
                        - I emailen skal der enten stå, om man vil lave en ny, og hvis der allerede findes en entry vil den blive erstattes af den nye.
                        - Der skal også stå, hvor mange timer, folk har til at klikke på linket.
                # Når der er sendt en verification email, så ændr formens indholf til at skrive "check your email"
                """





                response = {"success": "Application received. Please check your email for verification."}


            else:

                response = { "error": "Something went wrong" }
                for key, value in profile_form.errors.items():
                    response = { "error": value }
                for key, value in user_form.errors.items():
                    response = { "error": value }


        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )
    else:
        raise Http404("Use the membership registration form to register as a member")