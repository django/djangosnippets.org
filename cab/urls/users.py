from django.urls import path

from cab.views import popular, snippets

urlpatterns = [
    path("", popular.top_authors, name="cab_top_authors"),
    path("<username>/", snippets.author_snippets, name="cab_author_snippets"),
]
