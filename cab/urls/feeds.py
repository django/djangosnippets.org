from django.conf.urls.defaults import url, patterns

from cab import feeds

urlpatterns = patterns('',
    url(r'^author/(?P<username>[\w.@+-]+)/$',
        feeds.SnippetsByAuthorFeed()),
    url(r'^language/(?P<slug>[\w-]+)/$',
        feeds.SnippetsByLanguageFeed()),
    url(r'^latest/$',
        feeds.LatestSnippetsFeed()),
    url(r'^tag/(?P<slug>[\w-]+)/$',
        feeds.SnippetsByTagFeed()),
)
