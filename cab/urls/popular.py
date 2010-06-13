from django.conf.urls.defaults import *
from cab.views import popular

urlpatterns = patterns('',
    url(r'^languages/$',
        popular.top_languages,
        name='cab_top_languages'),
    url(r'^bookmarked/$',
        popular.top_bookmarked,
        name='cab_top_bookmarked'),
    url(r'^rated/$',
        popular.top_rated,
        name='cab_top_rated'),
)
