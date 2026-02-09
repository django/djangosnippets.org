from django.contrib.auth.models import User
from django.views.generic.base import TemplateView

from cab.models import Snippet


class HomePageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "registered_snippets": Snippet.objects.count(),
                "total_users": User.objects.count(),
                "top_rated_snippet": Snippet.objects.order_by("-rating_score").first(),
                "top_bookmarked_snippet": Snippet.objects.order_by("-bookmark_count").first(),
            },
        )

        return context
