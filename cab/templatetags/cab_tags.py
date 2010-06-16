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
