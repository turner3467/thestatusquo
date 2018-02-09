from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd(-@40ur(#rtu#=9i9j7-n05hc#pan2$lvuss!cz+=%*5hk7au'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ALLOWED_HOSTS = ['.thestatusquo.co.uk']

try:
    from .local import *
except ImportError:
    pass
