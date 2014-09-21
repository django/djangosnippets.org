import os
from django.core.urlresolvers import reverse


def user_url(user):
    return reverse('cab_author_snippets', kwargs={'username': user.username})


PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            os.pardir)

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
USE_TZ = False

DEFAULT_FROM_EMAIL = 'no-reply@djangosnippets.org'
SERVER_EMAIL = 'no-reply@djangosnippets.org'
EMAIL_SUBJECT_PREFIX = '[djangosnippets] '


ABSOLUTE_URL_OVERRIDES = {
    'auth.user': user_url,
}

FORCE_WWW = False

ROOT_URLCONF = 'djangosnippets.urls'

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

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.bitbucket',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.twitter',

    'cab',
    'cab.comments',
    'comments_spamfighter',
    'haystack',
    'pagination',
    'ratings',
    'south',
    'taggit',
    'captcha',
    'disqus',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'ratelimitbackend.middleware.RateLimitMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    # allauth specific context processors
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

STATIC_URL = '/assets/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, '..', 'assets', 'static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_ADAPTER = 'djangosnippets.adapters.DjangoSnippetsAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'djangosnippets.adapters.DjangoSnippetsSocialAccountAdapter'
SOCIALACCOUNT_AUTO_SIGNUP = False

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

COMMENTS_APP = 'cab.comments'

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

CAB_VERSIONS = (
    (1.7, '1.7'),
    (1.6, '1.6'),
    (1.5, '1.5'),
    (1.4, '1.4'),
    (1.3, '1.3'),
    (1.2, '1.2'),
    (1.1, '1.1'),
    (1, '1.0'),
    (.96, '.96'),
    (.95, 'Pre .96'),
    (0, 'Not specified'),
)

# keys for localhost and 127.0.0.1
RECAPTCHA_PUBLIC_KEY = '6LcXj_oSAAAAAPQ3u23Y6MqQqd2yMYtnHqa7Zj61'
RECAPTCHA_PRIVATE_KEY = '6LcXj_oSAAAAAFN31LR-F31lwFSQAcJgsg1pE5WP'
RECAPTCHA_USE_SSL = True

AUTHENTICATION_BACKENDS = (
    'ratelimitbackend.backends.RateLimitModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

DISQUS_WEBSITE_SHORTNAME = 'djangosnippets'
DISQUS_USE_SINGLE_SIGNON = True

from django.contrib import messages

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'alert',
}
