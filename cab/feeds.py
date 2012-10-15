from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed

from cab.models import Language, Snippet
from taggit.models import Tag


class LatestSnippetsFeed(Feed):
    """
    Feed of the most recently published Snippets.
    """
    feed_type = Atom1Feed
    title_template = 'cab/feeds/title.html'
    description_template = 'cab/feeds/description.html'
    item_copyright = 'Freely redistributable'
    title = "djangosnippets.org: Latest snippets"
    link = "/snippets/"
    description = "Latest snippets"
    author = "Snippets submitters"

    def item_author_name(self, item):
        return item.author.username

    def items(self):
        return Snippet.objects.all()[:15]

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.pub_date


class SnippetsByAuthorFeed(Feed):
    """
    Feed of the most recent Snippets by a given author.
    """
    feed_type = Atom1Feed
    title_template = 'cab/feeds/title.html'
    description_template = 'cab/feeds/description.html'
    item_copyright = 'Freely redistributable'

    def author_name(self, obj):
        return obj.username

    def get_object(self, request, username=None):
        return get_object_or_404(User, username__exact=username)

    def items(self, obj):
        return Snippet.objects.filter(author=obj)[:15]

    def link(self, obj):
        return "/users/%s/" % obj.username

    def title(self, obj):
        return "djangosnippets.org: Latest snippets posted by %s" % (obj.username)

    def item_author_name(self, item):
        return item.author.username

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.pub_date


class SnippetsByLanguageFeed(Feed):
    """
    Feed of the most recent Snippets in a given language.
    """
    feed_type = Atom1Feed
    title_template = 'cab/feeds/title.html'
    description_template = 'cab/feeds/description.html'
    item_copyright = 'Freely redistributable'

    def get_object(self, request, slug=None):
        return get_object_or_404(Language, slug__exact=slug)

    def items(self, obj):
        return Snippet.objects.filter(language=obj)[:15]

    def link(self, obj):
        return obj.get_absolute_url()

    def title(self, obj):
        return "djangosnippets.org: Latest snippets written in %s" % (obj.name)

    def item_author_name(self, item):
        return item.author.username

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.pub_date


class SnippetsByTagFeed(Feed):
    """
    Feed of the most recent Snippets with a given tag.

    """
    feed_type = Atom1Feed
    title_template = 'cab/feeds/title.html'
    description_template = 'cab/feeds/description.html'
    item_copyright = 'Freely redistributable'

    def get_object(self, request, slug=None):
        return get_object_or_404(Tag, slug__exact=slug)

    def items(self, obj):
        return Snippet.objects.matches_tag(obj)[:15]

    def link(self, obj):
        return reverse('cab_snippet_matches_tag', args=[obj.slug])

    def title(self, obj):
        return "djangosnippets.org: Latest snippets tagged with '%s'" % (obj.name)

    def item_author_name(self, item):
        return item.author.username

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.pub_date
