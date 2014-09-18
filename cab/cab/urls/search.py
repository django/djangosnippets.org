from django.conf.urls import url, patterns
from cab.forms import AdvancedSearchForm

from haystack.views import SearchView, search_view_factory

search_view = search_view_factory(view_class=SearchView,
                                  template='search/advanced_search.html',
                                  form_class=AdvancedSearchForm)

urlpatterns = patterns('',
    url(r'^$',
        'haystack.views.basic_search',
        name='cab_search'),
    url(r'^autocomplete/$',
        'cab.views.snippets.autocomplete',
        name='snippet_autocomplete'),
    url(r'^advanced/$',
        search_view,
        name='cab_search_advanced'),
)
