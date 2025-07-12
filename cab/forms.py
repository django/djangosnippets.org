from django import forms
from django.contrib import admin

from .models import VERSIONS, Language, Snippet, SnippetFlag


def validate_non_whitespace_only_string(value):
    """
    Additionally to requiring a non-empty string, this validator also strips
    the string to treat strings with only whitespaces in them as empty.
    """
    if not value or not value.strip():
        raise forms.ValidationError("This field is required", code="required")


class SnippetForm(forms.ModelForm):
    title = forms.CharField(validators=[validate_non_whitespace_only_string])
    description = forms.CharField(validators=[validate_non_whitespace_only_string], widget=forms.Textarea)
    code = forms.CharField(validators=[validate_non_whitespace_only_string], widget=forms.Textarea)

    class Meta:
        model = Snippet
        exclude = (
            "author",
            "bookmark_count",
            "rating_score",
        )


class SnippetFlagForm(forms.ModelForm):
    class Meta:
        model = SnippetFlag
        fields = ("flag",)


class AdvancedSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Search", widget=forms.TextInput(attrs={"type": "search"}))
    language = forms.ModelChoiceField(queryset=Language.objects.all(), required=False)
    version = forms.MultipleChoiceField(choices=VERSIONS, required=False)
    minimum_pub_date = forms.DateTimeField(widget=admin.widgets.AdminDateWidget, required=False)
    minimum_bookmark_count = forms.IntegerField(required=False)
    minimum_rating_score = forms.IntegerField(required=False)

    def search(self, sqs):
        # First, store the SearchQuerySet received from other processing.
        if self.cleaned_data["q"]:
            sqs = sqs.filter(search=self.cleaned_data["q"])

        if self.cleaned_data["language"]:
            sqs = sqs.filter(language__name=self.cleaned_data["language"].name)

        if self.cleaned_data["version"]:
            sqs = sqs.filter(version__in=self.cleaned_data["version"])

        if self.cleaned_data["minimum_pub_date"]:
            sqs = sqs.filter(pub_date__gte=self.cleaned_data["minimum_pub_date"])

        if self.cleaned_data["minimum_bookmark_count"]:
            sqs = sqs.filter(bookmark_count__gte=self.cleaned_data["minimum_bookmark_count"])

        if self.cleaned_data["minimum_rating_score"]:
            sqs = sqs.filter(rating_score__gte=self.cleaned_data["minimum_rating_score"])

        return sqs
