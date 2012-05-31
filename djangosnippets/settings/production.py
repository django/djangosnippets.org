from __future__ import absolute_import
import os
import urlparse
import dj_database_url

from djangosnippets.settings.base import *

# Heroku needs Gunicorn specifically.
INSTALLED_APPS += ('gunicorn',)

#
# Now lock this sucker down.
#
# INSTALLED_APPS += ['djangosecure']
# MIDDLEWARE_CLASSES.insert(0, 'djangosecure.middleware.SecurityMiddleware')
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 600
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_FRAME_DENY = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True

# The header Heroku uses to indicate SSL:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Canoncalize on "dashboard.djangoproject.com"
# MIDDLEWARE_CLASSES.insert(0, 'dashboard.middleware.CanonicalDomainMiddleware')
# CANONICAL_HOSTNAME = 'dashboard.djangoproject.com'

#
# Store files on S3, pulling config from os.environ.
#
# DEFAULT_FILE_STORAGE = STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
# AWS_S3_SECURE_URLS = False
# AWS_QUERYSTRING_AUTH = False

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'assets', 'static')
STATIC_URL = '/assets/static/'
ADMIN_MEDIA_PREFIX = '/assets/static/admin/'

# Pull the various config info from Heroku.
# Heroku adds some of this automatically if we're using a simple settings.py,
# but we're not and it's just as well -- I like doing this by hand.

# Grab database info
DATABASES = {}
DATABASES = {'default': dj_database_url.config()}

# Make sure urlparse understands custom config schemes.
urlparse.uses_netloc.append('redis')

# Now do redis and the cache.
redis_url = urlparse.urlparse(os.environ['REDISTOGO_URL'])
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': redis_url.password,
        },
        'VERSION': os.environ.get('CACHE_VERSION', 0),
    },
}

# Use Sentry for debugging if available.
if 'SENTRY_DSN' in os.environ:
    INSTALLED_APPS += ("raven.contrib.django",)
    SENTRY_DSN = os.environ.get('SENTRY_DSN')

HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = os.environ.get('WEBSOLR_URL', '')

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = os.environ.get('MAILGUN_ACCESS_KEY')
MAILGUN_SERVER_NAME = 'djangosnippets.mailgun.org'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}