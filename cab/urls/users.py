from django.conf.urls import url

from ..views import popular, snippets

urlpatterns = [
    url(r'^$',
        popular.top_authors,
        name='cab_top_authors'),
    url(r'^(?P<username>[\w.@+-]+)/$',
        snippets.author_snippets,
        name='cab_author_snippets'),
]
