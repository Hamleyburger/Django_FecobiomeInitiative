from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import Http404
from django.core.validators import validate_email
from user.subscription_handler import submit_member_request
from user.file_helpers import resize_crop_image
from user.models import Profile
from contact.mailsender import send_verification_mail
from .forms import ProfileForm, UserForm
from django.conf import settings



def home(request):
    profiles = Profile.objects.filter(approved=True, banned=False)

    panos = None
    hamley = None
    ordered_profiles = []


    for profile in profiles:
        if profile.user.username == settings.PANOS:
            panos = profile
        elif profile.user.username == settings.HAMLEY:
            hamley = profile
        else:
            ordered_profiles.append(profile)
    
    ordered_profiles.insert(0, panos)
    ordered_profiles.append(hamley)

    context = {
        "member_profiles": ordered_profiles,
    }
    return render(request, "pages/index.html", context)


def wikiCow(request):
    return render(request, "pages/wikicow.html")


def subscribe_newsletter(request):
    """ This function is only in use when the newsletter form is on the site. """
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
    if request.method == 'POST':

        profile_form = ProfileForm(request.POST, request.FILES)
        user_form = UserForm(request.POST)
        response = {}

        if request.is_ajax():

            if user_form.is_valid() and profile_form.is_valid():
                first_name = user_form.cleaned_data.get("first_name")
                last_name = user_form.cleaned_data.get("last_name")
                email = user_form.cleaned_data.get("email")
                affiliation = profile_form.cleaned_data.get("affiliation")
                display_member = profile_form.cleaned_data.get("display_member")
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
                    profile_picture = resize_crop_image(profile_picture, 150, str(profile.registration_key))
                    profile.profile_picture = profile_picture
                    profile.save()

                send_verification_mail(request, profile)

                response = {"success": "Application received. Please check your email for verification."}

            else:
                print(user_form.errors)
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
