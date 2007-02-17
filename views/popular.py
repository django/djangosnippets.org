"""
Views which deal with popular items -- most-bookmarked, highest-rated
and most-used.

"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from cab.models import Bookmark, Rating, Snippet

def most_bookmarked(request):
    """
    Shows a list of the most-bookmarked Snippets.
    
    Context::
        object_list
            The list of Snippets
    
    Template::
        cab/most_bookmarked.html
    
    """
    return render_to_response('cab/most_bookmarked.html',
                              { 'object_list': Bookmark.objects.most_bookmarked(10) },
                              context_instance=RequestContext(request))

def top_authors(request):
    """
    Shows a list of the authors who have submitted the most Snippets.
    
    Context::
        object_list
            The list of authors
    
    Template::
        cab/top_authors.html
    
    """
    return render_to_response('cab/top_authors.html',
                              { 'object_list': Snippet.objects.top_items('author', 10) },
                              context_instance=RequestContext(request))

def top_languages(request):
    """
    Shows a list of the most-used Languages.
    
    Context::
        object_list
            The list of Languages
    
    Template::
        cab/top_languages.html
    
    """
    return render_to_response('cab/top_languages.html',
                              { 'object_list': Snippet.objects.top_items('language', 10) },
                              context_instance=RequestContext(request))

def top_rated(request):
    """
    Shows a list of the top-rated Snippets.
    
    Context::
        object_list
            The list of Snippets
    
    Template::
        cab/top_rated.html
    
    """
    return render_to_response('cab/top_rated.html',
                              { 'object_list': Rating.objects.top_rated(10) },
                              context_instance=RequestContext(instance))

def top_tags(request):
    """
    Shows a list of the most-used Tags.
    
    Context::
        object_list
            The list of Tags
    
    Template::
        cab/top_tags.html
    
    """
    return render_to_response('cab/top_tags.html',
                              { 'object_list': Snippet.objects.top_items('tag', 10) },
                              context_instance=RequestContext(request))
