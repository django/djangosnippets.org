from django.shortcuts import get_object_or_404

from ..models import Language
from ..utils import month_object_list, object_list


def language_list(request):
    if request.htmx:
        return object_list(
            request,
            queryset=Language.objects.all(),
            template_name="cab/partials/language_list.html",
            paginate_by=20,
        )
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
        template_name="cab/language_detail.html",
        extra_context={"language": language},
    )
