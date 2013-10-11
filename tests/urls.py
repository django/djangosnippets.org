from django.conf.urls import patterns, url, include

from cab import feeds

urlpatterns = patterns('',
    url(r'^bookmarks/', include('cab.urls.bookmarks')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^feeds/author/(?P<username>[-\w]+)/$', feeds.SnippetsByAuthorFeed()),
    url(r'^feeds/language/(?P<slug>[-\w]+)/$', feeds.SnippetsByLanguageFeed()),
    url(r'^feeds/latest/$', feeds.LatestSnippetsFeed()),
    url(r'^feeds/tag/(?P<slug>[-\w]+)/$', feeds.SnippetsByTagFeed()),
    url(r'^languages/', include('cab.urls.languages')),
    url(r'^popular/', include('cab.urls.popular')),
    #url(r'^search/', include('haystack.urls')),
    #url(r'^search/$', 'haystack.views.basic_search', name='cab_search'),
    url(r'^search/$', 'cab.views.snippets.search', name='cab_search'),
    url(r'^snippets/', include('cab.urls.snippets')),
    url(r'^tags/', include('cab.urls.tags')),
    url(r'^users/$', 'cab.views.popular.top_authors', name='cab_top_authors'),
    url(r'^users/(?P<username>[-\w]+)/$', 'cab.views.snippets.author_snippets', name='cab_author_snippets'),
)
