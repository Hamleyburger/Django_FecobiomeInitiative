from pages import forms


def base_context(request):
    """ Custom code that needs to be available from the base template """
    newsletterform = forms.NewsletterForm()
    return {
        'newsletter_form': newsletterform
    }
