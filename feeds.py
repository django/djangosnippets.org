from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from models import Language, Snippet, Tag

current_site = Site.objects.get_current().name

class BaseSnippetsFeed(Feed):
    """
    Base feed class setting some common things which all the snippets
    feeds will want to inherit.
    
    """
    feed_type = Atom1Feed
    title_template = 'cab/feeds/title.html'
    description_template = 'cab/feeds/description.html'
    item_copyright = 'Freely redistributable'


class ByRelatedItemFeed(BaseFeed):
    """
    Base class for feeds which filter by related items.
    
    """
    def item_author_name(self, item):
        return item.author.username
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.pub_date

    
class LatestSnippetsFeed(BaseSnippetsFeed):
    """
    Feed of the most recently published Snippets.
    
    """
    title = "%s: Latest snippets" % current_site
    link = "/snippets/"
    description = "Latest snippets"
    author = "Snippets submitters"
    
    def item_author_name(self, item):
        return item.author.username
    
    def items(self):
        return Snippet.objects.all()[:15]


class SnippetsByAuthorFeed(ByRelatedItemFeed):
    """
    Feed of the most recent Snippets by a given author.
    
    """
    def author_name(self, obj):
        return obj.username
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username__exact=bits[0])
    
    def items(self, obj):
        return Snippet.objects.get_by_author(obj.username)[:15]
    
    def link(self, obj):
        return "/users/%s/" % obj.username

    def title(self, obj):
        return "%s: Latest snippets posted by %s" % (current_site, obj.username)


class SnippetsByLanguageFeed(ByRelatedItemFeed):
    """
    Feed of the most recent Snippets in a given language.
    
    """
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Language.objects.get(slug__exact=bits[0])
    
    def items(self, obj):
        return Snippet.objects.get_by_language(obj.slug)[:15]
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def title(self, obj):
        return "%s: Latest snippets written in %s" % (current_site, obj.name)


class SnippetsByTagFeed(ByRelatedItemFeed):
    """
    Feed of the most recent Snippets with a given tag.
    
    """
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(slug__exact=bits[0])
    
    def items(self, obj):
        return Snippet.objects.get_by_tag(obj.slug)[:15]
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def title(self, obj):
        return "%s: Latest snippets tagged with '%s'" % (current_site, obj.name)
