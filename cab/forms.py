from django import forms
from django.contrib import admin
from django.contrib.postgres.search import SearchVector 
from haystack.forms import SearchForm

from .models import VERSIONS, Language, Snippet, SnippetFlag


def validate_non_whitespace_only_string(value):
    """
    Additionally to requiring a non-empty string, this validator also strips
    the string to treat strings with only whitespaces in them as empty.
    """
    if not value or not value.strip():
        raise forms.ValidationError(u'This field is required', code='required')


class SnippetForm(forms.ModelForm):
    title = forms.CharField(
        validators=[validate_non_whitespace_only_string])
    description = forms.CharField(
        validators=[validate_non_whitespace_only_string],
        widget=forms.Textarea)
    code = forms.CharField(
        validators=[validate_non_whitespace_only_string],
        widget=forms.Textarea)

    class Meta:
        model = Snippet
        exclude = ('author', 'bookmark_count', 'rating_score',)


class SnippetFlagForm(forms.ModelForm):
    class Meta:
        model = SnippetFlag
        fields = ('flag',)


class AdvancedSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Search',
                        widget=forms.TextInput(attrs={'type': 'search'}))
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), required=False)
    version = forms.MultipleChoiceField(choices=VERSIONS, required=False)
    minimum_pub_date = forms.DateTimeField(
        widget=admin.widgets.AdminDateWidget, required=False)
    minimum_bookmark_count = forms.IntegerField(required=False)
    minimum_rating_score = forms.IntegerField(required=False)

    