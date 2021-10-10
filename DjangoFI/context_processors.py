from pages import forms


def base_context(request):
    """ Custom code that needs to be available from the base template """
    newsletterform = forms.NewsletterForm()
    member_user_form = forms.UserForm()
    member_profile_form = forms.ProfileForm()
    return {
        'newsletter_form': newsletterform,
        'member_user_form': member_user_form,
        'member_profile_form': member_profile_form
    }

