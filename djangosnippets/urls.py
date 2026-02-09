from django.contrib import admin
from django.urls import include, path

from .views import HomePageView

admin.autodiscover()


def trigger_sentry_error(request):
    return 1 / 0


urlpatterns = [
    path("sentry-debug/", trigger_sentry_error),
    path("accounts/", include("allauth.urls")),
    path("manage/", admin.site.urls),
    path("components/", include("django_components.urls")),
    path("bookmarks/", include("cab.urls.bookmarks")),
    path("comments/", include("django_comments.urls")),
    path("feeds/", include("cab.urls.feeds")),
    path("languages/", include("cab.urls.languages")),
    path("popular/", include("cab.urls.popular")),
    path("search/", include("cab.urls.search")),
    path("snippets/", include("cab.urls.snippets")),
    path("tags/", include("cab.urls.tags")),
    path("users/", include("cab.urls.users")),
    path("api/", include("cab.api.urls")),
    path("", HomePageView.as_view(), name="home"),
]
