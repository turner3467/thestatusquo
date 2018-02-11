from __future__ import absolute_import, unicode_literals

import os
from configparser import ConfigParser
from .base import *

config = ConfigParser()
config.read(os.path.join(os.environ['HOME'], 'tsq.ini'))

DEBUG = False

SECRET_KEY = config['DJANGO']['DJANGO_SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config['DATABASE']['POSTGRESQL_NAME'],
        'USER': config['DATABASE']['POSTGRESQL_USER'],
        'PASSWORD': config['DATABASE']['POSTGRESQL_PASSWORD'],
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

ALLOWED_HOSTS = ['.thestatusquo.co.uk']

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = config['EMAIL']['EMAIL_USER']
EMAIL_HOST_PASSWORD = config['EMAIL']['EMAIL_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

try:
    from .local import *
except ImportError:
    pass
