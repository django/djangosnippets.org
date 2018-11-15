from django.urls import path

from ..views import popular, snippets

urlpatterns = [
    path('', popular.top_tags, name='cab_top_tags'),
    path('<slug:slug>/', snippets.matches_tag, name='cab_snippet_matches_tag'),
]
