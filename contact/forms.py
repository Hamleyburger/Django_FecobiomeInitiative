from django import forms
from user.models import User
from resources.models import resources_meta
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

class ContactForm(forms.Form):

    choices = []
    
    contactables = User.objects.filter(profile__contactable=True).all()

    for contact in contactables:
        choices.append((contact.id, contact.profile.display_name))

    name = forms.CharField(label='Your name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Your e-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # recipient = forms.ChoiceField(label="Recepient", choices=choices, widget=forms.Select(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Subject', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class': 'form-control'}))


    class Meta:
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            #"recipient": forms.Select(attrs={'class': 'form-control'}),
            "subject": forms.TextInput(attrs={'class': 'form-control'}),
            "message": forms.Textarea(attrs={'class': 'form-control'}),
        }


class SubmitDataForm(forms.Form):

    choices = []
    database_choices = []
    example_file_choices = {}

    for key, value in resources_meta.items():
        database_choices.append((key, value["name"]))
        example_file_choices[key] = {
            "txt": value["example_file_txt"],
            "xlsx": value["example_file_xlsx"]
        }

    first_example_file = [example_file_choices[database_choices[0][0]]
                          ["txt"], example_file_choices[database_choices[0][0]]["xlsx"]]

    contactables = User.objects.filter(profile__contactable=True).all()

    for contact in contactables:
        choices.append((contact.id, contact.profile.display_name))

    database = forms.ChoiceField(label="Database", choices=database_choices, widget=forms.Select(
        attrs={'class': 'form-control half-field'}))

    name = forms.CharField(label='Your name', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Your name'}))
    email = forms.EmailField(label="Your e-mail", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Your email'}))
    # recipient = forms.ChoiceField(label="Recepient", choices=choices, widget=forms.Select(attrs={'class': 'form-control'}))
    affiliation = forms.CharField(label='Affiliation', max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Institute or university'}))
    message = forms.CharField(label='Message (optional)', widget=forms.Textarea(
        attrs={'class': 'form-control'}),  required=False)
    file = forms.FileField(
        label="", 
        widget=forms.FileInput(attrs={'hidden': ''}), 
        validators=[FileExtensionValidator( ['txt', 'xlsx'] )]
    )

