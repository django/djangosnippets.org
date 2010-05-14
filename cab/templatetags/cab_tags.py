from django import template

from cab.models import Snippet, Bookmark, Rating


def do_if_bookmarked(parser, token):
    """
    Returns either of two blocks of content depending on whether a
    given User has bookmarked a given Snippet.
    
    Example::
        {% if_bookmarked user.id object.id %}
            <p>You have already bookmarked this Snippet.</p>
        {% else %}
            <p>You haven't rated bookmarked Snippet yet.</p>
        {% endif_bookmarked %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s tag takes two arguments" % bits[0])
    nodelist_true = parser.parse(('else', 'endif_bookmarked'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_bookmarked',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IfBookmarkedNode(bits[1], bits[2], nodelist_true, nodelist_false)

class IfBookmarkedNode(template.Node):
    def __init__(self, user_id, snippet_id, nodelist_true, nodelist_false):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.user_id = template.Variable(user_id)
        self.snippet_id = template.Variable(snippet_id)
    
    def render(self, context):
        try:
            user_id = self.user_id.resolve(context)
            snippet_id = self.snippet_id.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        if Bookmark.objects.filter(user__pk=user_id, snippet__pk=snippet_id):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


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
        try:
            rating = Rating.objects.get(user__pk=self.user_id, snippet__pk=self.snippet_id)
        except Rating.DoesNotExist:
            return self.nodelist_false.render(context)
        else:
            context['rating'] = rating
            return self.nodelist_true.render(context)

        
register = template.Library()
register.tag('if_bookmarked', do_if_bookmarked)
register.tag('if_rated', do_if_rated)
