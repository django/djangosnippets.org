from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson as json
from django.views.generic.list_detail import object_list, object_detail

from haystack.query import SearchQuerySet

from taggit.models import Tag

from cab.forms import SnippetForm, SnippetFlagForm
from cab.models import Snippet, SnippetFlag, Language
from cab.utils import month_object_list


def snippet_list(request, queryset=None, **kwargs):
    if queryset is None:
        queryset = Snippet.objects.all()
    
    return month_object_list(
        request,
        queryset=queryset,
        paginate_by=20,
        **kwargs
    )

def snippet_detail(request, snippet_id):
    return object_detail(
        request,
        queryset=Snippet.objects.all(),
        object_id=snippet_id,
        extra_context={'flag_form': SnippetFlagForm()},
    )

def download_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    response = HttpResponse(snippet.code, mimetype='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s.%s' % \
        (snippet.id, snippet.language.file_extension)
    response['Content-Type'] = snippet.language.mime_type
    return response

@login_required
def rate_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    score = request.GET.get('score')
    if score and score in ['up', 'down']:
        score = {'up': 1, 'down': -1}[score]
        snippet.ratings.rate(user=request.user, score=score)
    return HttpResponseRedirect(snippet.get_absolute_url())

@login_required
def edit_snippet(request, snippet_id=None, template_name='cab/edit_snippet.html'):
    if not request.user.is_active:
        return HttpResponseForbidden()
    
    if snippet_id:
        snippet = get_object_or_404(Snippet, pk=snippet_id)
        if request.user.id != snippet.author.id:
            return HttpResponseForbidden()
    else:
        template_name = 'cab/add_snippet.html'
        snippet = Snippet(author=request.user, language=Language.objects.get(name='Python'))
    
    if request.method == 'POST':
        form = SnippetForm(instance=snippet, data=request.POST)
        if form.is_valid():
            snippet = form.save()
            messages.info(request, 'Your snippet has been saved')
            return HttpResponseRedirect(snippet.get_absolute_url())
    else:
        form = SnippetForm(instance=snippet)
    
    return render_to_response(template_name,
        {'form': form}, context_instance=RequestContext(request))

@login_required
def flag_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    snippet_flag = SnippetFlag(snippet=snippet, user=request.user)
    form = SnippetFlagForm(request.POST, instance=snippet_flag)
    
    if form.is_valid():
        snippet_flag = form.save()
        
        admin_link = request.build_absolute_uri(
            reverse('admin:cab_snippetflag_changelist')
        )
        
        mail_admins(
            'Snippet flagged: "%s"' % (snippet.title),
            '%s\n\nAdmin link: %s' % (snippet_flag, admin_link),
            fail_silently=True,
        )
        
        messages.info(request, 'Thank you for helping improve the site!')
    else:
        messages.error(request, 'Invalid form submission')
    
    return HttpResponseRedirect(snippet.get_absolute_url())

def author_snippets(request, username):
    user = get_object_or_404(User, username=username)
    snippet_qs = Snippet.objects.filter(author=user) 
    return snippet_list(
        request,
        snippet_qs,
        template_name='cab/user_detail.html',
        extra_context={'author': user},
    )

def matches_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    snippet_qs = Snippet.objects.matches_tag(tag)
    return snippet_list(
        request,
        queryset=snippet_qs,
        template_name='cab/tag_detail.html',
        extra_context={'tag': tag},
    )

def search(request):
    query = request.GET.get('q')
    snippet_qs = Snippet.objects.none()
    if query:
        snippet_qs = Snippet.objects.filter(
            Q(title__icontains=query) | 
            Q(tags__in=[query]) | 
            Q(author__username__iexact=query)
        ).distinct().order_by('-rating_score', '-pub_date')
    
    return snippet_list(
        request,
        queryset=snippet_qs,
        template_name='search/search.html',
        extra_context={'query':query},
    )

def autocomplete(request):
    q = request.GET.get('q', '')
    results = []
    if len(q) > 2:
        sqs = SearchQuerySet()
        result_set = sqs.filter(title_ngram=q)[:10]
        for obj in result_set:
            results.append({
                'title': obj.title,
                'author': obj.author,
                'url': obj.url
            })
    return HttpResponse(json.dumps(results), mimetype='application/json')

def tag_hint(request):
    q = request.GET.get('q', '')
    results = []
    if len(q) > 2:
        tag_qs = Tag.objects.filter(slug__startswith=q)
        annotated_qs = tag_qs.annotate(count=Count('taggit_taggeditem_items__id'))
        
        for obj in annotated_qs.order_by('-count', 'slug')[:10]:
            results.append({
                'tag': obj.slug,
                'count': obj.count,
            })
    
    return HttpResponse(json.dumps(results), mimetype='application/json')
