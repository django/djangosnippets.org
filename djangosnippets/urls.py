from django.conf.urls.defaults import url, patterns, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.shortcuts import render

from haystack.views import SearchView, search_view_factory

from cab import feeds
from cab.forms import AdvancedSearchForm, RegisterForm
from registration.backends.default.views import RegistrationView

admin.autodiscover()


class CabRegistrationView(RegistrationView):
    form_class = RegisterForm


urlpatterns = patterns('',
    url(r'^captcha/', include('captcha.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/register/$', CabRegistrationView.as_view(),
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bookmarks/', include('cab.urls.bookmarks')),
    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^feeds/author/(?P<username>[\w.@+-]+)/$',
        feeds.SnippetsByAuthorFeed(), name='cab_feed_author'),
    url(r'^feeds/language/(?P<slug>[\w-]+)/$', feeds.SnippetsByLanguageFeed(),
        name='cab_feed_language'),
    url(r'^feeds/latest/$', feeds.LatestSnippetsFeed(),
        name='cab_feed_latest'),
    url(r'^feeds/tag/(?P<slug>[\w-]+)/$', feeds.SnippetsByTagFeed(),
        name='cab_feed_tag'),

    url(r'^languages/', include('cab.urls.languages')),
    url(r'^popular/', include('cab.urls.popular')),
    url(r'^search/$', 'haystack.views.basic_search', name='cab_search'),
    url(r'^search/autocomplete/$', 'cab.views.snippets.autocomplete',
        name='snippet_autocomplete'),
    url(r'^search/advanced/$', search_view_factory(view_class=SearchView,
        template='search/advanced_search.html', form_class=AdvancedSearchForm),
        name='cab_search_advanced'),
    url(r'^snippets/', include('cab.urls.snippets')),
    url(r'^tags/', include('cab.urls.tags')),
    url(r'^users/$', 'cab.views.popular.top_authors', name='cab_top_authors'),
    url(r'^users/(?P<username>[-\w]+)/$', 'cab.views.snippets.author_snippets',
        name='cab_author_snippets'),
    url(r'^$', lambda request: render(request, 'homepage.html')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)
