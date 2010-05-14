from django.conf.urls.defaults import *
from cab.views import popular

urlpatterns = patterns('',
    url(r'^authors/$',
        popular.top_authors,
        name='cab_top_authors'),
    url(r'^languages/$',
        popular.top_languages,
        name='cab_top_languages'),
    url(r'^tags/$',
        popular.top_tags,
        name='cab_top_tags'),
    url(r'^bookmarked/$',
        popular.top_bookmarked,
        name='cab_top_bookmarked'),
    url(r'^rated/$',
        popular.top_rated,
        name='cab_top_rated'),
)
