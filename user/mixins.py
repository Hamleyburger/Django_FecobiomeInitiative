import requests
from django.conf import settings

def reCAPTCHAValidation(token):
    result = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", 
        data={
            "secret": settings.RECAPTCHA_PRIVATE_KEY,
            "response": token
        })
    return result.json()