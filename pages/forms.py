from django import forms
from user.models import User


class NewsletterForm(forms.Form):

    newsletter_email = forms.EmailField(label="", required=True, widget=forms.EmailInput(attrs={
        'class': 'emailfield form-control',
        'id': 'input-email',
        'placeholder': 'Your e-mail',
    }))


class NewsletterForm(forms.Form):

    newsletter_email = forms.EmailField(label="", required=True, widget=forms.EmailInput(attrs={
        'class': 'emailfield form-control',
        'id': 'input-email',
        'placeholder': 'Your e-mail',
    }))