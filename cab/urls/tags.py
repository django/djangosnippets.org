from django.conf.urls.defaults import *
from cab.views import popular, snippets

urlpatterns = patterns('',
    url(r'^$',
        popular.top_tags,
        name='cab_top_tags'),
    url(r'^(?P<slug>[-\w]+)/$',
        snippets.matches_tag,
        name='cab_snippet_matches_tag'),
)
