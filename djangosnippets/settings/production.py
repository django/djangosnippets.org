from __future__ import absolute_import
import os
import urlparse
import dj_database_url

from djangosnippets.settings.base import *

# Heroku needs Gunicorn specifically.
INSTALLED_APPS += ('gunicorn',)

# INSTALLED_APPS += ('djangosecure',)
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
            'PARSER_CLASS': 'redis.connection.HiredisParser'
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

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

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
