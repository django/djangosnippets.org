from django.conf.urls import patterns, url
from cab.views import popular, snippets

urlpatterns = patterns('',
    url(r'^$',
        popular.top_authors,
        name='cab_top_authors'),
    url(r'^(?P<username>[\w.@+-]+)/$',
        snippets.author_snippets,
        name='cab_author_snippets'),
)
