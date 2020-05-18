from django.urls import path
from haystack.views import SearchView,  search_view_factory

from ..forms import AdvancedSearchForm
from ..views.snippets import autocomplete, advanced_search,search

search_view = search_view_factory(view_class=SearchView,
                                  template='search/advanced_search.html',
                                  form_class=AdvancedSearchForm)

urlpatterns = [
    path('', search, name='cab_search'),
    path('autocomplete/', autocomplete, name='snippet_autocomplete'),
    path('advanced/', advanced_search, name='cab_search_advanced'),
]
