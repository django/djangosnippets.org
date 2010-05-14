from django import forms
from cab.models import Snippet

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        exclude = ('author', 'bookmark_count', 'rating_score',)
