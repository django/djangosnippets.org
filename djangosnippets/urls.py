from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

from cab.views.snippets import twitter_img

admin.autodiscover()


def trigger_sentry_error(request):
    division_by_zero = 1 / 0
    return division_by_zero


urlpatterns = [
    path('sentry-debug/', trigger_sentry_error),
    path('accounts/', include('allauth.urls')),
    path('manage/', admin.site.urls),
    path('bookmarks/', include('cab.urls.bookmarks')),
    path('comments/', include('django_comments.urls')),
    path('feeds/', include('cab.urls.feeds')),
    path('languages/', include('cab.urls.languages')),
    path('popular/', include('cab.urls.popular')),
    path('search/', include('cab.urls.search')),
    path('snippets/', include('cab.urls.snippets')),
    path('tags/', include('cab.urls.tags')),
    path('users/', include('cab.urls.users')),
    path('api/', include('cab.api.urls')),

    path('', lambda request: render(request, 'homepage.html'), name='home'),
    path("test-image", twitter_img, name="twitter_img")
]
