from __future__ import absolute_import
import os
import urlparse
import dj_database_url

from djangosnippets.settings.base import *

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)

# Heroku needs Gunicorn specifically.
INSTALLED_APPS += ('gunicorn',)

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = os.environ['AWS_S3_CUSTOM_DOMAIN']
AWS_PRELOAD_METADATA = True
# AWS_IS_GZIPPED = True
AWS_S3_USE_SSL = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_URL_PROTOCOL = '//:'

INSTALLED_APPS += ('djangosecure',)
MIDDLEWARE_CLASSES = (('djangosecure.middleware.SecurityMiddleware',) +
                      MIDDLEWARE_CLASSES)
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# The header Heroku uses to indicate SSL:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = [
    'djangosnippets.org',
    'www.djangosnippets.org',
]

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Pull the various config info from Heroku.
# Heroku adds some of this automatically if we're using a simple settings.py,
# but we're not and it's just as well -- I like doing this by hand.

# Grab database info
DATABASES = {'default': dj_database_url.config()}

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2'
}

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
    INSTALLED_APPS += ("raven.contrib.django.raven_compat",)
    RAVEN_CONFIG = {
        'dsn': os.environ.get('SENTRY_DSN'),
    }

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': os.environ.get('SEARCHBOX_SSL_URL', ''),
        'INDEX_NAME': 'djangosnippets-prod',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
}

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

SECRET_KEY = os.environ['SECRET_KEY']

AKISMET_SECRET_API_KEY = os.environ['AKISMET_KEY']

RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']
RECAPTCHA_USE_SSL = True
