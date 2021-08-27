from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import Http404
from django.core.validators import validate_email
from user.mailing_lists import add_subscriber


def home(request):
    return render(request, "pages/index.html")


def wikiCow(request):
    return render(request, "pages/wikicow.html")

def subscribe_newsletter(request):
    if request.method == 'POST':

        email = request.POST.get('input_email')
        response_data = {}

        try:
            validate_email(email)
            print("pretend to create new user")
            add_subscriber(email)

            response_data['success'] = 'Subscription successful!'
        except:
            response_data['error'] = 'Invalid email'


        # subscriber = User(email=email, username=email)
        # subscriber.save()
        # subscriber.profile = Profile()
        # subscriber.profile.dave
        # print(subscriber)
        # print(subscriber.profile)
        # mailing_list = MailingList.objects.filter(name="general newsletter").first()
        # print(mailing_list.id)
        # subscriber.profile.mailing_lists.add(mailing_list)

        #print(dir(subscriber.profile))


        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        raise Http404("Use the newsletter subscription form to subscribe to our newsletter")
