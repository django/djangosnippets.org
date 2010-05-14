from django.conf.urls.defaults import *
from cab.views import languages

urlpatterns = patterns('',
    url(r'^$',
        languages.language_list,
        name='cab_language_list'),
    url(r'^(?P<slug>[-\w]+)/$',
        languages.language_detail,
        name='cab_language_detail'),
)
