from django.urls import path

from cab.views import snippets

urlpatterns = [
    path("", snippets.snippet_list, name="cab_snippet_list"),
    path("<int:snippet_id>/", snippets.snippet_detail, name="cab_snippet_detail"),
    path("<int:snippet_id>/rate/", snippets.rate_snippet, name="cab_snippet_rate"),
    path(
        "<int:snippet_id>/download/",
        snippets.download_snippet,
        name="cab_snippet_download",
    ),
    path("<int:snippet_id>/raw/", snippets.raw_snippet, name="cab_snippet_raw"),
    path("<int:snippet_id>/edit/", snippets.edit_snippet, name="cab_snippet_edit"),
    path("<int:snippet_id>/flag/", snippets.flag_snippet, name="cab_snippet_flag"),
    path("add/", snippets.edit_snippet, name="cab_snippet_add"),
    path("tag-hint/", snippets.tag_hint, name="cab_snippet_tag_hint"),
]
