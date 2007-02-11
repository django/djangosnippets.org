"""
Recommended usage is to use a call to ``include()`` in your
project's root URLConf to include this URLConf for any URL
beginning with '/snippets/'.

"""

from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.contrib.auth.models import User
from models import Language, Snippet, Tag
from views import snippets, bookmarks

tag_info_dict = {
    'queryset': Tag.objects.all(),
    'paginate_by': 20,
    }

language_info_dict = {
    'queryset': Language.objects.all(),
    'paginate_by': 20,
    }

user_info_dict = {
    'queryset': User.objects.all(),
    'paginate_by': 20,
    'template_name': 'snippets/user_list.html',
    }

snippet_info_dict = {
    'queryset': Snippet.objects.all(),
    'paginate_by': 20,
    }

urlpatterns = patterns('',
                       (r'^languages/(?P<slug>[\w-]+)', snippets.snippets_by_language),
                       (r'^add/$', snippets.add_snippet),
                       (r'^edit/(?P<snippet_id>\d+)/$', snippets.edit_snippet),
                       (r'^(?P<snippet_id>\d+)/$', snippets.snippet_detail),
                       (r'^rate/(?P<snippet_id>\d+)/$', snippets.rate_snippet),
                       (r'^tags/(?P<slug>[\w-]+)/$', snippets.snippets_by_tag),
                       (r'^users/(?P<username>\w+)/$', snippets.snippets_by_author),
                       )

urlpatterns += patterns('',
                        (r'^bookmarks/$', bookmarks.bookmarks),
                        (r'^bookmarks/add/(?P<snippet_id>\d+)/$', bookmarks.add_bookmark),
                        (r'^bookmarks/author/(?P<author_username>[\w-]+)/$', bookmarks.bookmarks_by_author),
                        (r'^bookmarks/delete/(?P<bookmark_id>\d+)/$', bookmarks.delete_bookmark),
                        (r'^bookmarks/language/(?P<language_slug>[\w-]+)/$', bookmarks.bookmarks_by_language),
                        (r'^bookmarks/tag/(?P<tag_slug>[\w-]+)/$', bookmarks_by_tag),
                        )

urlpatterns += patterns('',
                        (r'^languages/$', object_list, language_info_dict),
                        (r'^$', object_list, snippet_info_dict),
                        (r'^tags/$', object_list, tag_info_dict),
                        (r'^users/$', object_list, user_info_dict),
                        )
