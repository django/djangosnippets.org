
from cab.models import Snippet
from cab.api.serializers import SnippetSerializer
from rest_framework import generics


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
