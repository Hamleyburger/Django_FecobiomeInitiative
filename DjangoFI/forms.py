from django import forms
from user.models import User, Profile
from django.core.exceptions import ValidationError
from user.mixins import reCAPTCHAValidation


class UnsibscribeForm(forms.Form):

    email = forms.EmailField(label="Your e-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    key = forms.UUIDField(widget=forms.HiddenInput())
    recaptcha_token = forms.CharField(widget=forms.HiddenInput(), error_messages={'required': 'Recaptcha token missing. Try refreshing the page or re-enable Javascript.'})

    def clean(self):

        cleaned_data = super().clean()
        mail = cleaned_data.get("email")
        subkey = cleaned_data.get("key")

        cancellor = Profile.objects.filter(user__email=mail).first()
        #print(cancellor.registration_key)
        if (not cancellor) or (not cancellor.registration_key == subkey):
            raise ValidationError('This email does not match the clicked link. Did you change the URL address or the email address above? If you have no email (a newsletter) with a cancellation link please contact us to cancel your membership. This is done to ensure that people cannot cancel each other\'s memberships.')


    def clean_recaptcha_token(self): # The name actually needs to be clean_ plus field name or it won't work
        data = self.cleaned_data['recaptcha_token']
        captcha = reCAPTCHAValidation(data)
        print("validating recaptcha")
        if not captcha.get("success"):
            raise ValidationError("Request denied: Invalid recaptcha token")
        elif captcha["score"] < 0.5:
            raise ValidationError("Request denied: Suspicious behaviour")
        print("recaptcha passed")
        
        return captcha["score"]


