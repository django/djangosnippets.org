import os

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)

ADMINS = (
    ('Jannis Leidel', 'jannis@leidel.info'),
)
MANAGERS = ADMINS


SITE_ID = 1
SITE_NAME = 'djangosnippets.org'

DEBUG = TEMPLATE_DEBUG = False

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = True

DEFAULT_FROM_EMAIL = 'no-reply@djangosnippets.org'
SERVER_EMAIL = 'no-reply@djangosnippets.org'
EMAIL_SUBJECT_PREFIX = '[djangosnippets] '

FORCE_WWW = False

ROOT_URLCONF = 'djangosnippets.urls'
HAYSTACK_SITECONF = 'djangosnippets.search_sites'

CACHE_KEY_PREFIX = 'djangosnippets'
CACHE_MIDDLEWARE_KEY_PREFIX = CACHE_KEY_PREFIX
CACHE_MIDDLEWARE_SECONDS = 60

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'cab',
    'cab.comments',
    'haystack',
    'pagination',
    'ratings',
    'registration',
    'south',
    'taggit',
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

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request'
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

COMMENTS_APP = 'cab.comments'