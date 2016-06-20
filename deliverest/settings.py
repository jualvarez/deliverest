
# -*- coding: utf-8 -*-

"""
Django settings for deliverest project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'update_in_settings_local.py'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['jualvarez.webfactional.com']


# Application definition

INSTALLED_APPS = (
    # Project apps
    'delidelivery',
    'deliproducts',
    'delicontacts',
    'deliorders',
    'delicontent',

    'autocomplete_light',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third party apps
    #'debug_toolbar.apps.DebugToolbarConfig',
    #'social.apps.django_app.default',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    'django_extensions',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'delicontacts.middleware.AssociateUserToCustomerMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'deliorders.context_processors.check_timeframe',
                 # Required by `allauth` template tags
                'django.core.context_processors.request'
            ]
        }
    }
]

ROOT_URLCONF = 'deliverest.urls'

WSGI_APPLICATION = 'deliverest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost'
    }
}

ABSOLUTE_URL = 'http://organicosdemitierra.com'
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
URL_PATH = ''

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
SOCIALACCOUNT_EMAIL_VERIFICATION = False


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

SITE_ID = 1
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Cordoba'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_FROM_EMAIL = 'email@server.com'
EMAIL_HOST = 'smtp.server.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'noreply'
EMAIL_HOST_PASSWORD = 'password'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/juan/Documents/dev/deliverest/static_root'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/juan/Documentos/dev/deliverest_media'


# Application specific settings
CATEGORY_SLUG_FOR_OTHER = 'otras'

# Monday is 0
WEEKLY_WINDOW_START = 0  # Monday
WEEKLY_WINDOW_END = 3  # Thursday

WEEKLY_WINDOW_START_HOUR = 11
WEEKLY_WINDOW_END_HOUR = 20

WEEKLY_DELIVERY_START = 2  # Wednesday
WEEKLY_DELIVERY_END = 3  # Thursday

# Delivery defaults
DELIVERY_DEFAULT_PRICE = 20.0

# Import local configurations
from settings_local import *
