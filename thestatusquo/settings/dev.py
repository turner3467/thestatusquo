from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
<<<<<<< HEAD
SECRET_KEY = 'd(-@40ur(#rtu#=9i9j7-n05hc#pan2$lvuss!cz+=%*5hk7au'
=======
SECRET_KEY = 'sz(s!*l=u2otc-h$h$)v7bynz7c*+&-w6xn)*enoosli_%jp$7'
>>>>>>> 64401152d4d6ebaa8d127a8b144e0271f717b68c


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
