from djangosnippets.settings.base import *  # noqa: F403

DEBUG = True

SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz0123456789'

import dj_database_url


DATABASES = {'default': dj_database_url.config(default='postgres:///djangosnippets')}

DATABASES['default']['ATOMIC_REQUESTS'] = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHE_BACKEND = 'dummy://'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'whoosh_index'),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
}
