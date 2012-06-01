from django import forms
from django.contrib.comments.forms import CommentForm


class CapCommentForm(CommentForm):
    name = forms.CharField(label='Your Name', required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    def clean(self):
        if self.cleaned_data.get('name'):
            raise forms.ValidationError('Please keep the Name field blank')
        return self.cleaned_data
