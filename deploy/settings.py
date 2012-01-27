import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

MEDIA_ROOT = '%s/media/' % (SITE_ROOT)
MEDIA_DOMAIN = 'http://djangosnippets.org'
MEDIA_URL = '%s/media/' % (MEDIA_DOMAIN)
ADMIN_MEDIA_PREFIX = '%s/media/admin/' % (MEDIA_DOMAIN)

CACHE_BACKEND = 'memcached://localhost:11211/'
CACHE_KEY_PREFIX = 'djangosnippets'
CACHE_MIDDLEWARE_KEY_PREFIX = CACHE_KEY_PREFIX
CACHE_MIDDLEWARE_SECONDS = 60

FORCE_WWW = False
LOGIN_REDIRECT_URL = '/'

SITE_NAME = 'djangosnippets.org'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangosnippets_main',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '<YOUR DATABASE HOST>',
        #'PORT': 6432, # pgBouncer
    }
}

if DEBUG:
    CACHE_BACKEND = 'dummy://'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
SITE_ID = 1
SECRET_KEY = ''
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    #'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'djangosnippets.urls'

TEMPLATE_DIRS = (
    '%s/templates/' % (SITE_ROOT),
)

ACCOUNT_ACTIVATION_DAYS = 7

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_AFFILIATE_ID = ''

HAYSTACK_SOLR_URL = 'http://<YOUR SERVER>:8999/solr/djangosnippets-autocomplete/'
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SITECONF = 'djangosnippets.search_sites'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'cab',
    'haystack',
    'pagination',
    'ratings',
    'registration',
    'south',
    'taggit',
)
