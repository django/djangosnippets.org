import re

from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Keyword


class KeywordAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial["fields"] = self.instance.fields.split(",")

    keyword = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "style": "height: 1.5em; line-height: 1.5em; width: 40em;",
                "class": "vLargeTextField",
            },
        ),
    )
    fields = forms.MultipleChoiceField(label=_("Fields to check"), choices=Keyword.FIELD_CHOICES)

    def clean_fields(self):
        return ",".join(self.cleaned_data["fields"])

    def clean(self):
        # Do a test match like the moderator does to ensure that the regular
        # expression is valid.
        if self.cleaned_data["is_regex"]:
            try:
                re.match(self.cleaned_data["keyword"], "", re.MULTILINE)
            except re.error as e:
                msg = _('This regular expression is not valid. Error message was: "%s"') % str(e)
                raise forms.ValidationError(msg) from e
        return self.cleaned_data

    class Meta:
        fields = "__all__"
        model = Keyword


class KeywordAdmin(admin.ModelAdmin):
    form = KeywordAdminForm
    list_display = ("active", "keyword", "fields")
    list_display_links = ("keyword",)
    list_filter = ("active",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "active",
                    ("keyword", "is_regex"),
                    "fields",
                ),
            },
        ),
    )


admin.site.register(Keyword, KeywordAdmin)
