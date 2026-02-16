from allauth.account.forms import LoginForm


class DjangoSnippetsLoginForm(LoginForm):

    def _setup_password_field(self):
        super()._setup_password_field()
        # Disable allauth's automatically set help_text
        self.fields["password"].help_text = None
