SECRET_KEY = 'your_own_very_own_app_key'
DEBUG = True
ALLOWED_HOSTS = ['site.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost'
    }
}

ABSOLUTE_URL = 'http://site.com'
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
URL_PATH = ''


DEFAULT_FROM_EMAIL = 'email@server.com'
EMAIL_HOST = 'smtp.server.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'noreply'
EMAIL_HOST_PASSWORD = 'passwd'


STATIC_URL = '/static/'
STATIC_ROOT = '/path/to/static_root'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/path/to/media'

# Application specific settings
CATEGORY_SLUG_FOR_OTHER = 'other'

# Monday is 0
WEEKLY_WINDOW_START = 0  # Monday
WEEKLY_WINDOW_END = 3  # Thursday

WEEKLY_WINDOW_START_HOUR = 11
WEEKLY_WINDOW_END_HOUR = 20

WEEKLY_DELIVERY_START = 2  # Wednesday
WEEKLY_DELIVERY_END = 3  # Thursday

# Delivery defaults
DELIVERY_DEFAULT_PRICE = 5.0
