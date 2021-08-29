from django import forms
from user.models import User


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
