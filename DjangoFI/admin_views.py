from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib import messages
# mail related imports
from contact.mailsender import send_mail_from_admin
from user.mailing_lists import get_subscribers_emails as newsletter_subscribers
# forms.py-ish imports
from django import forms
from ckeditor.fields import CKEditorWidget

class NewsletterForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Message', widget=CKEditorWidget(attrs={'class': 'form-control'}))


@method_decorator(staff_member_required, name='dispatch')
class NewsletterView(FormView):

    template_name = "admin/write_newsletter.html"
    form_class = NewsletterForm
    #success_url = template_name

    def form_valid(self, form):

        subject = form.data["subject"]
        message = form.data["message"]
        # sender_email = self.request.user.email
        print(message)

        send_mail_from_admin("FI Newsletter", newsletter_subscribers(), subject, message)

        context = {

            "form": form

        }

        messages.success(self.request, "Emaill not sent :)")
        return render(self.request, self.template_name, context)

