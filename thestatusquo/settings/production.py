from __future__ import absolute_import, unicode_literals

import os
from .base import *

DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRESQL_NAME'],
        'USER': os.environ['POSTGRESQL_USER'],
        'PASSWORD': os.environ['POSTGRESQL_PASSWORD'],
        'HOST': '',
        'PORT': 5432,
    }
}

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ['EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_USER']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

try:
    from .local import *
except ImportError:
    pass
