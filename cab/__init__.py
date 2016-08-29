def get_form():
    from django import forms
    from django_comments.forms import CommentForm

    from captcha.fields import ReCaptchaField

    class CabCommentForm(CommentForm):
        your_name = forms.CharField(
            label='Your Name', required=False,
            widget=forms.TextInput(attrs={'autocomplete': 'off'}),
        )
        captcha = ReCaptchaField(attrs={'theme': 'clean'})

        def clean(self):
            if self.cleaned_data.get('your_name'):
                raise forms.ValidationError('Please keep the Name field blank')
            return self.cleaned_data

    return CabCommentForm
