from django import template

from cab.models import Bookmark
from haystack.query import SearchQuerySet

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
def more_like_this(snippet, limit=None):
    try:
        sqs = SearchQuerySet().more_like_this(snippet)
        if limit is not None:
            sqs = sqs[:limit]
    except AttributeError:
        sqs = []
    return sqs
