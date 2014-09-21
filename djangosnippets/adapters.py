from allauth.account.adapter import DefaultAccountAdapter


class DjangoSnippetsAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        """Disabling common signup completely"""
        return False
