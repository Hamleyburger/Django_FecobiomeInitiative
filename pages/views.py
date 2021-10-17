from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import Http404
from django.core.validators import validate_email
from user.subscription_handler import subscribe, submit_member_request
from user.file_helpers import resize_crop_image
from contact.mailsender import send_verification_mail
from .forms import ProfileForm, UserForm



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
        raise Http404(
            "Use the newsletter subscription form to subscribe to our newsletter")


def request_membership(request):
    print("request membership accessed")
    if request.method == 'POST':
        # profile_form = ProfileForm(request.POST, request.FILES)

        profile_form = ProfileForm(request.POST, request.FILES)
        user_form = UserForm(request.POST)
        response = {}

        if request.is_ajax():

            if user_form.is_valid() and profile_form.is_valid():

                first_name = user_form.cleaned_data.get("first_name")
                last_name = user_form.cleaned_data.get("last_name")
                email = user_form.cleaned_data.get("email")
                affiliation = profile_form.cleaned_data.get("affiliation")
                display_member = profile_form.cleaned_data.get(
                    "display_member")
                recaptcha_score = profile_form.cleaned_data.get("recaptcha_token")
                profile_picture = profile_form.cleaned_data.get("profile_picture")

                profile = submit_member_request(
                    first_name,
                    last_name,
                    email,
                    affiliation,
                    display_member,
                    recaptcha_score
                )

                if profile_picture:
                    profile_picture = resize_crop_image(profile_picture, 150, str(profile.user.id))
                    profile.profile_picture = profile_picture
                    profile.save()

                send_verification_mail(profile)
                """
                        Send verifikationsemail.
                        - Der skal også stå, hvor mange timer, folk har til at klikke på linket.
                # Når der er sendt en verification email, så ændr formens indholf til at skrive "check your email"
                """

                response = {"success": "Application received. Please check your email for verification."}

            else:
                print(profile_form.errors)
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
