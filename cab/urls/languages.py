from django.conf.urls import url

from ..views import languages

urlpatterns = [
    url(r'^$',
        languages.language_list,
        name='cab_language_list'),
    url(r'^(?P<slug>[-\w]+)/$',
        languages.language_detail,
        name='cab_language_detail'),
]
