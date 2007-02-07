from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cab.models import Bookmark, Language, Snippet, Tag

def most_bookmarked(request):
    """
    Shows a list of the most-bookmarked Snippets.
    
    Context::
        object_list
            The list of Snippets
    
    Template::
        snippets/most_bookmarked.html
    
    """
    return render_to_response('snippets/most_bookmarked.html',
                              { 'object_list': Bookmark.objects.most_bookmarked(10) },
                              context_instance=RequestContext(request))

def top_authors(request):
    """
    Shows a list of the authors who have submitted the most
    Snippets.
    
    Context::
        object_list
            The list of authors
    
    Template::
        snippets/top_authors.html
    
    """
    return render_to_response('snippets/top_authors.html',
                              { 'object_list': Snippet.objects.top_items('author', 10) },
                              context_instance=RequestContext(request))

def top_languages(request):
    """
    Shows a list of the most-used Languages.
    
    Context::
        object_list
            The list of Languages
    
    Template::
        snippets/top_languages.html
    
    """
    return render_to_response('snippets/top_languages.html',
                              { 'object_list': Snippet.objects.top_items('language', 10) },
                              context_instance=RequestContext(request))

def top_rated(request):
    """
    Shows a list of the top-rated Snippets.
    
    Context::
        object_list
            The list of Snippets
    
    Template::
        snippets/top_rated.html
    
    """
    return render_to_response('snippets/top_rated.html',
                              { 'object_list': Rating.objects.top_rated(10) },
                              context_instance=RequestContext(instance))

def top_tags(request):
    """
    Shows a list of the most-used Tags.
    
    Context::
        object_list
            The list of Tags
    
    Template::
        snippets/top_tags.html
    
    """
    return render_to_response('snippets/top_tags.html',
                              { 'object_list': Snippet.objects.top_items('tag', 10) },
                              context_instance=RequestContext(request))
