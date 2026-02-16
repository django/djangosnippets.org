from typing import Literal

from django_components import Component, register
from pydantic import BaseModel, EmailStr

from base.main import TAB_VAR, ObjectList
from base.pagination import PAGE_VAR, Pagination
from base.templatetags.base_templatetags import querystring


@register("icon")
class Icon(Component):
    class Kwargs(BaseModel):
        kind: Literal["heart", "bookmark"]
        color: str
        label: str

    template_file = "icon.html"

    def get_template_data(self, args, kwargs, slots, context):
        return {
            "kind": kwargs.kind,
            "label": kwargs.label,
            "color": kwargs.color,
            "classes": "w-[18px] h-[18px]",
        }


class PaginationItem(BaseModel):
    kind: Literal["current", "ellipsis", "number"]
    text: str | int | None = None
    attrs: dict | None = None


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
            return PaginationItem(kind="ellipsis", text=str(pagination.paginator.ELLIPSIS))
        if num == pagination.page_num:
            return PaginationItem(kind="current", text=num)
        link = querystring(None, {**pagination.params, PAGE_VAR: num})
        return PaginationItem(
            kind="number",
            text=num,
            attrs={"href": link},
        )

    def get_template_data(self, args, kwargs, slots, context):
        pagination = kwargs.pagination_obj
        page_elements = [
            self.pagination_number(pagination, page_num) for page_num in pagination.page_range
        ]
        previous_page_link = (
            f"?{PAGE_VAR}={pagination.page_num - 1}" if pagination.page.has_previous() else ""
        )
        next_page_link = (
            f"?{PAGE_VAR}={pagination.page_num + 1}" if pagination.page.has_next() else ""
        )
        return {
            "pagination": pagination,
            "previous_page_link": previous_page_link,
            "next_page_link": next_page_link,
            "page_elements": page_elements,
        }


class TabItem(BaseModel):
    text: str
    is_current: bool
    attrs: dict | None


@register("sorting_tabs")
class SortingTabs(Component):
    template_file = "sorting_tabs.html"

    class Kwargs(BaseModel):
        object_list: ObjectList
        model_config = {"arbitrary_types_allowed": True}

    def create_tab(self, object_list: ObjectList, tab: str) -> TabItem:
        verbose_text = tab.replace("_", " ").title()
        is_current = tab == object_list.current_tab
        link = querystring(None, {**object_list.params, TAB_VAR: tab})
        attrs = {"href": link}
        if is_current:
            attrs["aria-selected"] = "true"
        return TabItem(text=verbose_text, is_current=is_current, attrs=attrs)

    def create_all_tabs(self, object_list: ObjectList):
        return [self.create_tab(object_list, tab) for tab in object_list.sorting_tabs]

    def get_template_data(self, args, kwargs, slots, context):
        object_list = kwargs.object_list
        return {
            "tabs": self.create_all_tabs(object_list),
            "object_list": object_list,
        }


@register("contact_information_button")
class ContactInformationButton(Component):
    MAINTAINER_EMAILS = [
        "antoliny0919@gmail.com",
        "wedgemail@gmail.com",
    ]
    template_file = "contact_information_button.html"

    class Kwargs(BaseModel):
        button_text: str
        description: str
        contact_emails: list[EmailStr] | None = None

    def get_template_data(self, args, kwargs, slots, context):
        contact_emails = kwargs.contact_emails or self.MAINTAINER_EMAILS
        return {
            "button_text": kwargs.button_text,
            "description": kwargs.description,
            "contact_emails": contact_emails,
        }
