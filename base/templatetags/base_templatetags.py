from collections.abc import Iterable, Mapping

from django import template
from django.http import QueryDict
from django.template.exceptions import TemplateSyntaxError

register = template.Library()


# This template tag is scheduled to be added in Django 6.0.
# Imported for use before the release of Django 6.0.
@register.simple_tag(name="querystring", takes_context=True)
def querystring(context, *args, **kwargs):
    """
    Build a query string using `args` and `kwargs` arguments.

    This tag constructs a new query string by adding, removing, or modifying
    parameters from the given positional and keyword arguments. Positional
    arguments must be mappings (such as `QueryDict` or `dict`), and
    `request.GET` is used as the starting point if `args` is empty.

    Keyword arguments are treated as an extra, final mapping. These mappings
    are processed sequentially, with later arguments taking precedence.

    A query string prefixed with `?` is returned.

    Raise TemplateSyntaxError if a positional argument is not a mapping or if
    keys are not strings.

    For example::

        {# Set a parameter on top of `request.GET` #}
        {% querystring foo=3 %}

        {# Remove a key from `request.GET` #}
        {% querystring foo=None %}

        {# Use with pagination #}
        {% querystring page=page_obj.next_page_number %}

        {# Use a custom ``QueryDict`` #}
        {% querystring my_query_dict foo=3 %}

        {# Use multiple positional and keyword arguments #}
        {% querystring my_query_dict my_dict foo=3 bar=None %}
    """
    if not args:
        args = [context.request.GET]
    params = QueryDict(mutable=True)
    for d in [*args, kwargs]:
        if not isinstance(d, Mapping):
            msg = f"querystring requires mappings for positional arguments (got {d!r} instead)."
            raise TemplateSyntaxError(
                msg,
            )
        for key, value in d.items():
            if not isinstance(key, str):
                msg = f"querystring requires strings for mapping keys (got {key!r} instead)."
                raise TemplateSyntaxError(
                    msg,
                )
            if value is None:
                params.pop(key, None)
            elif isinstance(value, Iterable) and not isinstance(value, str):
                params.setlist(key, value)
            else:
                params[key] = value
    query_string = params.urlencode() if params else ""
    return f"?{query_string}"
