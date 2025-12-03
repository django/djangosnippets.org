import os
from pathlib import Path

import dj_database_url
from django.contrib import messages
from django.urls import reverse
from dotenv import load_dotenv

load_dotenv()


def user_url(user):
    return reverse("cab_author_snippets", kwargs={"username": user.username})


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SITE_ID = 1
SITE_NAME = "djangosnippets.org"

ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS",
    "djangosnippets.org,www.djangosnippets.org",
).split(",")

DEBUG = False

TIME_ZONE = "America/Chicago"
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_TZ = False

DEFAULT_FROM_EMAIL = "no-reply@djangosnippets.org"
SERVER_EMAIL = "no-reply@djangosnippets.org"
EMAIL_SUBJECT_PREFIX = "[djangosnippets] "


ABSOLUTE_URL_OVERRIDES = {
    "auth.user": user_url,
}

FORCE_WWW = False

ROOT_URLCONF = "djangosnippets.urls"

CACHE_KEY_PREFIX = "djangosnippets"
CACHE_MIDDLEWARE_KEY_PREFIX = CACHE_KEY_PREFIX
CACHE_MIDDLEWARE_SECONDS = 60

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django_comments",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.bitbucket_oauth2",
    "allauth.socialaccount.providers.github",
    "base",
    "cab",
    "comments_spamfighter",
    "ratings",
    "taggit",
    "tailwind",
    "theme",
    "django_recaptcha",
    "django_components",
    "rest_framework",
    "django_htmx",
    "widget_tweaks",
]

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # 'django.middleware.cache.UpdateCacheMiddleware',
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "ratelimitbackend.middleware.RateLimitMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "allauth.account.middleware.AccountMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(Path(PROJECT_ROOT) / "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                        "django_components.template_loader.Loader",
                    ],
                ),
            ],
            "builtins": [
                "django_components.templatetags.component_tags",
            ],
        },
    },
]

STATIC_URL = "/assets/static/"
STATIC_ROOT = str(Path(PROJECT_ROOT) / ".." / "assets" / "static")
STATICFILES_DIRS = (str(Path(PROJECT_ROOT) / "static"),)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_components.finders.ComponentsFileSystemFinder",
]

TAILWIND_APP_NAME = "theme"

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_SIGNUP_FIELDS = ["username*", "email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_FORMS = {
    "login": "base.forms.DjangoSnippetsLoginForm",
}
ACCOUNT_SESSION_REMEMBER = True
SOCIALACCOUNT_ADAPTER = "djangosnippets.adapters.DjangoSnippetsSocialAccountAdapter"
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_LOGIN_ON_GET = True

LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

COMMENTS_APP = "cab"

CAB_VERSIONS = (
    ("5.2", "5.2"),
    ("5.1", "5.1"),
    ("5.0", "5.0"),
    ("4.2", "4.2"),
    ("4.1", "4.1"),
    ("4.0", "4.0"),
    ("3.2", "3.2"),
    ("3.1", "3.1"),
    ("3.0", "3.0"),
    ("2.2", "2.2"),
    ("2.1", "2.1"),
    ("2.0", "2.0"),
    ("1.11", "1.11"),
    ("1.10", "1.10"),
    ("1.9", "1.9"),
    ("1.8", "1.8"),
    ("1.7", "1.7"),
    ("1.6", "1.6"),
    ("1.5", "1.5"),
    ("1.4", "1.4"),
    ("1.3", "1.3"),
    ("1.2", "1.2"),
    ("1.1", "1.1"),
    ("1.0", "1.0"),
    ("0.96", ".96"),
    ("0.95", "Pre .96"),
    ("0", "Not specified"),
)

# keys for localhost and 127.0.0.1
RECAPTCHA_PUBLIC_KEY = "6LcXj_oSAAAAAPQ3u23Y6MqQqd2yMYtnHqa7Zj61"
RECAPTCHA_PRIVATE_KEY = "6LcXj_oSAAAAAFN31LR-F31lwFSQAcJgsg1pE5WP"
RECAPTCHA_USE_SSL = True

AUTHENTICATION_BACKENDS = (
    "ratelimitbackend.backends.RateLimitModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

DISQUS_WEBSITE_SHORTNAME = "djangosnippets"
DISQUS_USE_SINGLE_SIGNON = True

MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "alert",
}


DATABASES = {"default": dj_database_url.config(conn_max_age=600, conn_health_checks=True)}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
    ],
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
