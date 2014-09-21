from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class DjangoSnippetsAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        """Disabling common signup completely"""
        return False


class DjangoSnippetsSocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        """
        Explicitely enabling it since we want social account signups.
        """
        return True
