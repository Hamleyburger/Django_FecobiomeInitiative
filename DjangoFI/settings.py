from .secrets import *
from django.contrib.messages import constants as messages

"""
Django settings for DjangoFI project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = secret_debug

if DEBUG:
    ALLOWED_HOSTS = allowed_hosts_debug
else:
    ALLOWED_HOSTS = ['fecobiome.pythonanywhere.com', 'www.fecobiome.com', 'fecobiome.com']
# Application definition

INSTALLED_APPS = [
    'pages.apps.PagesConfig',
    'resources.apps.ResourcesConfig',
    'blog.apps.BlogConfig',
    'contact.apps.ContactConfig',
    'user.apps.UserConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoFI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'DjangoFI.context_processors.base_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoFI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# This is added afterwards to be able to have all static files in a global directory
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

# Media url and root I made for storing images based on this guy:
# https://www.youtube.com/watch?v=ygzGr51dbsY&list=PLCC34OHNcOtr025c1kHSPrnP18YPB-NFi&index=26
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CKEDITOR_CONFIGS = {
    "default": {
        "removePlugins": "stylesheetparser",
        'skin': 'moono-lisa',
        'toolbar_Basic': [['-', 'Bold', 'Italic']],
        'toolbar_Full': [
            ['Bold', 'Italic', 'Underline', 'Strike',
                'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink'], ['Table'],
            ['SpecialChar']],
        'toolbar': 'Full',
        'height': 291,
        'width': 'auto',
        'filebrowserWindowWidth': 940,
        'filebrowserWindowHeight': 725,
    }
}

# Email configs for mailing bot
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = secret_email_host_user
EMAIL_HOST = secret_email_host
EMAIL_PORT = secret_email_port
EMAIL_HOST_PASSWORD = secret_email_password
EMAIL_USE_TLS = True


# By importing messages we can set bootstrap classes to django message categories:
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


# HTTPS SETTINGS

SESSION_COOKIE_SECURE = secret_session_cookie_secure
CSRF_COOKIE_SECURE = secret_csrf_cookie_secure
SECURE_SSL_REDIRECT = secret_secure_ssl_redirect

# HSTS SETTINGS
SECURE_HSTS_SECONDS = secret_secure_hsts_seconds
SECURE_HSTS_PRELOAD = secret_secure_hsts_preload
SECURE_HSTS_INCLUDE_SUBDOMAINS = secret_secure_hsts_include_subdomains

if DEBUG:
    RECAPTCHA_PUBLIC_KEY = debug_recaptcha_site_key
    RECAPTCHA_PRIVATE_KEY = debug_recaptcha_secret_key
else:
    RECAPTCHA_PUBLIC_KEY = deploy_recaptcha_site_key
    RECAPTCHA_PRIVATE_KEY = deploy_recaptcha_secret_key
