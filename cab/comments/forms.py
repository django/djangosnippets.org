from django import forms
from django.contrib.comments.forms import CommentForm
from captcha.fields import CaptchaField


class CabCommentForm(CommentForm):
    your_name = forms.CharField(label='Your Name', required=False,
                                widget=forms.TextInput(attrs={
                                    'autocomplete': 'off',
                                }))
    captcha = CaptchaField()

    def clean(self):
        if self.cleaned_data.get('your_name'):
            raise forms.ValidationError('Please keep the Name field blank')
        return self.cleaned_data
