from django.conf.urls import url
from haystack.views import SearchView, basic_search, search_view_factory

from ..forms import AdvancedSearchForm
from ..views.snippets import autocomplete

search_view = search_view_factory(view_class=SearchView,
                                  template='search/advanced_search.html',
                                  form_class=AdvancedSearchForm)

urlpatterns = [
    url(r'^$', basic_search, name='cab_search'),
    url(r'^autocomplete/$', autocomplete, name='snippet_autocomplete'),
    url(r'^advanced/$', search_view, name='cab_search_advanced'),
]
