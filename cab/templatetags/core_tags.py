from django.db.models.loading import get_model
from django.db.models.query import QuerySet
from django.db.models.fields import DateTimeField, DateField
from django import template

register = template.Library()

@register.filter
def latest(model_or_obj, num=5):
    # load up the model if we were given a string
    if isinstance(model_or_obj, basestring):
        model_or_obj = get_model(*model_or_obj.split('.'))

    # figure out the manager to query
    if isinstance(model_or_obj, QuerySet):
        manager = model_or_obj
        model_or_obj = model_or_obj.model
    else:
        manager = model_or_obj._default_manager

    # get a field to order by, defaulting to the primary key
    field_name = model_or_obj._meta.pk.name
    for field in model_or_obj._meta.fields:
        if isinstance(field, (DateTimeField, DateField)):
            field_name = field.name
            break
    return manager.all().order_by('-%s' % field_name)[:num]

@register.filter
def call_manager(model_or_obj, method):
    # load up the model if we were given a string
    if isinstance(model_or_obj, basestring):
        model_or_obj = get_model(*model_or_obj.split('.'))

    # figure out the manager to query
    if isinstance(model_or_obj, QuerySet):
        manager = model_or_obj
        model_or_obj = model_or_obj.model
    else:
        manager = model_or_obj._default_manager

    return getattr(manager, method)()
