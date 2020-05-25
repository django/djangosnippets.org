from djangosnippets.settings.base import *  # noqa: F403

DEBUG = True

SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz0123456789'

DATABASES = {'default': dj_database_url.config(default='postgres:///djangosnippets')}

DATABASES['default']['ATOMIC_REQUESTS'] = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHE_BACKEND = 'dummy://'
