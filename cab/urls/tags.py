from django.conf.urls import url

from ..views import popular, snippets

urlpatterns = [
    url(r'^$',
        popular.top_tags,
        name='cab_top_tags'),
    url(r'^(?P<slug>[-\w]+)/$',
        snippets.matches_tag,
        name='cab_snippet_matches_tag'),
]
