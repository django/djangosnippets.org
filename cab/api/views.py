from rest_framework import generics

from ..models import Snippet
from .serializers import SnippetSerializer


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.active_snippet()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateAPIView):
    queryset = Snippet.objects.active_snippet()
    serializer_class = SnippetSerializer
