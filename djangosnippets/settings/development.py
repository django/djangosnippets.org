from djangosnippets.settings.base import *  # noqa: F403

DEBUG = True

SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz0123456789'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHE_BACKEND = 'dummy://'

INSTALLED_APPS = INSTALLED_APPS

ALLOWED_HOSTS = ["0.0.0.0","101a1b5d5a95.ngrok.io"]
