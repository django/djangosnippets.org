import os  # noqa: F401
from pathlib import Path

from djangosnippets.settings.base import *  # noqa: F403

SITE_ID = 1
ROOT_URLCONF = "cab.tests.urls"

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "allauth.account.middleware.AccountMiddleware",
)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.messages",
    "django_comments",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.forms",
    "django_components",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.bitbucket_oauth2",
    "allauth.socialaccount.providers.github",
    "base",
    "base.tests",
    "comments_spamfighter",
    "cab",
    "ratings",
    "taggit",
    "rest_framework",
]

SECRET_KEY = "yadayada"

STATIC_URL = "/static/"

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

SNIPPETS_TEMPLATES_DIR = str(
    Path(__file__).resolve().parent.parent.parent / "djangosnippets" / "templates",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(Path(__file__).resolve().parent.parent.parent / "cab" / "tests" / "templates"),
            SNIPPETS_TEMPLATES_DIR,
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                "django_components.template_loader.Loader",
            ],
            "builtins": [
                "django_components.templatetags.component_tags",
            ],
        },
    },
]

CAB_VERSIONS = (
    ("0.0", "0.0"),
    ("1.1", "1.1"),
)

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
