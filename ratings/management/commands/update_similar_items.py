from django.conf import settings
from django.core.management.base import AppCommand

from ...models import _RatingsDescriptor


class Command(AppCommand):
    help = "Update the similar items table for any or all apps."

    def handle(self, *apps, **options):
        self.verbosity = int(options.get('verbosity', 1))

        if not apps:
            from django.db.models import get_app
            apps = []

            for app in settings.INSTALLED_APPS:
                try:
                    app_label = app.split('.')[-1]
                    get_app(app_label)
                    apps.append(app_label)
                except:
                    pass

        return super(Command, self).handle(*apps, **options)

    def handle_app(self, app, **options):
        from django.db.models import get_models

        for model in get_models(app):
            for k, v in model.__dict__.items():
                if isinstance(v, _RatingsDescriptor):
                    if self.verbosity > 0:
                        print('Updating the %s field of %s' % (k, model))
                    getattr(model, k).update_similar_items()
