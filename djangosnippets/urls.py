from django.conf.urls.defaults import url, patterns, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.shortcuts import render

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^captcha/', include('captcha.urls')),
    url(r'^accounts/', include('cab.urls.accounts')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bookmarks/', include('cab.urls.bookmarks')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^feeds/', include('cab.urls.feeds')),
    url(r'^languages/', include('cab.urls.languages')),
    url(r'^popular/', include('cab.urls.popular')),
    url(r'^search/', include('cab.urls.search')),
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
