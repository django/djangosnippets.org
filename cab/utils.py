import datetime

import bleach
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404, HttpResponse
from django.template import loader
from django.utils.safestring import mark_safe
from markdown import markdown as markdown_func


def object_list(
    request,
    queryset,
    paginate_by=None,
    page=None,
    allow_empty=True,
    template_name=None,
    template_loader=loader,
    extra_context=None,
    template_object_name="object",
    content_type=None,
):
    """
    Generic list of objects.

    Templates: ``<app_label>/<model_name>_list.html``
    Context:
        object_list
            list of objects
        is_paginated
            are the results paginated?
        results_per_page
            number of objects per page (if paginated)
        has_next
            is there a next page?
        has_previous
            is there a prev page?
        page
            the current page
        next
            the next page
        previous
            the previous page
        pages
            number of pages, total
        hits
            number of objects, total
        last_on_page
            the result number of the last of object in the
            object_list (1-indexed)
        first_on_page
            the result number of the first object in the
            object_list (1-indexed)
        page_range:
            A list of the page numbers (1-indexed).
    """
    if extra_context is None:
        extra_context = {}
    queryset = queryset._clone()
    if paginate_by:
        paginator = Paginator(queryset, paginate_by, allow_empty_first_page=allow_empty)
        if not page:
            page = request.GET.get("page", 1)

        if page == "last":
            page_number = paginator.num_pages
        else:
            try:
                page_number = int(page)
            except ValueError:
                # Page is not 'last', nor can it be converted to an int.
                raise Http404
        try:
            page_obj = paginator.page(page_number)
        except InvalidPage:
            raise Http404
        try:
            next_page = page_obj.next_page_number()
        except InvalidPage:
            next_page = None
        try:
            previous_page = page_obj.previous_page_number()
        except InvalidPage:
            previous_page = None

        c = {
            "%s_list" % template_object_name: page_obj.object_list,
            "paginator": paginator,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            # Legacy template context stuff. New templates should use page_obj
            # to access this instead.
            "results_per_page": paginator.per_page,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "page": page_obj.number,
            "next": next_page,
            "previous": previous_page,
            "first_on_page": page_obj.start_index(),
            "last_on_page": page_obj.end_index(),
            "pages": paginator.num_pages,
            "hits": paginator.count,
            "page_range": paginator.page_range,
        }
    else:
        c = {
            "%s_list" % template_object_name: queryset,
            "paginator": None,
            "page_obj": None,
            "is_paginated": False,
        }
        if not allow_empty and len(queryset) == 0:
            raise Http404

    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    if not template_name:
        model = queryset.model
        template_name = "%s/%s_list.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    return HttpResponse(t.render(c, request=request), content_type=content_type)


def object_detail(
    request,
    queryset,
    object_id=None,
    slug=None,
    slug_field="slug",
    template_name=None,
    template_name_field=None,
    template_loader=loader,
    extra_context=None,
    context_processors=None,
    template_object_name="object",
    content_type=None,
):
    """
    Generic detail of an object.

    Templates: ``<app_label>/<model_name>_detail.html``
    Context:
        object
            the object
    """
    if extra_context is None:
        extra_context = {}
    model = queryset.model
    if not object_id or (slug and slug_field):
        raise AttributeError("Generic detail view must be called with either " "an object_id or a slug/slug_field.")
    if object_id:
        queryset = queryset.filter(pk=object_id)
    elif slug and slug_field:
        queryset = queryset.filter(**{slug_field: slug})

    try:
        obj = queryset.get()
    except ObjectDoesNotExist:
        raise Http404("No %s found matching the query" % model._meta.verbose_name)
    if not template_name:
        template_name = "%s/%s_detail.html" % (model._meta.app_label, model._meta.object_name.lower())
    if template_name_field:
        template_name_list = [getattr(obj, template_name_field), template_name]
        t = template_loader.select_template(template_name_list)
    else:
        t = template_loader.get_template(template_name)
    c = {
        template_object_name: obj,
    }
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    response = HttpResponse(t.render(c, request=request), content_type=content_type)
    return response


def get_past_datetime(months_ago):
    now = datetime.datetime.now()

    # a little stupid validation here:
    if months_ago < 1 or months_ago > 48:
        return now

    return now - datetime.timedelta(days=months_ago * 31)


def month_object_list(request, queryset, *args, **kwargs):
    extra_context = kwargs.pop("extra_context", {})

    if "months" in request.GET and request.GET["months"].isdigit():
        months = int(request.GET["months"])
        queryset = queryset.filter(pub_date__gt=get_past_datetime(months))
        extra_context["months"] = months

    kwargs["extra_context"] = extra_context

    return object_list(request, queryset, *args, **kwargs)


def sanitize_markdown(value):
    return mark_safe(
        bleach.clean(
            markdown_func(value),
            tags=[
                "a",
                "abbr",
                "acronym",
                "b",
                "blockquote",
                "code",
                "em",
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "i",
                "li",
                "ol",
                "p",
                "pre",
                "strong",
                "ul",
            ],
        )
    )
