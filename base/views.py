from allauth.account.views import EmailVerificationSentView


class DjangoSnippetsEmailVerificationSentView(EmailVerificationSentView):
    MAINTAINER_EMAILS = [
        "antoliny0919@gmail.com",
        "wedgemail@gmail.com",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["maintainer_emails"] = self.MAINTAINER_EMAILS
        return context
