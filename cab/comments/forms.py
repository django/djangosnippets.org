from django import forms
from django.contrib.comments.forms import CommentForm


class CapCommentForm(CommentForm):
    pass

    your_name = forms.CharField(label='Your Name', required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    def clean(self):
        if self.cleaned_data.get('your_name'):
            raise forms.ValidationError('Please keep the Name field blank')
        return self.cleaned_data