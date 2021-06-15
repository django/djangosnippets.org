from djangosnippets.settings.base import *

SITE_ID = 1
ROOT_URLCONF = 'cab.tests.urls'

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.messages',
    'django_comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.bitbucket',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.twitter',
    'comments_spamfighter',
    'cab',
    'ratings',
    'taggit',
    'ratings.tests',
    'rest_framework',
)

SECRET_KEY = 'yadayada'

STATIC_URL = '/static/'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

SNIPPETS_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      os.pardir, os.pardir, 'djangosnippets', 'templates')

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'cab', 'tests', 'templates'), SNIPPETS_TEMPLATES_DIR],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django.template.context_processors.request',
        ],
    },
}]

CAB_VERSIONS = (
    ('0.0', '0.0'),
    ('1.1', '1.1'),
)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
