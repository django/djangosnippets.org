import datetime

import bleach
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.template import loader
from django.utils.safestring import mark_safe
from markdown import markdown as markdown_func

from base.pagination import Pagination


def object_list(
    request,
    queryset,
    paginate_by=None,
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
        pagination
            This is a pagination object that holds attributes
            related to pagination.
            For more detail, please refer to the `base.pagination.Pagination` class.
        hits
            number of objects, total
    """
    if extra_context is None:
        extra_context = {}
    queryset = queryset._clone()
    model = queryset.model
    opts = model._meta
    if paginate_by:
        pagination = Pagination(request, model, queryset, paginate_by)
        object_list = pagination.get_objects()

        context = {
            "%s_list" % template_object_name: object_list,
            "pagination": pagination,
            "hits": pagination.result_count,
        }
    else:
        context = {
            "%s_list" % template_object_name: object_list,
        }
        if not allow_empty and len(queryset) == 0:
            raise Http404

    for key, value in extra_context.items():
        if callable(value):
            context[key] = value()
        else:
            context[key] = value
    if not template_name:
        template_name = "%s/%s_list.html" % (opts.app_label, opts.object_name.lower())
    template = template_loader.get_template(template_name)
    return HttpResponse(template.render(context, request=request), content_type=content_type)


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
