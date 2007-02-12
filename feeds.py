from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.auth.models import User
from django.contrib.syndication.feeds import Feed
from models import Language, Snippet, Tag

class LatestSnippetsFeed(Feed):
    """
    Feed of the most recently published Snippets.
    
    """
    feed_type = Atom1Feed
    title = "Django snippets: All snippets"
    link = "/snippets/"
    description = "Latest snippets"
    author = "Snippets submitters"
    
    def item_author_name(self, item):
        return item.author.username
    
    def items(self):
        return Snippet.objects.all()[:15]


class SnippetsByAuthorFeed(Feed):
    """
    Feed of the most recent Snippets by a given author.
    
    """
    feed_type = Atom1Feed
    
    def author_name(self, obj):
        return obj.username
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username__exact=bits[0])
    
    def item_author(self, item):
        return item.author.username
    
    def items(self, obj):
        return Snippet.objects.by_author(obj.username)[:15]
    
    def link(self, obj):
        return "/users/%s/" % obj.username
    
    def title(self, obj):
        return "Latest snippets posted by %s" % obj.username


class SnippetsByLanguageFeed(Feed):
    """
    Feed of the most recent Snippets in a given language.
    
    """
    feed_type = Atom1Feed
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Language.objects.get(slug__exact=bits[0])
    
    def item_author(self, item):
        return item.author.username
    
    def items(self, obj):
        return Snippet.objects.by_language(obj.slug)[:15]
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def title(self, obj):
        return "Latest snippets written in %s" % obj.name


class SnippetsByTagFeed(Feed):
    """
    Feed of the most recent Snippets with a given tag.
    
    """
    feed_type = Atom1Feed
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(slug__exact=bits[0])
    
    def item_author(self, item):
        return item.author.username
    
    def items(self, obj):
        return Snippet.objects.by_tag(obj.slug)[:15]
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def title(self, obj):
        return "Latest snippets tagged with '%s'" % obj.name
