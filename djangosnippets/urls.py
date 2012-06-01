from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.syndication.views import feed

from haystack.views import SearchView, search_view_factory

from cab import feeds
from cab.forms import AdvancedSearchForm, RegisterForm

admin.autodiscover()

feed_dict = {
    'author': feeds.SnippetsByAuthorFeed,
    'language': feeds.SnippetsByLanguageFeed,
    'latest': feeds.LatestSnippetsFeed,
    'tag': feeds.SnippetsByTagFeed,
}

urlpatterns = patterns('',
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/register/$', 'registration.views.register', {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': RegisterForm,
        }, name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bookmarks/', include('cab.urls.bookmarks')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': feed_dict}),
    url(r'^languages/', include('cab.urls.languages')),
    url(r'^popular/', include('cab.urls.popular')),
    url(r'^search/$', 'haystack.views.basic_search', name='cab_search'),
    url(r'^search/autocomplete/$',
        'cab.views.snippets.autocomplete',
        name='snippet_autocomplete',
    ),
    url(r'^search/advanced/$', search_view_factory(
        view_class=SearchView,
        template='search/advanced_search.html',
        form_class=AdvancedSearchForm
    ), name='cab_search_advanced'),
    url(r'^snippets/', include('cab.urls.snippets')),
    url(r'^tags/', include('cab.urls.tags')),
    url(r'^users/$', 'cab.views.popular.top_authors', name='cab_top_authors'),
    url(r'^users/(?P<username>[-\w]+)/$', 'cab.views.snippets.author_snippets', name='cab_author_snippets'),
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'homepage.html'}),
    url(r'^%s/(?P<path>.*)$' % settings.STATIC_URL.strip('/'),
        'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
)
