from django.conf.urls.defaults import *
from cab.views import bookmarks

urlpatterns = patterns('',
    url(r'^$',
        bookmarks.user_bookmarks,
        name='cab_user_bookmarks'),
    url(r'^add/(?P<snippet_id>\d+)/$',
        bookmarks.add_bookmark,
        name='cab_bookmark_add'),
    url(r'^delete/(?P<snippet_id>\d+)/$',
        bookmarks.delete_bookmark,
        name='cab_bookmark_delete'),
)
