from django.urls import path

from ..views.snippets import (
    advanced_search_full_text, autocomplete_full_text, basic_search_full_text,
)

urlpatterns = [
    path('', basic_search_full_text, name='cab_search_full_text'),
    path('autocomplete/', autocomplete_full_text, name='snippet_autocomplete_full_text'),
    path('advanced/', advanced_search_full_text, name='cab_search_advanced_full_text'),
]
