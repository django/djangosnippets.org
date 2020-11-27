from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SnippetList, SnippetDetail


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("snippets/", SnippetList.as_view()),
    path("snippets/<int:pk>/", SnippetDetail.as_view()),
  
]

urlpatterns = format_suffix_patterns(urlpatterns)
