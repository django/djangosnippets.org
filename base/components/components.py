from typing import Literal, Optional

from django_components import Component, register
from pydantic import BaseModel

from base.pagination import PAGE_VAR, Pagination
from base.templatetags.base_templatetags import querystring


class PaginationItem(BaseModel):
    kind: Literal["current", "ellipsis", "number"]
    text: Optional[str | int] = None
    attrs: Optional[dict] = None


@register("pagination")
class PaginationComponent(Component):
    template_file = "pagination.html"

    class Kwargs(BaseModel):
        pagination_obj: Pagination
        model_config = {"arbitrary_types_allowed": True}

    def pagination_number(self, pagination: Pagination, num: int) -> PaginationItem:
        """
        Generates a list of `PaginatedItem`, each representing an individual page with
        its associated properties in a pagination navigation list.
        """
        if num == pagination.paginator.ELLIPSIS:
            return PaginationItem(kind="ellipsis", text=pagination.paginator.ELLIPSIS)
        elif num == pagination.page_num:
            return PaginationItem(kind="current", text=num)
        else:
            link = querystring(None, {**pagination.params, PAGE_VAR: num})
            return PaginationItem(
                kind="number",
                text=num,
                attrs={"href": link},
            )

    def get_template_data(self, args, kwargs, slots, context):
        pagination = kwargs.pagination_obj
        page_elements = [self.pagination_number(pagination, page_num) for page_num in pagination.page_range]
        previous_page_link = f"?{PAGE_VAR}={pagination.page_num - 1}" if pagination.page.has_previous() else ""
        next_page_link = f"?{PAGE_VAR}={pagination.page_num + 1}" if pagination.page.has_next() else ""
        return {
            "pagination": pagination,
            "previous_page_link": previous_page_link,
            "next_page_link": next_page_link,
            "page_elements": page_elements,
        }
