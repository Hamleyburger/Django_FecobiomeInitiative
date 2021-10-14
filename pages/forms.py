from django import forms
from django.forms.fields import ImageField
from user.models import User, Profile
from django.core.validators import FileExtensionValidator


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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["affiliation", "profile_picture", "display_member"]
    
    affiliation = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Institute or university'}))
    profile_picture = forms.ImageField(required=False, validators=[FileExtensionValidator( ['jpg', 'jpeg', 'png'] )], widget=forms.FileInput(attrs={'hidden': ''}))
