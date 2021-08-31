from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from user.subscription_handler import unsubscribe
from django.contrib import messages
from django import forms
from django.shortcuts import render
from django import http


class UnsibscribeForm(forms.Form):
    email = forms.EmailField(label="Your e-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))

class UnsubscribeFormView(FormView):
    template_name = "unsubscribe.html"
    form_class = UnsibscribeForm
    unsubscribe_key = ""
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

    
        
    
