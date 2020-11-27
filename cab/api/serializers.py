from cab.models import Snippet
from rest_framework import serializers


class SnippetSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    language = serializers.StringRelatedField()

    class Meta:
        model = Snippet
        fields = [
            "title",
            "language",
            "author",
            "description",
            "description_html",
            "code",
            "highlighted_code",
            "version",
            "pub_date",
            "updated_date",
            "bookmark_count",
            "rating_score",
        ]
