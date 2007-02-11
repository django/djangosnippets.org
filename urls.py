"""
URLConf for Cab.

Recommended usage is to use a call to ``include()`` in your
project's root URLConf to include this URLConf for any URL
beginning with '/snippets/'.

"""

from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.contrib.auth.models import User
from models import Language, Snippet, Tag
from views import bookmarks, snippets

# Info for generic views.
base_generic_dict = {
    'paginate_by': 20,
    }

language_info_dict = dict(base_generic_dict,
                          queryset=Language.objects.all())

snippet_info_dict = dict(base_generic_dict,
                         queryset=Snippet.objects.all())

tag_info_dict = dict(base_generic_dict,
                     queryset=Tag.objects.all())

user_info_dict = dict(base_generic_dict,
                      queryset=User.objects.all(),
                      template_name='snippets/user_list.html')

# General snippets views.
urlpatterns = patterns('',
                       (r'^(?P<snippet_id>\d+)/$', snippets.snippet_detail),
                       (r'^add/$', snippets.add_snippet),
                       (r'^edit/(?P<snippet_id>\d+)/$', snippets.edit_snippet),
                       (r'^languages/(?P<slug>[\w-]+)', snippets.snippets_by_language),
                       (r'^rate/(?P<snippet_id>\d+)/$', snippets.rate_snippet),
                       (r'^tags/(?P<slug>[\w-]+)/$', snippets.snippets_by_tag),
                       (r'^users/(?P<username>\w+)/$', snippets.snippets_by_author),
                       )

# Views that work with bookmarks.
urlpatterns += patterns('',
                        (r'^bookmarks/$', bookmarks.bookmarks),
                        (r'^bookmarks/add/(?P<snippet_id>\d+)/$', bookmarks.add_bookmark),
                        (r'^bookmarks/author/(?P<author_username>[\w-]+)/$', bookmarks.bookmarks_by_author),
                        (r'^bookmarks/delete/(?P<bookmark_id>\d+)/$', bookmarks.delete_bookmark),
                        (r'^bookmarks/language/(?P<language_slug>[\w-]+)/$', bookmarks.bookmarks_by_language),
                        (r'^bookmarks/tag/(?P<tag_slug>[\w-]+)/$', bookmarks.bookmarks_by_tag),
                        )

# Generic views.
urlpatterns += patterns('',
                        (r'^$', object_list, snippet_info_dict),
                        (r'^languages/$', object_list, language_info_dict),
                        (r'^tags/$', object_list, tag_info_dict),
                        (r'^users/$', object_list, user_info_dict),
                        )
