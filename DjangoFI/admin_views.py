from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django import forms
from django.contrib import messages
from contact.mailsender import sendMail
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

        context = {

            "form": form

        }

        messages.success(self.request, "Emaill not sent :)")
        return render(self.request, self.template_name, context)

