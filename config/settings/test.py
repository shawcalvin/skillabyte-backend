from .base import *

DEBUG = True

ALLOWED_HOSTS = ['test.skillabyte.com']
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ['https://test.skillabyte.com']

BASE_FRONTEND_DOMAIN = get_secret("TEST_FRONTEND_DOMAIN")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': get_secret('LOCAL_DATABASE_HOST'),
        'NAME': get_secret('LOCAL_DATABASE_NAME'),
        'PORT': get_secret('LOCAL_DATABASE_PORT'),
        'USER': get_secret('LOCAL_DATABASE_USER'),
        'PASSWORD': get_secret('LOCAL_DATABASE_PASSWORD'),
    }
}