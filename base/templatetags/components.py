from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from base.pagination import PAGE_VAR

from .base_templatetags import querystring

register = template.Library()


@register.simple_tag
def pagination_number(pagination, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == pagination.paginator.ELLIPSIS:
        return format_html("{} ", pagination.paginator.ELLIPSIS)
    elif i == pagination.page_num:
        return format_html('<em class="current-page" aria-current="page">{}</em> ', i)
    else:
        link = querystring(None, pagination.params, {PAGE_VAR: i})
        return format_html(
            '<a href="{}" aria-label="page {}" {}>{}</a> ',
            link,
            i,
            mark_safe(' class="end"' if i == pagination.paginator.num_pages else ""),
            i,
        )


@register.inclusion_tag("base/components/pagination.html", name="pagination")
def pagination_tag(pagination):
    previous_page_link = f"?{PAGE_VAR}={pagination.page_num - 1}"
    next_page_link = f"?{PAGE_VAR}={pagination.page_num + 1}"
    return {
        "pagination": pagination,
        "previous_page_link": previous_page_link,
        "next_page_link": next_page_link,
    }
