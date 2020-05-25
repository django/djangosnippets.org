from cab.models import Bookmark, SnippetFlag
from django import template


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
    if not user.is_authenticated:
        return False
    return Bookmark.objects.filter(snippet=snippet, user=user).exists()


@register.filter
def has_flagged(user, snippet):
    if not user.is_authenticated:
        return False
    return SnippetFlag.objects.filter(snippet=snippet, user=user).exists()
