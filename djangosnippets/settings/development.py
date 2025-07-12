from djangosnippets.settings.base import *  # noqa: F403

DEBUG = True

SECRET_KEY = "abcdefghijklmnopqrstuvwxyz0123456789"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CACHE_BACKEND = "dummy://"

INSTALLED_APPS = INSTALLED_APPS

TEMPLATES[0]["OPTIONS"]["loaders"] = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
    "django_components.template_loader.Loader",
]
