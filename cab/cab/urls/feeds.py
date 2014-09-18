from django.conf.urls import url, patterns

from cab import feeds

urlpatterns = patterns('',
    url(r'^author/(?P<username>[\w.@+-]+)/$',
        feeds.SnippetsByAuthorFeed(), name='cab_feed_author'),
    url(r'^language/(?P<slug>[\w-]+)/$',
        feeds.SnippetsByLanguageFeed(), name='cab_feed_language'),
    url(r'^latest/$',
        feeds.LatestSnippetsFeed(), name='cab_feed_latest'),
    url(r'^tag/(?P<slug>[\w-]+)/$',
        feeds.SnippetsByTagFeed(), name='cab_feed_tag'),
)
