from django import template
from cab.models import Bookmark, Rating, Snippet

register = template.Library()


class MostBookmarkedNode(template.Node):
    def __init__(self, num, context_var):
        self.context_var = context_var
        self.num = num
    
    def render(self, context):
        context[self.context_var] = Bookmark.objects.most_bookmarked(self.num)
        return ''


class TopItemsNode(template.Node):
    def __init__(self, item_type, num, context_var):
        self.item_type, self.num = item_type, num
        self.context_var = context_var
    
    def render(self, context):
        context[self.context_var] = Snippet.objects.top_items(self.item_type, self.num)
        return ''


class TopRatedNode(template.Node):
    def __init__(self, num, context_var):
        self.num = num
        self.context_var = context_var
    
    def render(self, context):
        context[self.context_var] = Rating.objects.top_rated(num)
        return ''


def do_most_bookmarked(parser, token):
    """
    Returns a given number of most-bookmarked Snippets.
    
    Example::
        {% get_most_bookmarked 5 as most_bookmarked %}
    
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes exactly three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return MostBookmarkedNode(bits[1], bits[3])

def do_top_items(parser, token):
    """
    Returns a given number of most-used items.
    
    Examples::
        {% get_top_authors 5 as top_authors %}
        {% get_top_languages 5 as top_languages %}
        {% get_top_tags 5 as top_tags %}
    
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes exactly three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    item_type = bits[1].split('_')[1][:-1]
    return TopItemsNode(item_type, bits[1], bits[3])

def do_top_rated(parser, token):
    """
    Returns a given number of top-rated Snippets.
    
    Example::
        {% get_top_rated 5 as top_rated %}
    
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes either exactly three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' must be 'as'" % bits[0])
    return TopRatedNode(bits[1], bits[3])

register.tag('get_most_bookmarked', do_most_bookmarked)
register.tag('get_top_rated', do_top_rated)
register.tag('get_top_authors', do_top_items)
register.tag('get_top_languages', do_top_items)
register.tag('get_top_tags', do_top_items)
