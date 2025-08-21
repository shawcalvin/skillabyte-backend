from .base import *

DEBUG = False

ALLOWED_HOSTS = ['learning.skillabyte.com','localhost']
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ['https://learning.skillabyte.com','http://localhost:3000']

BASE_FRONTEND_DOMAIN = get_secret("PROD_FRONTEND_DOMAIN")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': get_secret('PRODUCTION_DATABASE_HOST'),
        'NAME': get_secret('PRODUCTION_DATABASE_NAME'),
        'PORT': get_secret('PRODUCTION_DATABASE_PORT'),
        'USER': get_secret('PRODUCTION_DATABASE_USER'),
        'PASSWORD': get_secret('PRODUCTION_DATABASE_PASSWORD'),
    }
}