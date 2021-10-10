from django import forms
from user.models import User, Profile


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
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email address'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture", "display_member"]
        widgets = {
            'profile_picture': forms.FileInput(attrs={'hidden': ''}),
            # 'display_member': forms.FileInput(attrs={'hidden': ''}),
        }

