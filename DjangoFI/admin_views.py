from django.forms.fields import ImageField
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib import messages
# mail related imports
from contact.mailsender import send_newsletter
from user.subscription_handler import get_subscribers_emails as newsletter_subscribers
# forms.py-ish imports
from django import forms
from ckeditor.fields import CKEditorWidget
from user.models import Profile


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

        send_newsletter(self.request, "FI Newsletter",
                        newsletter_subscribers(), subject, message)

        context = {
            "form": form
        }

        messages.success(self.request, "Newsletter has been sent to everybody! :-)")
        return render(self.request, self.template_name, context)



@method_decorator(staff_member_required, name='dispatch')
class MemberView(ListView):

    model = Profile
    template_name = "admin/approve.html"
    context_object_name = "profiles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context

    def get_queryset(self):
        queryset = Profile.objects.filter(user_verified=True, approved=False, banned=False, user__is_staff=False).all()
        return queryset


@staff_member_required
def approve_members(request):


    if request.method == 'POST':
        print(request.POST.get)
        button = request.POST.get("approve-submit")
        user_id = int(request.POST.get("user_id"))
        profile = Profile.objects.filter(user__id=user_id).first()

        if button == "approve":
            print("approve {}".format(user_id))
            profile.approved = True
            profile.save()

        elif button == "disapprove":
            print("disapprove {}".format(user_id))
            profile.user.delete()

        elif button == "ban":
            print("ban {}".format(user_id))
            profile.banned = True
            profile.profile_picture.delete()
            profile.save()


    profiles = Profile.objects.filter(user_verified=True, approved=False, banned=False, user__is_staff=False).all()

    context = {
        "profiles": profiles,
    }

    return render(request, "admin/approve.html", context)



