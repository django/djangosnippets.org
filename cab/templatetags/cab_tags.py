from django import template

from cab.models import Bookmark

register = template.Library()

@register.filter
def is_bookmarked(snippet, user):
    """
    {% if snippet|is_bookmarked:request.user %}
        already bookmarked
    {% else %}
        not bookmarked yet
    {% endif %}
    """
    if not user.is_authenticated():
        return False
    return bool(Bookmark.objects.filter(snippet=snippet, user=user).count())

@register.filter
def is_rated(snippet, user):
    """
    {% if snippet|is_rated:request.user %}
        already rated
    {% else %}
        not rated yet
    {% endif %}
    """
    if not user.is_authenticated():
        return False
    return bool(snippet.ratings.filter(user=user).count())
