import datetime

from django.views.generic.list_detail import object_list


def get_past_datetime(months_ago):
    now = datetime.datetime.now()

    # a little stupid validation here:
    if months_ago < 1 or months_ago > 48:
        return now

    return now - datetime.timedelta(days=months_ago * 31)


def month_object_list(request, queryset, *args, **kwargs):
    extra_context = kwargs.pop('extra_context', {})

    if 'months' in request.GET and request.GET['months'].isdigit():
        months = int(request.GET['months'])
        queryset = queryset.filter(
            pub_date__gt=get_past_datetime(months)
        )
        extra_context['months'] = months

    kwargs['extra_context'] = extra_context

    return object_list(
        request,
        queryset,
        *args,
        **kwargs
    )
