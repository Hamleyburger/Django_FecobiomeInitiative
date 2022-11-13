from django.http.response import Http404
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from user.subscription_handler import cancel_membership, verify_profile
from django.contrib import messages
from django import forms
from django.shortcuts import render
from django import http
from user.models import Profile
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import UnsibscribeForm
import requests  
import json


class UnsubscribeFormView(FormView):

    template_name = "unsubscribe.html"
    form_class = UnsibscribeForm
    unsubscribe_key = "" # Can be removed
   
    
    def get_context_data(self, **kwargs):
        key = self.kwargs.get("unsubscribe_key")
        unsubscribe_allowed = False # To make sure that only users who used a link can get to the form

        if key:
            unsubscribe_allowed = True
            unsubscriber = Profile.objects.filter(
                registration_key=key).first()

            if unsubscriber:
                self.initial['email'] = unsubscriber.user.email
                self.initial['key'] = key
            else: 
                self.initial['email'] = ""
                self.initial['key'] = key

        context = super().get_context_data(**kwargs)
        context["unsubscribe_allowed"] = unsubscribe_allowed
        return context


    # This is relevant if users can unsubscribe by typing their emails
    def form_valid(self, form):

        key = form.cleaned_data["key"]
        response_data = {}
        try:
            cancel_membership(unsubscribe_key=key)
            response_data = {"success": 'Cancellation successful!' }
        except Exception as e:
            # If either unsubscribing or email notification failed:
            response_data = {"error": {"error": "Something went wrong. If the problem persists please contact us."}}


        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


    def form_invalid(self, form):

        response_data = {"error": form.errors }
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


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
