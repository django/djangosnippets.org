from django.contrib.auth.models import User
from django.db.models import Count, Max
from django.views.generic.base import TemplateView

from cab.models import Snippet


class HomePageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        snippet_stats = Snippet.objects.aggregate(
            total_count=Count("id"),
            max_rating=Max("rating_score"),
            max_bookmarks=Max("bookmark_count"),
        )
        context.update(
            {
                "registered_snippets": snippet_stats["total_count"],
                "total_users": User.objects.count(),
                "highest_rating_cnt": snippet_stats["max_rating"] or 0,
                "highest_bookmark_cnt": snippet_stats["max_bookmarks"] or 0,
            },
        )
        return context
