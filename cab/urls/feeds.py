from django.urls import path

from cab import feeds

urlpatterns = [
    path("author/<username>/", feeds.SnippetsByAuthorFeed(), name="cab_feed_author"),
    path(
        "language/<slug:slug>/",
        feeds.SnippetsByLanguageFeed(),
        name="cab_feed_language",
    ),
    path("latest/", feeds.LatestSnippetsFeed(), name="cab_feed_latest"),
    path("tag/<slug:slug>/", feeds.SnippetsByTagFeed(), name="cab_feed_tag"),
]
