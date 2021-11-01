from django.http.response import Http404
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from user.subscription_handler import unsubscribe, verify_profile
from django.contrib import messages
from django import forms
from django.shortcuts import render
from django import http
from user.models import Profile
from django.core.exceptions import ValidationError


class UnsibscribeForm(forms.Form):
    email = forms.EmailField(label="Your e-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))

class UnsubscribeFormView(FormView):
    template_name = "unsubscribe.html"
    form_class = UnsibscribeForm
    unsubscribe_key = "" # Can be removed
    def get_context_data(self, **kwargs):
        key = self.kwargs.get("unsubscribe_key")
        if key:
            print(key)
            unsubscribed = unsubscribe(unsubscribe_key=key)
            if unsubscribed:
                messages.success(self.request, "You have been successfully unsubscribed from our newsletter. You're welcome back anytime!")
            else:
                messages.error(self.request, "This unsubscribe token does not exist in our mailing list. Try typing your email below.")

        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):

        email = form.data["email"]
        unsubscribed = unsubscribe(unsubscribe_email=email)
        if unsubscribed:
            messages.success(self.request, "You have been successfully unsubscribed from our newsletter. You're welcome back anytime!")
        else:
            messages.warning(self.request, "This email does not exist in our mailing list")
        return http.HttpResponseRedirect(self.request.path)


def validate_registration(request):
    """
    User kan se sine indtastede oplysninger og billede.
    To knapper: "Accept" og "Delete"
    if POST:
        if btn is accept:
            if profile with uuid exists:
                set user to "validated" and send approval request
            else message "Link expired. Profile no longer exists"
        else (btn is delete):
            if user is not validated:
                delete profile and user
            else:
                message "Link expired. Profile already validated.
            

    """
    return render(request, "template")


class ValidateForm(forms.Form):

    uuid = forms.UUIDField(widget=forms.HiddenInput)

    def clean_uuid(self):
        data = self.cleaned_data['uuid']
        profile = Profile.objects.filter(registration_key=data, user_verified=False).first()
        if not profile:
            raise ValidationError("Invalid email confirmation link")

        return profile

class ValidateFormView(FormView):
    template_name = "validate.html"
    form_class = ValidateForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        requested_key = self.kwargs.get("registration_key")
        context["registration_key"] = requested_key

        profile = Profile.objects.filter(registration_key=requested_key, approved=False).first()
        context["profile"] = profile

        return context


    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        initial['uuid'] = self.kwargs.get("registration_key")
        return initial


    def form_valid(self, form):

        profile = form.cleaned_data["uuid"]

        if 'submit_validate' in self.request.POST:
            verify_profile(profile)
            messages.success(self.request, "User details successfully verified. Awaiting approval.")
        else:
            profile.user.delete()
            messages.success(self.request, "User details successfully deleted.")

        return http.HttpResponseRedirect(self.request.path)
