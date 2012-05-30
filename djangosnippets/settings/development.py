from djangosnippets.settings.base import *

DEBUG = True

SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz0123456789'

ADMINS = (
)
MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": 'snippets.db',
    },
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = 2525

CACHE_BACKEND = 'dummy://'

HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, 'whoosh_index')
