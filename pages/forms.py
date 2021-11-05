from django import forms
from user.models import User, Profile
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from user.mixins import reCAPTCHAValidation
from user.file_helpers import get_mimetype


class NewsletterForm(forms.Form):

    newsletter_email = forms.EmailField(label="", required=True, widget=forms.EmailInput(attrs={
        'class': 'emailfield form-control',
        'id': 'input-email',
        'placeholder': 'Your e-mail',
    }))



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email address', 'type': 'email'}))

    def clean_email(self):
        mail = self.cleaned_data['email']
        banned_list = Profile.objects.filter(banned=True).all()
        for profile in banned_list:
            if profile.user.email == mail:
                raise ValidationError("Request rejected. User is banned.")

        return mail


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["affiliation", "profile_picture", "display_member"]
    
    affiliation = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Institute or university'}))
    profile_picture = forms.ImageField(required=False, validators=[FileExtensionValidator( ['jpg', 'jpeg', 'png'] )], widget=forms.FileInput(attrs={'hidden': ''}))
    # ReCaptcha token needs to be there so the form validates the field.
    recaptcha_token = forms.CharField(widget=forms.HiddenInput(), error_messages={'required': 'Recaptcha token missing. Try refreshing the page or re-enable Javascript.'})

    def clean_recaptcha_token(self): # The name actually needs to be clean_ plus field name or it won't work
        data = self.cleaned_data['recaptcha_token']
        captcha = reCAPTCHAValidation(data)
        if not captcha.get("success"):
            raise ValidationError("Request denied: Invalid recaptcha token")
        elif captcha["score"] < 0.5:
            raise ValidationError("Request denied: Suspicious behaviour")
        return captcha["score"]
    
    def clean_profile_picture(self):
        file = self.cleaned_data['profile_picture']
        if file:
            mimetype = get_mimetype(file)
            if mimetype != "image/png" and mimetype != "image/jpeg":
                raise ValidationError("Profile picture must be .jpeg or .png")
        return file