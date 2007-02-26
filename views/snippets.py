"""
Views which work with Snippets, allowing them to be added, modified,
rated and viewed according to various criteria.

"""

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cab.forms import SnippetForm
from cab.models import Language, Rating, Snippet, Tag
from bookmarks import base_generic_dict

def add_snippet(request):
    """
    Allows a user to add a Snippet to the database.
    
    Context::
        form
            The form to add the Snippet.
    
    Template::
        cab/add_snippet_form.html
    
    """
    original_id = request.GET.get('oid', None)
    
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            new_snippet = Snippet(title=form.clean_data['title'],
                                  description=form.clean_data['description'],
                                  code=form.clean_data['code'],
                                  tag_list=form.clean_data['tag_list'],
                                  language_id=form.clean_data['language'],
                                  author=request.user)
            if original_id:
                new_snippet.original_id = original_id
            new_snippet.save()
            return HttpResponseRedirect(new_snippet.get_absolute_url())
    else:
        form = SnippetForm()
    return render_to_response('cab/add_snippet_form.html',
                              { 'form': form },
                              context_instance=RequestContext(request))
add_snippet = login_required(add_snippet)

def download(request, snippet_id):
    """
    Allows a user to download a Snippet's code.
    
    Context::
        None, returns a downloadable file.
    
    Template::
        None, returns a downloadable file.
    
    """
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    response = HttpResponse(snippet.code, mimetype='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s.%s' % (snippet.id,
                                                                      snippet.language.file_extension)
    response['Content-Type'] = snippet.language.mime_type
    return response

def edit_snippet(request, snippet_id):
    """
    Allows a user to edit an existing Snippet.
    
    Context::
        form
            The form to add the Snippet.
    
        original
            The Snippet being edited.
    
    Template::
        cab/edit_snippet_form.html
    
    """
    snippet = get_object_or_404(Snippet,
                                pk=snippet_id,
                                author__pk=request.user.id)
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            for field in ['title', 'description', 'code', 'tag_list']:
                setattr(snippet, field, form.clean_data[field])
            snippet.language_id = form.clean_data['language_id']
            snippet.save()
            return HttpResponseRedirect(snippet.get_absolute_url())
    else:
        form = SnippetForm(initial=dict(snippet.__dict__,
                                        language=snippet.language))
    return render_to_response('cab/edit_snippet_form.html',
                              { 'form': form,
                                'original': snippet },
                              context_instance=RequestContext(request))
edit_snippet = login_required(edit_snippet)

def rate_snippet(request, snippet_id):
    """
    Allows a user to rate a Snippet.
    
    Context::
        None, returns a redirect back to the Snippet.
    
    Template::
        None, returns a redirect back to the Snippet.
    
    """
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    
    if not Rating.objects.already_rated(request.user.id, snippet.id):
        score = request.GET.get('score')
        if score:
            rating = Rating.objects.create(snippet=snippet,
                                           user=request.user,
                                           score={ 'up': 1,
                                                   'down': -1 }[score])
    return HttpResponseRedirect(snippet.get_absolute_url())
rate_snippet = login_required(rate_snippet)

def snippets_by_author(request, username):
    """
    List of Snippets submitted by a particular User.
    
    Context::
    Same as the generic ``list_detail.object_list`` view, with
    one extra variable:
    
        object
            The User
    
    Template::
        cab/user_detail.html
    
    """
    user = get_object_or_404(User, username__exact=username)
    return list_detail.object_list(request,
                                   queryset=Snippet.objects.get_by_author(user.username).select_related(),
                                   extra_context={ 'object': user },
                                   template_name='cab/user_detail.html',
                                   **base_generic_dict)

def snippets_by_language(request, slug):
    """
    List of Snippets written in a particular Language.
    
    Context::
    Same as the generic ``list_detail.object_list`` view, with
    one extra variable:
    
        object
            The Language
    
    Template::
        cab/language_detail.html
    
    """
    language = get_object_or_404(Language, slug__exact=slug)
    return list_detail.object_list(request,
                                   queryset=Snippet.objects.get_by_language(slug).select_related(),
                                   extra_context={ 'object': language },
                                   template_name='cab/language_detail.html',
                                   **base_generic_dict)

def snippets_by_tag(request, slug):
    """
    List of Snippets with a particular Tag.
    
    Context::
    Same as the generic ``list_detail.object_list`` view, with
    one extra variable:
    
        object
            The Tag
    
    Template::
        cab/tag_detail.html
    
    """
    tag = get_object_or_404(Tag, slug__exact=slug)
    return list_detail.object_list(request,
                                   queryset=Snippet.objects.get_by_tag(slug).select_related(),
                                   extra_context={ 'object': tag },
                                   template_name='cab/tag_detail.html',
                                   **base_generic_dict)

def snippet_detail(request, snippet_id):
    """
    Detail view of a Snippet.
    
    Context::
        object
            The Snippet object.
    
        num_ratings
            The number of Ratings this Snippet has received.
    
        rating_score
            The sum of this Snippet's received ratings.
    
    Template::
        cab/snippet_detail.html
    
    """
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    return render_to_response('cab/snippet_detail.html',
                              { 'object': snippet,
                                'num_ratings': snippet.rating_set.count(),
                                'rating_score': Rating.objects.score_for_snippet(snippet.id) },
                              context_instance=RequestContext(request))
