from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class DjangoSnippetsSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        """
        Explicitely enabling it since we want social account signups.
        """
        return True
