from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, Http404,
)
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.http import is_safe_url


# allow GET requests to create ratings -- this goes against the "GET" requests
# should be idempotent but avoids the necessity of using <form> elements or
# javascript to create rating links
ALLOW_GET = getattr(settings, 'RATINGS_ALLOW_GET', True)


@login_required
def rate_object(request, ct, pk, score=1, add=True):
    if request.method != 'POST' and not ALLOW_GET:
        return HttpResponseNotAllowed('Invalid request method: "%s". '
                                      'Must be POST.' % request.method)

    redirect_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
    if redirect_url and not is_safe_url(redirect_url):
        return HttpResponseBadRequest("Invalid next URL.")
    if not redirect_url:
        redirect_url = '/'

    ctype = get_object_or_404(ContentType, pk=ct)
    model_class = ctype.model_class()

    if not hasattr(model_class, '_ratings_field'):
        raise Http404('Model class %s does not support ratings' % model_class)

    obj = get_object_or_404(model_class, pk=pk)

    ratings_descriptor = getattr(obj, obj._ratings_field)

    if add:
        score = '.' in score and float(score) or int(score)
        ratings_descriptor.rate(request.user, score)
    else:
        ratings_descriptor.unrate(request.user)

    if request.is_ajax():
        return HttpResponse('{"success": true}', content_type='application/json')
    return HttpResponseRedirect(redirect_url)
