"""
General-purpose tags for working with various aspects of
Snippets -- whether a user has bookmarked/rated a given
Snippet, etc.

"""

from django import template
from cab.models import Bookmark, Rating

register = template.Library()


class IfBookmarkedNode(template.Node):
    def __init__(self, user_id, snippet_id, nodelist_true, nodelist_false):
        self.user_id = user_id
        self.snippet_id = snippet_id
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    
    def render(self, context):
        try:
            self.user_id = template.resolve_variable(self.user_id, context)
            self.snippet_id = template.resolve_variable(self.snippet_id, context)
        except template.VariableDoesNotExist:
            return ''
        if Bookmark.objects.already_bookmarked(self.user_id, self.snippet_id):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


class IfRatedNode(template.Node):
    def __init__(self, user_id, snippet_id, nodelist_true, nodelist_false):
        self.user_id = user_id
        self.snippet_id = snippet_id
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    
    def render(self, context):
        try:
            self.user_id = template.resolve_variable(self.user_id, context)
            self.snippet_id = template.resolve_variable(self.snippet_id, context)
        except template.VariableDoesNotExist:
            return ''
        if Rating.objects.already_rated(self.user_id, self.snippet_id):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


class RatingForSnippetNode(template.Node):
    def __init__(self, snippet_id, context_var):
        self.snippet_id = snippet_id
        self.context_var = context_var
    
    def render(self, context):
        try:
            self.snippet_id = template.resolve_variable(self.snippet_id, context)
        except template.VariableDoesNotExist:
            return ''
        context[self.context_var] = Rating.objects.score_for_snippet(self.snippet_id)
        return ''


class RatingByUserNode(template.Node):
    def __init__(self, user_id, snippet_id, context_var):
        self.user_id, self.snippet_id = user_id, snippet_id
        self.context_var = context_var
    
    def render(self, context):
        try:
            self.user_id = template.resolve_variable(self.user_id, context)
            self.snippet_id = template.resolve_variable(self.snippet_id, context)
            rating = Rating.objects.get(user__pk=self.user_id, snippet__pk=self.snippet_id)
        except template.VariableDoesNotExist:
            return ''
        except Rating.DoesNotExist:
            return ''
        context[self.context_var] = rating
        return ''


def do_if_bookmarked(parser, token):
    """
    Returns either of two blocks of content depending on whether a
    given User has bookmarked a given Snippet.
    
    Example::
        {% if_already_bookmarked user.id object.id %}
            <p>This Snippet is in your bookmarks.</p>
        {% else %}
            <p>You haven't bookmarked this Snippet.</p>
        {% endif_already_bookmarked %}
            
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes exactly two arguments" % bits[0])
    nodelist_true = parser.parse(('else', 'endif_bookmarked'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_bookmarked',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IfBookmarkedNode(bits[1], bits[2], nodelist_true, nodelist_false)

def do_if_rated(parser, token):
    """
    Returns either of two blocks of content depending on whether a
    given User has rated a given Snippet.
    
    Example::
        {% if_rated user.id object.id %}
            <p>You have already rated this Snippet.</p>
        {% else %}
            <p>You haven't rated this Snippet yet.</p>
        {% endif_rated %}
    
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes exactly two arguments" % bits[0])
    nodelist_true = parser.parse(('else', 'endif_rated'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_rated',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IfRatedNode(bits[1], bits[2], nodelist_true, nodelist_false)

def do_rating_for_snippet(parser, token):
    """
    Retrieves a list containing the total score for a Snippet and
    the number of Ratings it's received, and stores them in a
    specified context variable.
    
    Example usage::
        {% get_rating_for_snippet object.id as score %}
    
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes exactly three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return RatingForSnippetNode(bits[1], bits[3])

def do_rating_by_user(parser, token):
    """
    Returns a User's Rating of a Snippet, if any.
    
    Example::
        {% get_rating_by_user user.id object.id as rating %}
    
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes exactly four arguments" % bits[0])
    if bits[3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return RatingByUserNode(bits[1], bits[2], bits[4])

register.tag('get_rating_for_snippet', do_rating_for_snippet)
register.tag('if_bookmarked', do_if_bookmarked)
register.tag('if_rated', do_if_rated)
register.tag('get_rating_by_user', do_rating_by_user)
