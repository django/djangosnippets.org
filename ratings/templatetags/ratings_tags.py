from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def rating_score(obj, user):
    """
    Returns the score a user has given an object
    """
    if not user.is_authenticated() or not hasattr(obj, '_ratings_field'):
        return False

    ratings_descriptor = getattr(obj, obj._ratings_field)
    try:
        rating = ratings_descriptor.get(user=user).score
    except ratings_descriptor.model.DoesNotExist:
        rating = None

    return rating


@register.filter
def has_rated(user, obj):
    """
    Returns whether or not the user has rated the given object
    """
    return rating_score(obj, user) is not None


@register.filter
def rate_url(obj, score=1):
    """
    Generates a link to "rate" the given object with the provided score - this
    can be used as a form target or for POSTing via Ajax.
    """
    return reverse('ratings_rate_object', args=(
        ContentType.objects.get_for_model(obj).pk,
        obj.pk,
        score,
    ))


@register.filter
def unrate_url(obj):
    """
    Generates a link to "un-rate" the given object - this
    can be used as a form target or for POSTing via Ajax.
    """
    return reverse('ratings_unrate_object', args=(
        ContentType.objects.get_for_model(obj).pk,
        obj.pk,
    ))
