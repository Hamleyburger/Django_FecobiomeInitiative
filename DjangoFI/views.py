from django.http.response import Http404
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from user.subscription_handler import cancel_membership, verify_profile
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
        unsubscribed_user = False
        if key:
            unsubscribed = cancel_membership(unsubscribe_key=key)
            if unsubscribed:
                messages.success(self.request, "Your membership is successfully cancelled. You're welcome back anytime!")
                unsubscribed_user = True
            else:
                messages.error(self.request, "This cancellation token does not exist. Try typing your email below instead.")

        context = super().get_context_data(**kwargs)
        context["unsubscribed"] = unsubscribed_user
        return context

    # This is relevant if users can unsubscribe by typing their emails
    # def form_valid(self, form):

    #     email = form.data["email"]
    #     unsubscribed = cancel_membership(unsubscribe_email=email)
    #     if unsubscribed:
    #         messages.success(self.request, "Your membership is successfully cancelled. You're welcome back anytime!")
    #     else:
    #         messages.warning(self.request, "No member exists with this email")
    #     return http.HttpResponseRedirect(self.request.path)


class ValidateForm(forms.Form):

    uuid = forms.UUIDField(widget=forms.HiddenInput)

    def clean_uuid(self):
        data = self.cleaned_data['uuid']
        profile = Profile.objects.filter(registration_key=data, user_verified=False, banned=False).first()
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

        profile = Profile.objects.filter(registration_key=requested_key, approved=False, banned=False).first()
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
            if verify_profile(self.request, profile):
                messages.success(self.request, "User details successfully verified. Awaiting approval.")
            else:
                messages.error(self.request, "Sorry. We're closed.")
        else:
            profile.user.delete()
            messages.success(self.request, "User details successfully deleted.")

        return http.HttpResponseRedirect(self.request.path)
