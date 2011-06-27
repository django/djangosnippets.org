from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from cab.models import Language
from cab.utils import month_object_list


def language_list(request):
    return object_list(
        request,
        queryset=Language.objects.all(),
        paginate_by=20,
    )

def language_detail(request, slug):
    language = get_object_or_404(Language, slug=slug)
    return month_object_list(
        request,
        queryset=language.snippet_set.all(),
        paginate_by=20,
        template_name='cab/language_detail.html',
        extra_context={'language': language},
    )
