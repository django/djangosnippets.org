from django.urls import include, path

urlpatterns = [
    path('accounts/', include('allauth.urls')),
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
]
