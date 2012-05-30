import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangosnippets.settings.production")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
