DATABASE_ENGINE = 'sqlite3'

SITE_ID = 1
ROOT_URLCONF = 'cab.tests.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

HAYSTACK_SITECONF = 'cab.tests.search_sites'
HAYSTACK_SEARCH_ENGINE = 'dummy'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'cab',
    'cab.tests',
    'ratings',
    'taggit',
)
