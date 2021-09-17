from django.urls import path

from ..views.snippets import advanced_search, autocomplete, basic_search

urlpatterns = [
    path("", basic_search, name="cab_search"),
    path("autocomplete/", autocomplete, name="snippet_autocomplete"),
    path("advanced/", advanced_search, name="cab_search_advanced"),
]
