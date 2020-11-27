from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import SnippetDetail, SnippetList

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("snippets/", SnippetList.as_view(), name="api_snippet_list"),
    path("snippets/<int:pk>/", SnippetDetail.as_view(), name="api_snippet_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
